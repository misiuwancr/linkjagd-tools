import "dotenv/config";
import fs from "fs";
import path from "path";
import { eq } from "drizzle-orm";
import { affiliatePrograms, tools } from "@/db/schema";
import { getDb } from "@/db/client";
import { importDiscoveredTool } from "@/lib/import/service";
import { saveAffiliateRecord } from "@/lib/tools/mutations";
import { getToolBySlug, refreshSearchText } from "@/lib/tools/repository";
import catalog from "@/data/verified-tools.json";

const deadNames = [
  "GeoSpy.ai",
  "Maze",
  "Godmode",
  "Any Summary",
  "Stable WarpFusion",
  "Nack",
  "Intellisay",
  "Deepfakes.lol",
  "Scribble Diffusion",
  "Wonder Dynamics",
  "ChatGPT for Search Engines",
  "kAI",
  "Musenet (OpenAI)",
];

type Entry = (typeof catalog)[number];

function missing(entry: Entry) {
  const gaps: string[] = [];
  if (!entry.shortDescriptionDe) gaps.push("kurzbeschreibung");
  if (!entry.longDescriptionDe) gaps.push("langbeschreibung");
  if (entry.licenseType === "unknown") gaps.push("lizenz");
  if (entry.licenseType === "open_source" && !entry.oss?.license) gaps.push("oss_lizenzname");
  if (!entry.partnerStatus) gaps.push("affiliate_status");
  return gaps;
}

function note(entry: Entry) {
  if (entry.partnerStatus === "found") {
    return "verified-import. Ein öffentliches Programm ist bekannt. Ein eigener Affiliate-Link ist nicht hinterlegt und wird nicht aus der Recherche übernommen.";
  }
  return "verified-import. Kein eigener Affiliate-Link. Programm nicht als Weiterleitungsziel gespeichert.";
}

async function main() {
  const database = await getDb();
  const errors: string[] = [];
  let created = 0;
  let updated = 0;
  let published = 0;
  let archived = 0;

  for (const name of deadNames) {
    const rows = await database.select().from(tools).where(eq(tools.name, name));
    for (const row of rows) {
      if (row.contentLocked) continue;
      await database
        .update(tools)
        .set({ publishStatus: "archived", updatedAt: new Date(), internalNotes: "Archiviert: nicht mehr verfügbar oder von der Liste ausgeschlossen." })
        .where(eq(tools.id, row.id));
      archived += 1;
    }
  }

  for (const entry of catalog) {
    try {
      const imported = await importDiscoveredTool(database, {
        name: entry.name,
        originalUrl: entry.originalUrl,
        shortDescriptionDe: entry.shortDescriptionDe,
        longDescriptionDe: entry.longDescriptionDe,
        pricingModel: entry.pricingModel,
        categorySlugs: entry.categorySlugs,
        tags: entry.licenseType === "open_source" ? ["Open Source"] : ["Geprüft"],
        discoverySource: entry.discoverySource,
      });
      const existing = imported.ok ? null : imported.existingSlug ? await getToolBySlug(database, imported.existingSlug) : null;
      if (!imported.ok && !existing) {
        errors.push(`${entry.name}: ${imported.error}`);
        continue;
      }
      const id = imported.ok ? imported.id : existing!.id;
      const current = existing ?? (await getToolBySlug(database, imported.ok ? imported.slug : ""));
      const locked = Boolean(current?.contentLocked);
      const gaps = missing(entry);
      const patch: Record<string, unknown> = {
        missingFields: JSON.stringify(gaps),
        lastCheckedAt: new Date(),
        updatedAt: new Date(),
      };
      if (!locked) {
        patch.shortDescriptionDe = entry.shortDescriptionDe;
        patch.longDescriptionDe = entry.longDescriptionDe;
        patch.featuresDe = JSON.stringify(entry.featuresDe);
        patch.useCasesDe = JSON.stringify(entry.useCasesDe);
        patch.pricingModel = entry.pricingModel;
        patch.licenseType = entry.licenseType;
        patch.originalUrl = entry.originalUrl;
        patch.domain = entry.domain;
        patch.beginnerFriendly = entry.beginnerFriendly;
        patch.discoverySource = entry.discoverySource;
        if (entry.oss) {
          patch.ossProjectUrl = entry.oss.projectUrl;
          patch.ossRepoUrl = entry.oss.repoUrl;
          patch.ossLicense = entry.oss.license;
          patch.ossOperatingSystems = JSON.stringify(entry.oss.systems);
          patch.ossInstallNotes = entry.oss.install;
        }
        if (current?.publishStatus === "draft" && entry.verified) {
          patch.publishStatus = "published";
          published += 1;
        }
      }
      await database.update(tools).set(patch).where(eq(tools.id, id));
      await refreshSearchText(database, id);
      const programs = await database.select().from(affiliatePrograms).where(eq(affiliatePrograms.toolId, id));
      const hasOwnLink = programs.some((program) => program.affiliateUrl && program.isActive && program.status === "active");
      if (!hasOwnLink && !programs.some((program) => (program.notes || "").includes("verified-import"))) {
        const saved = await saveAffiliateRecord(database, id, {
          affiliateUrl: "",
          network: "manual",
          partnerProgramId: "",
          status: entry.partnerStatus,
          priority: 0,
          isActive: false,
          notes: note(entry),
        });
        if (!saved.ok) errors.push(`${entry.name}: ${saved.error}`);
      }
      if (imported.ok) created += 1;
      else updated += 1;
    } catch (error) {
      errors.push(`${entry.name}: ${error instanceof Error ? error.message : "Fehler"}`);
    }
  }

  const log = errors.length ? errors.join("\n") : "Keine Fehler.";
  fs.mkdirSync("/opt/cursor/artifacts", { recursive: true });
  fs.writeFileSync("/opt/cursor/artifacts/verified-import-log.txt", log);
  fs.writeFileSync(path.join(process.cwd(), "data", "verified-import-log.txt"), log);
  console.log({ created, updated, published, archived, errors: errors.length });
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
