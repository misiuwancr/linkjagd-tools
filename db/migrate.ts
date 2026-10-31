import fs from "fs";
import path from "path";
import { createClient, type Client } from "@libsql/client";
import { resolveAppDatabase } from "./resolve";

function statements(sql: string) {
  return sql
    .split(/;\s*(?:\n|$)/)
    .map((part) => part.trim())
    .filter((part) => part.length > 0);
}

export async function applyMigrations(client: Client) {
  await client.execute("PRAGMA foreign_keys = ON");
  await client.execute(
    `CREATE TABLE IF NOT EXISTS schema_migrations (
      id text PRIMARY KEY NOT NULL,
      applied_at integer NOT NULL
    )`,
  );
  const dir = path.join(process.cwd(), "migrations");
  const files = fs
    .readdirSync(dir)
    .filter((file) => file.endsWith(".sql"))
    .sort();
  const applied = await client.execute("SELECT id FROM schema_migrations");
  const done = new Set(applied.rows.map((row) => String(row.id)));

  for (const file of files) {
    if (done.has(file)) continue;
    const sql = fs.readFileSync(path.join(dir, file), "utf8");
    for (const statement of statements(sql)) {
      await client.execute(statement);
    }
    await client.execute({
      sql: "INSERT INTO schema_migrations (id, applied_at) VALUES (?, ?)",
      args: [file, Date.now()],
    });
  }
}

async function main() {
  const target = resolveAppDatabase();
  if (target.kind === "file") {
    const filePath = target.url.slice("file:".length).replace(/^\/\//, "");
    fs.mkdirSync(path.dirname(path.resolve(filePath)), { recursive: true });
  }
  const client = createClient({ url: target.url, authToken: target.authToken });
  await applyMigrations(client);
  console.log(target.kind === "turso" ? "Migrationen auf Turso angewendet." : "Migrationen angewendet.");
}

if (process.argv[1] && process.argv[1].includes("migrate.ts")) {
  import("dotenv/config").then(() => main());
}
