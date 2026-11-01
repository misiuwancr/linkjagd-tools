import { createClient } from "@libsql/client";
import type { AppDatabase } from "@/db/client";
import { resolveAppDatabase } from "@/db/resolve";
import { sql } from "drizzle-orm";
import { tools } from "@/db/schema";
import { and, eq } from "drizzle-orm";

let cached: boolean | null = null;

export async function allowIndexColumnExists() {
  if (cached !== null) return cached;
  const target = resolveAppDatabase();
  const client = createClient({ url: target.url, authToken: target.authToken });
  const info = await client.execute("select 1 as ok from pragma_table_info('tools') where name = 'allow_index'");
  cached = info.rows.length > 0;
  return cached;
}

export function resetAllowIndexCache() {
  cached = null;
}

export async function readAllowIndex(database: AppDatabase, toolId: string) {
  if (!(await allowIndexColumnExists())) return true;
  const rows = await database.all<{ allow_index: number }>(sql`select allow_index as allow_index from tools where id = ${toolId} limit 1`);
  const value = rows[0]?.allow_index;
  return value === undefined || value === null ? true : Number(value) === 1;
}

export async function writeAllowIndex(database: AppDatabase, toolId: string, allow: boolean) {
  if (!(await allowIndexColumnExists())) return false;
  await database.run(sql`update tools set allow_index = ${allow ? 1 : 0} where id = ${toolId}`);
  return true;
}

export async function indexablePublished(database: AppDatabase) {
  const base = and(eq(tools.publishStatus, "published"), eq(tools.isExample, false));
  if (!(await allowIndexColumnExists())) {
    return database.select({ slug: tools.slug, updatedAt: tools.updatedAt }).from(tools).where(base);
  }
  return database
    .select({ slug: tools.slug, updatedAt: tools.updatedAt })
    .from(tools)
    .where(and(base, sql`allow_index = 1`));
}
