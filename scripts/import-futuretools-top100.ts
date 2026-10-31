import "dotenv/config";
import fs from "fs";
import path from "path";
import { eq } from "drizzle-orm";
import { affiliatePrograms, tools } from "@/db/schema";
import { getDb } from "@/db/client";
import { importDiscoveredTool } from "@/lib/import/service";
import { saveAffiliateRecord } from "@/lib/tools/mutations";
import { getToolBySlug, refreshSearchText } from "@/lib/tools/repository";
import catalog from "@/data/futuretools-top100.json";

type Entry = (typeof catalog)[number];

const priceDe: Record<string, string> = {
  free: "Kostenlos",
  freemium: "Freemium",
  paid: "Kostenpflichtig",
  open_source: "Open Source",
};

function csvCell(value: string) {
  return `"${value.replaceAll('"', '""')}"`;
}

function affiliateNote(entry: Entry) {
  if (entry.partner === "ja") {
    return `futuretools-top100. Öffentliche Programmseite, nicht als Weiterleitung verwendet: ${entry.programUrl}`;
  }
  if (entry.partner === "unklar") {
    return "futuretools-top100. Programmseite nicht geprüft oder die Website war nicht erreichbar.";
  }
  return "futuretools-top100. Auf der Startseite und unter /affiliate(s) keine klar erkennbare Programmseite gefunden.";
}

async function saveLogo(entry: Entry) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  try {
    const home = await fetch(entry.originalUrl, {
      redirect: "follow",
      signal: controller.signal,
      headers: { "user-agent": "LinkjagdTools/1.0", accept: "text/html" },
    });
    if (!home.ok) return null;
    const html = await home.text();
    const href =
      html.match(/<link[^>]+rel=["'][^"']*icon[^"']*["'][^>]+href=["']([^"']+)["']/i)?.[1] ||
      html.match(/<link[^>]+href=["']([^"']+)["'][^>]+rel=["'][^"']*icon[^"']*["']/i)?.[1] ||
      "/favicon.ico";
    const iconUrl = new URL(href, home.url);
    const host = iconUrl.hostname.replace(/^www\./, "");
    if (host !== entry.domain && !host.endsWith(`.${entry.domain}`) && !entry.domain.endsWith(`.${host}`)) {
      return null;
    }
    const image = await fetch(iconUrl, { redirect: "follow", signal: controller.signal, headers: { "user-agent": "LinkjagdTools/1.0" } });
    if (!image.ok) return null;
    const type = image.headers.get("content-type") || "";
    const ext = type.includes("svg") ? "svg" : type.includes("png") ? "png" : type.includes("webp") ? "webp" : type.includes("jpeg") ? "jpg" : null;
    if (!ext) return null;
    const bytes = Buffer.from(await image.arrayBuffer());
    if (bytes.length < 40 || bytes.length > 350_000) return null;
    const dir = path.join(process.cwd(), "public", "logos");
    fs.mkdirSync(dir, { recursive: true });
    const filename = `${entry.rank.toString().padStart(3, "0")}-${entry.domain.replace(/[^a-z0-9.]+/gi, "-")}.${ext}`;
    fs.writeFileSync(path.join(dir, filename), bytes);
    return `/logos/${filename}`;
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

async function pool<T>(items: T[], limit: number, worker: (item: T) => Promise<void>) {
  let cursor = 0;
  async function run() {
    while (cursor < items.length) {
      const item = items[cursor++];
      await worker(item);
    }
  }
  await Promise.all(Array.from({ length: limit }, run));
}

async function main() {
  const database = await getDb();
  const withLogos = process.env.SKIP_LOGOS !== "1";
  const logos = new Map<string, string>();
  if (withLogos) {
    await pool(catalog, 8, async (entry) => {
      const logo = await saveLogo(entry);
      if (logo) logos.set(entry.domain, logo);
    });
  }
  let created = 0;
  let existingCount = 0;
  for (const entry of catalog) {
    const imported = await importDiscoveredTool(database, {
      name: entry.name,
      originalUrl: entry.originalUrl,
      shortDescriptionDe: entry.shortDescriptionDe,
      longDescriptionDe: entry.longDescriptionDe,
      pricingModel: entry.pricingModel,
      categorySlugs: entry.categorySlugs,
      tags: ["Top-100"],
      discoverySource: entry.discoverySource,
    });
    const existing = imported.ok ? null : imported.existingSlug ? await getToolBySlug(database, imported.existingSlug) : null;
    if (!imported.ok && (!existing || existing.discoverySource !== "futuretools-top100")) {
      console.error("übersprungen", entry.name, imported.error);
      return;
    }
    const row = imported.ok ? { id: imported.id } : { id: existing!.id };
    if (imported.ok) created += 1;
    else existingCount += 1;
    const logo = logos.get(entry.domain) ?? null;
    await database
      .update(tools)
      .set({
        featuresDe: JSON.stringify(entry.featuresDe),
        internalNotes: [
          `Rang ${entry.rank} auf futuretools.io/tools?sort=popular (Most Popular — All Time), abgerufen am 31. Oktober 2026.`,
          entry.urlNote,
          "Texte und Bilder von FutureTools wurden nicht übernommen.",
        ]
          .filter(Boolean)
          .join(" "),
        ...(logo ? { logo } : {}),
        updatedAt: new Date(),
      })
      .where(eq(tools.id, row.id));
    await refreshSearchText(database, row.id);
    const programs = await database.select().from(affiliatePrograms).where(eq(affiliatePrograms.toolId, row.id));
    const already = programs.find((program) => (program.notes || "").includes("futuretools-top100"));
    if (!already) {
      const saved = await saveAffiliateRecord(database, row.id, {
        affiliateUrl: "",
        network: "manual",
        partnerProgramId: "",
        status: entry.partner === "ja" ? "found" : "none_found",
        priority: 0,
        isActive: false,
        notes: affiliateNote(entry),
      });
      if (!saved.ok) console.error("Partnerstatus", entry.name, saved.error);
    }
    console.log(`${entry.rank} ${entry.name} ${imported.ok ? "neu" : "vorhanden"}`);
  }

  const header = ["Name", "Domain", "Kategorie", "Preismodell", "Partnerprogramm", "Programm-URL"];
  const lines = [header.map(csvCell).join(",")];
  for (const entry of catalog) {
    lines.push(
      [
        entry.name,
        entry.domain,
        entry.categorySlugs.join(" | "),
        priceDe[entry.pricingModel] || entry.pricingModel,
        entry.partner,
        entry.programUrl,
      ]
        .map(csvCell)
        .join(","),
    );
  }
  const csv = `${lines.join("\n")}\n`;
  const artifactDir = "/opt/cursor/artifacts";
  fs.mkdirSync(artifactDir, { recursive: true });
  fs.writeFileSync(path.join(artifactDir, "futuretools-top100.csv"), csv);
  fs.writeFileSync(path.join(process.cwd(), "data", "futuretools-top100.csv"), csv);
  console.log(`fertig: ${created} neu, ${existingCount} vorhanden`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
