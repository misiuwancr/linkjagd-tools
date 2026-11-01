import { and, eq } from "drizzle-orm";
import type { AppDatabase } from "@/db/client";
import { tools } from "@/db/schema";

export async function writeAllowIndex(database: AppDatabase, toolId: string, allow: boolean) {
  await database.update(tools).set({ allowIndex: allow }).where(eq(tools.id, toolId));
}

export async function indexablePublished(database: AppDatabase) {
  return database
    .select({ slug: tools.slug, updatedAt: tools.updatedAt })
    .from(tools)
    .where(and(eq(tools.publishStatus, "published"), eq(tools.isExample, false), eq(tools.allowIndex, true)));
}
