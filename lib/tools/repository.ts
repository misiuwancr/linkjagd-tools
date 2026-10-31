import { and, asc, desc, eq, inArray, like, sql, type SQL } from "drizzle-orm";
import {
  affiliatePrograms,
  categories,
  clickDaily,
  newsPosts,
  tags,
  toolCategories,
  tools,
  toolTags,
  type AffiliateProgram,
  type Tool,
} from "@/db/schema";
import type { AppDatabase } from "@/db/client";
import { normalizeSearch, slugify } from "@/lib/utils";
import type { ToolListQuery } from "@/lib/tools/query";
import type { PublicCategory, PublicTag } from "@/lib/tools/public";

export type ToolWithRelations = Tool & {
  categories: PublicCategory[];
  tags: PublicTag[];
  programs: AffiliateProgram[];
};

function filters(query: ToolListQuery): SQL[] {
  const parts: SQL[] = [];
  if (query.status !== "all") parts.push(eq(tools.publishStatus, query.status));
  if (query.featuredOnly) parts.push(eq(tools.featured, true));
  if (query.rankedOnly) parts.push(sql`${tools.editorialRank} is not null`);
  if (query.pricing) parts.push(eq(tools.pricingModel, query.pricing));
  const needle = normalizeSearch(query.q);
  if (needle) parts.push(like(tools.searchText, `%${needle}%`));
  if (query.categorySlug) {
    parts.push(sql`${tools.id} in (
      select tc.tool_id from tool_categories tc
      inner join categories c on c.id = tc.category_id
      where c.slug = ${query.categorySlug}
    )`);
  }
  if (query.discoverySources.length > 0) {
    parts.push(inArray(tools.discoverySource, query.discoverySources));
  }
  return parts;
}

function orderBy(query: ToolListQuery) {
  const clicks = sql`(select coalesce(sum(count), 0) from click_daily where tool_id = ${tools.id})`;
  if (query.sort === "alpha") return [asc(tools.name)];
  if (query.sort === "popular") return [desc(clicks), desc(tools.createdAt)];
  if (query.sort === "featured" || query.rankedOnly) {
    return [
      sql`case when ${tools.editorialRank} is null then 1 else 0 end`,
      asc(tools.editorialRank),
      desc(tools.featured),
      desc(tools.createdAt),
    ];
  }
  return [desc(tools.createdAt)];
}

export async function attachRelations(
  database: AppDatabase,
  rows: Tool[],
): Promise<ToolWithRelations[]> {
  if (rows.length === 0) return [];
  const ids = rows.map((row) => row.id);
  const [categoryRows, tagRows, programs] = await Promise.all([
    database
      .select({
        toolId: toolCategories.toolId,
        name: categories.name,
        slug: categories.slug,
      })
      .from(toolCategories)
      .innerJoin(categories, eq(toolCategories.categoryId, categories.id))
      .where(inArray(toolCategories.toolId, ids)),
    database
      .select({
        toolId: toolTags.toolId,
        name: tags.name,
        slug: tags.slug,
      })
      .from(toolTags)
      .innerJoin(tags, eq(toolTags.tagId, tags.id))
      .where(inArray(toolTags.toolId, ids)),
    database.select().from(affiliatePrograms).where(inArray(affiliatePrograms.toolId, ids)),
  ]);

  return rows.map((row) => ({
    ...row,
    categories: categoryRows
      .filter((item) => item.toolId === row.id)
      .map(({ name, slug }) => ({ name, slug })),
    tags: tagRows
      .filter((item) => item.toolId === row.id)
      .map(({ name, slug }) => ({ name, slug })),
    programs: programs.filter((item) => item.toolId === row.id),
  }));
}

export async function listTools(database: AppDatabase, query: ToolListQuery) {
  const where = and(...filters(query));
  const totalRow = await database
    .select({ total: sql<number>`count(*)` })
    .from(tools)
    .where(where);
  const total = Number(totalRow[0]?.total ?? 0);
  const pages = Math.max(1, Math.ceil(total / query.pageSize));
  const page = Math.min(query.page, pages);
  const rows = await database
    .select()
    .from(tools)
    .where(where)
    .orderBy(...orderBy(query))
    .limit(query.pageSize)
    .offset((page - 1) * query.pageSize);
  return { total, page, items: await attachRelations(database, rows) };
}

export async function getToolBySlug(database: AppDatabase, slug: string) {
  const rows = await database.select().from(tools).where(eq(tools.slug, slug)).limit(1);
  const [tool] = await attachRelations(database, rows);
  return tool ?? null;
}

export async function getToolById(database: AppDatabase, id: string) {
  const rows = await database.select().from(tools).where(eq(tools.id, id)).limit(1);
  const [tool] = await attachRelations(database, rows);
  return tool ?? null;
}

export async function listSimilar(database: AppDatabase, tool: ToolWithRelations, limit = 4) {
  if (tool.categories.length === 0) return [];
  const slugs = tool.categories.map((category) => category.slug);
  const rows = await database
    .select()
    .from(tools)
    .where(
      and(
        eq(tools.publishStatus, "published"),
        sql`${tools.id} != ${tool.id}`,
        sql`${tools.id} in (
          select tc.tool_id from tool_categories tc
          inner join categories c on c.id = tc.category_id
          where c.slug in (${sql.join(slugs.map((slug) => sql`${slug}`), sql`, `)})
        )`,
      ),
    )
    .orderBy(desc(tools.featured), desc(tools.createdAt))
    .limit(limit);
  return attachRelations(database, rows);
}

export async function listCategories(database: AppDatabase) {
  const rows = await database.select().from(categories).orderBy(asc(categories.sortOrder), asc(categories.name));
  const counts = await database
    .select({
      categoryId: toolCategories.categoryId,
      total: sql<number>`count(*)`,
    })
    .from(toolCategories)
    .innerJoin(tools, eq(toolCategories.toolId, tools.id))
    .where(eq(tools.publishStatus, "published"))
    .groupBy(toolCategories.categoryId);
  const countById = new Map(counts.map((row) => [row.categoryId, Number(row.total)]));
  return rows.map((category) => ({ ...category, toolCount: countById.get(category.id) ?? 0 }));
}

export async function getCategoryBySlug(database: AppDatabase, slug: string) {
  const rows = await database.select().from(categories).where(eq(categories.slug, slug)).limit(1);
  return rows[0] ?? null;
}

export function buildSearchText(input: {
  name: string;
  shortDescriptionDe: string;
  longDescriptionDe: string;
  categories: string[];
  tags: string[];
}) {
  return normalizeSearch(
    [input.name, input.shortDescriptionDe, input.longDescriptionDe, ...input.categories, ...input.tags].join(" "),
  );
}

export async function replaceCategories(database: AppDatabase, toolId: string, categoryIds: string[]) {
  await database.delete(toolCategories).where(eq(toolCategories.toolId, toolId));
  const unique = [...new Set(categoryIds)];
  if (unique.length === 0) return;
  await database.insert(toolCategories).values(unique.map((categoryId) => ({ toolId, categoryId })));
}

export async function replaceTags(database: AppDatabase, toolId: string, names: string[]) {
  await database.delete(toolTags).where(eq(toolTags.toolId, toolId));
  const unique = [...new Set(names.map((name) => name.trim()).filter(Boolean))];
  for (const name of unique) {
    const slug = slugify(name);
    if (!slug) continue;
    const existing = await database.select().from(tags).where(eq(tags.slug, slug)).limit(1);
    const tagId = existing[0]?.id ?? crypto.randomUUID();
    if (!existing[0]) {
      await database.insert(tags).values({ id: tagId, name, slug });
    }
    await database.insert(toolTags).values({ toolId, tagId });
  }
}

export async function refreshSearchText(database: AppDatabase, toolId: string) {
  const tool = await getToolById(database, toolId);
  if (!tool) return;
  await database
    .update(tools)
    .set({
      searchText: buildSearchText({
        name: tool.name,
        shortDescriptionDe: tool.shortDescriptionDe,
        longDescriptionDe: tool.longDescriptionDe,
        categories: tool.categories.map((category) => category.name),
        tags: tool.tags.map((tag) => tag.name),
      }),
    })
    .where(eq(tools.id, toolId));
}

export async function findByDomainOrSlug(database: AppDatabase, domain: string, slug: string) {
  const rows = await database
    .select()
    .from(tools)
    .where(sql`${tools.domain} = ${domain} or ${tools.slug} = ${slug}`)
    .limit(1);
  return rows[0] ?? null;
}

export async function recordClick(
  database: AppDatabase,
  input: { toolId: string; programId: string; day: string },
) {
  await database
    .insert(clickDaily)
    .values({ ...input, count: 1 })
    .onConflictDoUpdate({
      target: [clickDaily.toolId, clickDaily.programId, clickDaily.day],
      set: { count: sql`${clickDaily.count} + 1` },
    });
}

export async function listPublishedNews(database: AppDatabase, limit = 6) {
  return database
    .select()
    .from(newsPosts)
    .where(eq(newsPosts.status, "published"))
    .orderBy(desc(newsPosts.publishedAt))
    .limit(limit);
}

export async function publishedSlugs(database: AppDatabase) {
  return database
    .select({ slug: tools.slug, updatedAt: tools.updatedAt })
    .from(tools)
    .where(eq(tools.publishStatus, "published"));
}

export async function dashboardCounts(database: AppDatabase) {
  const [toolRows, categoryRows, draftRows] = await Promise.all([
    database.select().from(tools),
    database.select().from(categories),
    database
      .select()
      .from(tools)
      .where(
        and(eq(tools.publishStatus, "draft"), inArray(tools.discoverySource, ["import", "submission"])),
      ),
  ]);
  const published = toolRows.filter((tool) => tool.publishStatus === "published");
  const programs = published.length
    ? await database
        .select()
        .from(affiliatePrograms)
        .where(inArray(affiliatePrograms.toolId, published.map((tool) => tool.id)))
    : [];
  const withCta = new Set(
    programs.filter((program) => program.isActive && program.status === "active" && program.affiliateUrl).map((program) => program.toolId),
  );
  return {
    published: published.length,
    drafts: toolRows.filter((tool) => tool.publishStatus === "draft").length,
    archived: toolRows.filter((tool) => tool.publishStatus === "archived").length,
    categories: categoryRows.length,
    moderation: draftRows.length,
    publishedWithoutCta: published.filter((tool) => !withCta.has(tool.id)).length,
  };
}
