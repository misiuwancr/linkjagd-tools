import fs from "fs";
import path from "path";
import { createClient } from "@libsql/client";
import { drizzle, type LibSQLDatabase } from "drizzle-orm/libsql";
import * as schema from "./schema";
import { applyMigrations } from "./migrate";
import { resolveAppDatabase } from "./resolve";

export type AppDatabase = LibSQLDatabase<typeof schema>;

let ready: Promise<AppDatabase> | null = null;

async function init(): Promise<AppDatabase> {
  const target = resolveAppDatabase();
  if (target.kind === "file") {
    const relative = target.url.slice("file:".length).replace(/^\/\//, "");
    const absolute = path.resolve(relative);
    fs.mkdirSync(path.dirname(absolute), { recursive: true });
  }
  const client = createClient({ url: target.url, authToken: target.authToken });
  await client.execute("PRAGMA foreign_keys = ON");
  if (target.kind === "file") {
    await client.execute("PRAGMA journal_mode = WAL");
  }
  await applyMigrations(client);
  return drizzle(client, { schema });
}

export function getDb() {
  if (!ready) ready = init();
  return ready;
}
