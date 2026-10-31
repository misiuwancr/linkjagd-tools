import "dotenv/config";
import { createClient } from "@libsql/client";
import { germanFromHtml } from "@/lib/facts";
import { robotsAllows } from "@/lib/logos";

const USER_AGENT = "LinkjagdToolsFactBot/1.0";

async function main() {
  const url = process.env.DATABASE_URL;
  if (!url) throw new Error("DATABASE_URL fehlt.");
  const client = createClient({ url });
  const rows = await client.execute(
    "select slug, original_url from tools where publish_status = 'published' and is_example = 0 and german_ui = 'unklar'",
  );
  let marked = 0;
  let seen = 0;
  const queue = rows.rows.map((row) => ({ slug: String(row.slug), originalUrl: String(row.original_url) }));
  let index = 0;
  async function one(entry: (typeof queue)[number]) {
    seen += 1;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 7000);
    try {
      const pageUrl = new URL(entry.originalUrl);
      const robots = await fetch(new URL("/robots.txt", pageUrl.origin), {
        signal: controller.signal,
        headers: { "user-agent": USER_AGENT },
      }).then((response) => (response.ok ? response.text() : "")).catch(() => "");
      if (!robotsAllows(robots, pageUrl.pathname || "/")) return;
      const response = await fetch(entry.originalUrl, {
        signal: controller.signal,
        redirect: "follow",
        headers: { "user-agent": USER_AGENT, accept: "text/html" },
      });
      if (!response.ok) return;
      const html = (await response.text()).slice(0, 200_000);
      if (germanFromHtml(html) !== "ja") return;
      await client.execute({ sql: "update tools set german_ui = 'ja' where slug = ? and german_ui = 'unklar'", args: [entry.slug] });
      marked += 1;
    } catch {
      return;
    } finally {
      clearTimeout(timer);
    }
  }
  async function worker() {
    while (index < queue.length) {
      const current = queue[index];
      index += 1;
      await one(current);
    }
  }
  await Promise.all(Array.from({ length: 12 }, () => worker()));
  console.log(JSON.stringify({ marked, seen, total: queue.length }));
}

main();
