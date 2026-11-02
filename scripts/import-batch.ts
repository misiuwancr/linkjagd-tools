import "dotenv/config";
import fs from "node:fs";
import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import * as schema from "@/db/schema";
import { resolveAppDatabase } from "@/db/resolve";
import { createRetryingFetch } from "@/db/http";
import { importBatchCandidate } from "@/lib/import/batch";
import { domainFromUrl, slugify } from "@/lib/utils";

async function main() {
  const file = process.argv[2];
  if (!file) throw new Error("Aufruf: import-batch.ts DATEI [--apply] [--publish] [--remote] [--report=DATEI]");
  const apply = process.argv.includes("--apply");
  const publish = process.argv.includes("--publish");
  const target = resolveAppDatabase();
  if (apply && target.kind === "turso" && !process.argv.includes("--remote")) throw new Error("Remote-Schreibzugriff erfordert --remote.");
  const rows: unknown = JSON.parse(fs.readFileSync(file, "utf8"));
  if (!Array.isArray(rows)) throw new Error("Kandidaten müssen eine Liste sein.");
  // Do not call getDb: a production import must never run schema migrations or seed data.
  const client = createClient({ url: target.url, authToken: target.authToken, ...(target.kind === "turso" ? { fetch: createRetryingFetch(undefined, { attempts: 1 }) } : {}) });
  const database = drizzle(client, { schema });
  const report = process.argv.find(a => a.startsWith("--report="))?.slice(9) || `${file}.results.jsonl`;
  const names = new Set<string>();
  const urls = new Set<string>();
  const shared = new Set(["github.com", "gitlab.com", "invent.kde.org", "huggingface.co", "apps.apple.com", "chromewebstore.google.com"]);
  try {
    for (const [index, row] of rows.entries()) {
      let result;
      try {
        const candidate = row as { name?: string; originalUrl?: string };
        const name = typeof candidate.name === "string" ? slugify(candidate.name) : "";
        const domain = typeof candidate.originalUrl === "string" ? domainFromUrl(candidate.originalUrl) : "";
        const key = shared.has(domain) ? `${domain}${new URL(candidate.originalUrl!).pathname.replace(/\/$/, "")}` : domain;
        if ((name && names.has(name)) || (key && urls.has(key))) result = { status: "duplicate-input" };
        else {
          result = await importBatchCandidate(database, row, publish, !apply);
          if (!["invalid", "error"].includes(result.status)) { names.add(name); urls.add(key); }
        }
      }
      catch (error) { result = { status: "error", error: error instanceof Error ? error.message : "Importfehler" }; }
      if (["invalid", "error"].includes(result.status)) process.exitCode = 1;
      fs.appendFileSync(report, JSON.stringify({ at: new Date().toISOString(), index, mode: apply ? "apply" : "dry-run", ...result }) + "\n");
      console.log(index + 1, result.status);
    }
  } finally { client.close(); }
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
