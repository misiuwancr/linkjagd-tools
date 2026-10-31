import "dotenv/config";
import { createClient, type Client, type InValue } from "@libsql/client";
import { applyMigrations } from "@/db/migrate";
import { resolveLocalDatabase } from "@/db/resolve";
import { DATA_TABLES, sqlCell } from "@/db/transfer";
import { exportLocalDatabase } from "./export-database";

const CHUNK = 40;

async function columns(client: Client, table: string) {
  const info = await client.execute(`pragma table_info(${table})`);
  return info.rows.map((row) => String(row.name));
}

async function readRows(client: Client, table: string) {
  const result = await client.execute(`select * from ${table}`);
  return result.rows.map((row) => ({ ...row }) as Record<string, unknown>);
}

async function replaceTable(remote: Client, table: string, rows: Record<string, unknown>[], cols: string[]) {
  await remote.execute(`delete from ${table}`);
  for (let offset = 0; offset < rows.length; offset += CHUNK) {
    const slice = rows.slice(offset, offset + CHUNK);
    const statements = slice.map((row) => {
      const placeholders = cols.map(() => "?").join(", ");
      return {
        sql: `insert into ${table} (${cols.join(", ")}) values (${placeholders})`,
        args: cols.map((column) => sqlCell(row[column]) as InValue),
      };
    });
    if (statements.length > 0) await remote.batch(statements, "write");
  }
}

async function main() {
  const manifest = await exportLocalDatabase();
  const tursoUrl = process.env.TURSO_DATABASE_URL?.trim() ?? "";
  const authToken = process.env.TURSO_AUTH_TOKEN?.trim() ?? "";
  if (!tursoUrl || !authToken) {
    console.error(
      "Export liegt in data/export. Übertragung übersprungen: TURSO_DATABASE_URL und TURSO_AUTH_TOKEN setzen, dann npm run db:push-remote erneut ausführen.",
    );
    process.exit(1);
  }
  if (!/^libsql:\/\//.test(tursoUrl) && !/^https:\/\//.test(tursoUrl)) {
    throw new Error("TURSO_DATABASE_URL muss mit libsql:// oder https:// beginnen.");
  }
  const local = resolveLocalDatabase();
  const source = createClient({ url: local.url });
  const remote = createClient({ url: tursoUrl, authToken });
  await applyMigrations(remote);
  await remote.execute("PRAGMA foreign_keys = OFF");
  const counts: Record<string, number> = {};
  for (const table of [...DATA_TABLES].reverse()) {
    await remote.execute(`delete from ${table}`);
  }
  for (const table of DATA_TABLES) {
    const cols = await columns(source, table);
    const rows = await readRows(source, table);
    await replaceTable(remote, table, rows, cols);
    counts[table] = rows.length;
  }
  await remote.execute("PRAGMA foreign_keys = ON");
  console.log(JSON.stringify({ exported: manifest.counts, remote: counts }));
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
