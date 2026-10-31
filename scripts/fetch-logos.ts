import "dotenv/config";
import fs from "fs";
import path from "path";
import sharp from "sharp";
import { createClient } from "@libsql/client";
import { isFaviconProxy, parseIconCandidates, parseManifestIcons, robotsAllows, type IconCandidate } from "@/lib/logos";

const USER_AGENT = "LinkjagdToolsLogoBot/1.0 (+https://linkjagd.tools; logo fetch)";
const OUT = path.join(process.cwd(), "public", "logos");
const TIMEOUT_MS = 7000;

function withTimeout(url: string) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  return fetch(url, {
    signal: controller.signal,
    redirect: "follow",
    headers: { "user-agent": USER_AGENT, accept: "text/html,application/xhtml+xml,image/*,application/json" },
  }).finally(() => clearTimeout(timer));
}

async function robotsFor(origin: string) {
  try {
    const response = await withTimeout(new URL("/robots.txt", origin).toString());
    if (!response.ok) return "";
    return await response.text();
  } catch {
    return "";
  }
}

function pathOf(href: string) {
  return new URL(href).pathname || "/";
}

async function candidatesFor(pageUrl: string, html: string, robots: string) {
  const page = new URL(pageUrl);
  const listed = parseIconCandidates(html, pageUrl).filter((item) => robotsAllows(robots, pathOf(item.href)));
  const manifest = listed.find((item) => item.score === 0);
  const icons = listed.filter((item) => item.score > 0);
  if (manifest && robotsAllows(robots, pathOf(manifest.href))) {
    try {
      const response = await withTimeout(manifest.href);
      if (response.ok) {
        const body = (await response.json()) as { icons?: { src?: string; sizes?: string; purpose?: string }[] };
        icons.push(...parseManifestIcons(body, manifest.href).filter((item) => robotsAllows(robots, pathOf(item.href))));
      }
    } catch {
      // Manifest ist optional.
    }
  }
  if (icons.length === 0) {
    const fallback = new URL("/favicon.ico", page.origin).toString();
    if (robotsAllows(robots, "/favicon.ico") && !isFaviconProxy(fallback)) icons.push({ href: fallback, score: 1 });
  }
  return icons.sort((a, b) => b.score - a.score);
}

async function saveIcon(slug: string, icons: IconCandidate[]) {
  for (const icon of icons.slice(0, 4)) {
    try {
      const response = await withTimeout(icon.href);
      if (!response.ok) continue;
      const type = response.headers.get("content-type") ?? "";
      if (type.includes("text/html")) continue;
      const bytes = Buffer.from(await response.arrayBuffer());
      if (bytes.length < 32 || bytes.length > 2_000_000) continue;
      const file = path.join(OUT, `${slug}.webp`);
      await sharp(bytes, { failOn: "none" }).resize(128, 128, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } }).webp({ quality: 80 }).toFile(file);
      const stat = fs.statSync(file);
      if (stat.size < 40) {
        fs.unlinkSync(file);
        continue;
      }
      return `/logos/${slug}.webp`;
    } catch {
      continue;
    }
  }
  return null;
}

async function main() {
  const url = process.env.DATABASE_URL;
  if (!url) throw new Error("DATABASE_URL fehlt.");
  fs.mkdirSync(OUT, { recursive: true });
  const client = createClient({ url });
  const rows = await client.execute(
    "select slug, original_url, logo from tools where publish_status = 'published' and is_example = 0 order by name",
  );
  let saved = 0;
  let skipped = 0;
  let failed = 0;
  const queue = rows.rows.map((row) => ({
    slug: String(row.slug),
    originalUrl: String(row.original_url),
    logo: row.logo ? String(row.logo) : "",
  }));
  async function one(entry: (typeof queue)[number]) {
    const target = path.join(OUT, `${entry.slug}.webp`);
    if (entry.logo === `/logos/${entry.slug}.webp` && fs.existsSync(target)) {
      skipped += 1;
      return;
    }
    let origin: string;
    try {
      origin = new URL(entry.originalUrl).origin;
    } catch {
      failed += 1;
      return;
    }
    const robots = await robotsFor(origin);
    if (!robotsAllows(robots, new URL(entry.originalUrl).pathname || "/")) {
      failed += 1;
      return;
    }
    try {
      const page = await withTimeout(entry.originalUrl);
      if (!page.ok) {
        failed += 1;
        return;
      }
      const html = await page.text();
      const icons = await candidatesFor(page.url, html, robots);
      const stored = await saveIcon(entry.slug, icons);
      if (!stored) {
        failed += 1;
        return;
      }
      await client.execute({ sql: "update tools set logo = ? where slug = ?", args: [stored, entry.slug] });
      saved += 1;
    } catch {
      failed += 1;
    }
  }
  const workers = 10;
  let index = 0;
  async function worker() {
    while (index < queue.length) {
      const current = queue[index];
      index += 1;
      await one(current);
      if ((saved + skipped + failed) % 50 === 0) {
        console.log(JSON.stringify({ saved, skipped, failed, seen: saved + skipped + failed, total: queue.length }));
      }
    }
  }
  await Promise.all(Array.from({ length: workers }, () => worker()));
  console.log(JSON.stringify({ saved, skipped, failed, total: queue.length }));
}

main();
