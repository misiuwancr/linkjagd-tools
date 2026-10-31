import "dotenv/config";
import fs from "fs";
import path from "path";
import { createClient } from "@libsql/client";
import { DATA_TABLES, publicExportRow } from "@/db/transfer";
import { resolveLocalDatabase } from "@/db/resolve";

export async function exportLocalDatabase(outDir = path.join(process.cwd(), "data", "export")) {
  const local = resolveLocalDatabase();
  const client = createClient({ url: local.url });
  fs.mkdirSync(outDir, { recursive: true });
  const counts: Record<string, number> = {};
  for (const table of DATA_TABLES) {
    const result = await client.execute(`select * from ${table}`);
    const rows = result.rows.map((row) => publicExportRow(table, row as Record<string, unknown>));
    if (table === "users" && rows.some((row) => "password_hash" in row)) {
      throw new Error("Export enthält ein Passwort-Hash. Abbruch.");
    }
    counts[table] = rows.length;
    fs.writeFileSync(path.join(outDir, `${table}.json`), `${JSON.stringify(rows, null, 2)}\n`);
  }
  const manifest = {
    exportedAt: new Date().toISOString(),
    source: "local-sqlite",
    counts,
    omitted: ["users.password_hash"],
    note: "Keine Zugangsdaten. Alternativen, Aufgabenseiten und Kategorietexte liegen im Code, nicht in diesen Dateien.",
  };
  fs.writeFileSync(path.join(outDir, "manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`);
  return manifest;
}

if (process.argv[1]?.includes("export-database.ts")) {
  exportLocalDatabase()
    .then((manifest) => {
      console.log(JSON.stringify(manifest.counts));
    })
    .catch((error) => {
      console.error(error instanceof Error ? error.message : error);
      process.exit(1);
    });
}
