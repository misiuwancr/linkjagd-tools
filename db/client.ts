import fs from "fs";
import path from "path";
import { createClient } from "@libsql/client";
import { drizzle, type LibSQLDatabase } from "drizzle-orm/libsql";
import * as schema from "./schema";
import { applyMigrations } from "./migrate";

export type AppDatabase = LibSQLDatabase<typeof schema>;

let ready: Promise<AppDatabase> | null = null;

async function init(): Promise<AppDatabase> {
  const url = process.env.DATABASE_URL;
  if (!url) {
    throw new Error("DATABASE_URL fehlt. Lege eine .env nach .env.example an.");
  }
  if (url.startsWith("file:")) {
    const relative = url.slice("file:".length).replace(/^\/\//, "");
    const absolute = path.resolve(relative);
    fs.mkdirSync(path.dirname(absolute), { recursive: true });
  }
  const client = createClient({ url });
  await client.execute("PRAGMA foreign_keys = ON");
  if (url.startsWith("file:")) {
    await client.execute("PRAGMA journal_mode = WAL");
  }
  await applyMigrations(client);
  return drizzle(client, { schema });
}

export function getDb() {
  if (!ready) ready = init();
  return ready;
}
