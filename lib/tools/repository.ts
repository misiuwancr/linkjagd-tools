import { and, or, asc, desc, eq, inArray, like, sql, type SQL } from "drizzle-orm";
import {
  affiliatePrograms,
  categories,
  clickDaily,
  newsPosts,
  newsletterSubscribers,
  siteSettings,
  tags,
  toolCategories,
  tools,
  toolTags,
  type AffiliateProgram,
  type Tool,
} from "@/db/schema";
import type { AppDatabase } from "@/db/client";
import { normalizeSearch, slugify } from "@/lib/utils";
import { publicListQuery, type ToolListQuery } from "@/lib/tools/query";
import type { PublicCategory, PublicTag } from "@/lib/tools/public";
import { weeklyPopularVisible } from "@/lib/tools/popular";
import { companiesForTools, companyBySlug, type CompanyToolRef } from "@/lib/companies";
import { editorialStarterSlugs, starterRank } from "@/lib/editorial-selection";
import { emptyEditorial, linkjagdAssignmentSql, publicationSql, readEditorialBatch, type ToolEditorial } from "@/lib/tool-editorial";
import { contextClickInsert, type CtaPosition } from "@/lib/affiliate/context";

export type ToolWithRelations = Tool & {
  categories: PublicCategory[];
  tags: PublicTag[];
  programs: AffiliateProgram[];
  editorial: ToolEditorial;
};

function filters(query: ToolListQuery): SQL[] {
  const parts: SQL[] = [];
  if (query.status !== "all") parts.push(eq(tools.publishStatus, query.status));
  if (query.featuredOnly) parts.push(or(eq(tools.featured, true), inArray(tools.slug, [...editorialStarterSlugs]))!);
  if (query.rankedOnly) parts.push(sql`${tools.editorialRank} is not null`);
  if (query.excludeExamples) parts.push(eq(tools.isExample, false));
  if (query.manualRecommendationsOnly) parts.push(eq(tools.featured, true));
  if (query.linkjagdOnly || query.linkjagdVideo || query.videoSearch) parts.push(linkjagdAssignmentSql(query.linkjagdVideo, query.videoSearch));
  if (query.datedOnly) parts.push(sql`julianday(${publicationSql}) <= julianday('now')`);
  if (query.partnerGap) {
    parts.push(sql`${tools.id} in (
      select tool_id from affiliate_programs
      where program_presence = 'yes'
        and (affiliate_url is null or affiliate_url = '')
        and is_active = 0
    )`);
  }
  if (query.pricing) parts.push(eq(tools.pricingModel, query.pricing));
  if (query.license) parts.push(eq(tools.licenseType, query.license));
  const terms = normalizeSearch(query.q).split(/\s+/).filter(Boolean).slice(0, 12);
  // Existing search indexes may be truncated. Search the actual descriptions too,
  // without rewriting any production rows or requiring a second search service.
  const description = sql`replace(replace(replace(replace(lower(${tools.name} || ' ' || ${tools.shortDescriptionDe} || ' ' || ${tools.longDescriptionDe}), 'ä', 'ae'), 'ö', 'oe'), 'ü', 'ue'), 'ß', 'ss')`;
  for (const term of terms) parts.push(or(like(tools.searchText, `%${term}%`), sql`${description} like ${`%${term}%`}`)!);
  const selectedCategories = query.categorySlugs?.length ? query.categorySlugs : query.categorySlug ? [query.categorySlug] : [];
  if (selectedCategories.length) {
    parts.push(sql`${tools.id} in (
      select tc.tool_id from tool_categories tc
      inner join categories c on c.id = tc.category_id
      where c.slug in (${sql.join(selectedCategories.map((slug) => sql`${slug}`), sql`, `)})
    )`);
  }
  if (query.discoverySources.length > 0) {
    parts.push(inArray(tools.discoverySource, query.discoverySources));
  }
  if (query.germanUi) parts.push(eq(tools.germanUi, query.germanUi));
  if (query.noSignup) parts.push(eq(tools.noSignup, query.noSignup));
  if (query.fromVideo) {
    parts.push(sql`(
      coalesce(${tools.tiktokUrl}, '') != ''
      or coalesce(${tools.instagramReelUrl}, '') != ''
      or coalesce(${tools.youtubeShortUrl}, '') != ''
    )`);
  }
  if (query.company) parts.push(companySql(query.company));
  return parts;
}

function companySql(slug: string): SQL {
  const company = companyBySlug(slug);
  if (!company) return sql`0`;
  const parts: SQL[] = [];
  for (const suffix of company.suffixes) {
    parts.push(sql`${tools.domain} = ${suffix} or ${tools.domain} like ${`%.${suffix}`}`);
  }
  for (const exact of company.exact) parts.push(sql`${tools.domain} = ${exact}`);
  for (const toolSlug of company.toolSlugs) parts.push(sql`${tools.slug} = ${toolSlug}`);
  if (parts.length === 0) return sql`0`;
  let clause = sql`(${sql.join(parts, sql` or `)})`;
  for (const denied of company.deny) {
    clause = sql`(${clause} and ${tools.domain} != ${denied} and ${tools.domain} not like ${`%.${denied}`})`;
  }
  return clause;
}

function orderBy(query: ToolListQuery) {
  const clicks = sql`(select coalesce(sum(count), 0) from click_daily where tool_id = ${tools.id})`;
  if (query.sort === "oldest") return [asc(tools.createdAt), asc(tools.id)];
  if (query.sort === "alpha") return [sql`lower(${tools.name})`, asc(tools.id)];
  if (query.sort === "freeFirst") {
    return [sql`case ${tools.pricingModel} when 'free' then 0 when 'freemium' then 1 else 2 end`, desc(tools.createdAt), asc(tools.id)];
  }
  if (query.sort === "popular") return [desc(clicks), desc(tools.createdAt), asc(tools.id)];
  if (query.sort === "featured" || query.rankedOnly) {
    return [
      sql`case when ${tools.editorialRank} is null then 1 else 0 end`,
      asc(tools.editorialRank),
      desc(tools.featured),
      starterOrder(),
      desc(tools.createdAt),
      asc(tools.id),
    ];
  }
  return [sql`case when julianday(${publicationSql}) <= julianday('now') then 0 else 1 end`, sql`julianday(${publicationSql}) desc`, asc(tools.id)];
}

function starterOrder() {
  return sql`case ${tools.slug} ${sql.join(editorialStarterSlugs.map((slug, index) => sql`when ${slug} then ${index + 1}`), sql` `)} else 999 end`;
}

export async function attachRelations(
  database: AppDatabase,
  rows: Tool[],
): Promise<ToolWithRelations[]> {
  if (rows.length === 0) return [];
  const ids = rows.map((row) => row.id);
  const [categoryRows, tagRows, programs, editorial] = await Promise.all([
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
    readEditorialBatch(database, ids),
  ]);

  return rows.map((row) => ({
    ...row,
    editorial: editorial.get(row.id) ?? emptyEditorial(),
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
        eq(tools.isExample, false),
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

export async function listWeeklyPopular(database: AppDatabase, sinceDay: string, limit = 6) {
  const ranked = await database
    .select({
      toolId: clickDaily.toolId,
      total: sql<number>`coalesce(sum(${clickDaily.count}), 0)`,
    })
    .from(clickDaily)
    .where(sql`${clickDaily.day} >= ${sinceDay}`)
    .groupBy(clickDaily.toolId)
    .orderBy(sql`coalesce(sum(${clickDaily.count}), 0) desc`)
    .limit(limit);
  const clicks = ranked.reduce((sum, row) => sum + Number(row.total), 0);
  if (!weeklyPopularVisible(clicks)) return [];
  const ids = ranked.map((row) => row.toolId);
  const rows = await database
    .select()
    .from(tools)
    .where(and(inArray(tools.id, ids), eq(tools.publishStatus, "published"), eq(tools.isExample, false)));
  const byId = new Map(rows.map((row) => [row.id, row]));
  const ordered = ids.flatMap((id) => {
    const row = byId.get(id);
    return row ? [row] : [];
  });
  return attachRelations(database, ordered);
}

export async function listAlternativePool(database: AppDatabase, tool: ToolWithRelations, limit = 24) {
  if (tool.categories.length === 0) return [];
  const slugs = tool.categories.map((category) => category.slug);
  const rows = await database
    .select()
    .from(tools)
    .where(
      and(
        eq(tools.publishStatus, "published"),
        eq(tools.isExample, false),
        sql`${tools.id} != ${tool.id}`,
        sql`${tools.id} in (
          select tc.tool_id from tool_categories tc
          inner join categories c on c.id = tc.category_id
          where c.slug in (${sql.join(slugs.map((slug) => sql`${slug}`), sql`, `)})
        )`,
      ),
    )
    .orderBy(desc(tools.featured), asc(tools.name))
    .limit(limit);
  return attachRelations(database, rows);
}

export async function listClickStats(database: AppDatabase, since7: string, since30: string) {
  const rows = await database
    .select({
      id: tools.id,
      name: tools.name,
      slug: tools.slug,
      days7: sql<number>`(select coalesce(sum(c.count), 0) from click_daily c where c.tool_id = ${tools.id} and c.day >= ${since7})`,
      days30: sql<number>`(select coalesce(sum(c.count), 0) from click_daily c where c.tool_id = ${tools.id} and c.day >= ${since30})`,
      programPresence: sql<string>`(select coalesce(max(a.program_presence), 'unknown') from affiliate_programs a where a.tool_id = ${tools.id})`,
    })
    .from(tools)
    .where(and(eq(tools.publishStatus, "published"), eq(tools.isExample, false)))
    .groupBy(tools.id, tools.name, tools.slug);
  return rows.map((row) => ({
    ...row,
    days7: Number(row.days7),
    days30: Number(row.days30),
  }));
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
    .where(and(eq(tools.publishStatus, "published"), eq(tools.isExample, false)))
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
    12000,
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
    let existing = await database.select().from(tags).where(eq(tags.slug, slug)).limit(1);
    let tagId = existing[0]?.id ?? crypto.randomUUID();
    if (!existing[0]) {
      try {
        await database.insert(tags).values({ id: tagId, name, slug });
      } catch {
        existing = await database.select().from(tags).where(eq(tags.slug, slug)).limit(1);
        if (!existing[0]) throw new Error(`Schlagwort ${slug} konnte nicht gespeichert werden.`);
        tagId = existing[0].id;
      }
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

const sharedHosts = new Set([
  "github.com",
  "gitlab.com",
  "invent.kde.org",
  "huggingface.co",
  "apps.apple.com",
  "chromewebstore.google.com",
]);

export async function findDuplicateTool(
  database: AppDatabase,
  domain: string,
  slug: string,
  originalUrl: string,
) {
  const bySlug = await database.select().from(tools).where(eq(tools.slug, slug)).limit(1);
  if (bySlug[0]) return { ...bySlug[0], duplicate: "slug" as const };
  const byDomain = await database.select().from(tools).where(eq(tools.domain, domain));
  if (!sharedHosts.has(domain)) {
    return byDomain[0] ? { ...byDomain[0], duplicate: "domain" as const } : null;
  }
  let path = "/";
  try {
    path = new URL(originalUrl).pathname.replace(/\/$/, "") || "/";
  } catch {
    return byDomain[0] ? { ...byDomain[0], duplicate: "domain" as const } : null;
  }
  const hit = byDomain.find((row) => {
    try {
      return (new URL(row.originalUrl).pathname.replace(/\/$/, "") || "/") === path;
    } catch {
      return false;
    }
  });
  return hit ? { ...hit, duplicate: "domain" as const } : null;
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
    input: { toolId: string; programId: string | null; kind: "affiliate" | "official"; day: string; source?: string; position?: CtaPosition },
) {
  const programSlot = input.kind === "affiliate" ? input.programId || "" : "";
  const total = database
    .insert(clickDaily)
    .values({
      toolId: input.toolId,
      programSlot,
      targetKind: input.kind,
      day: input.day,
      count: 1,
    })
    .onConflictDoUpdate({
      target: [clickDaily.toolId, clickDaily.targetKind, clickDaily.day, clickDaily.programSlot],
      set: { count: sql`${clickDaily.count} + 1` },
    });
  if (input.source && input.position) {
    await database.batch([total, contextClickInsert(database, { ...input, source: input.source, position: input.position })]);
  } else await total;
}

export async function listPublishedNews(database: AppDatabase, limit = 6, offset = 0) {
  return database
    .select()
    .from(newsPosts)
    .where(eq(newsPosts.status, "published"))
    .orderBy(desc(newsPosts.publishedAt), asc(newsPosts.id))
    .limit(limit)
    .offset(offset);
}

export async function publishedBlogSlugs(database: AppDatabase) {
  return database.select({ slug: newsPosts.slug, updatedAt: newsPosts.updatedAt }).from(newsPosts)
    .where(eq(newsPosts.status, "published")).orderBy(asc(newsPosts.slug));
}

export async function publishedBlogCount(database: AppDatabase) {
  const rows = await database.select({ total: sql<number>`count(*)` }).from(newsPosts).where(eq(newsPosts.status, "published"));
  return Number(rows[0]?.total ?? 0);
}

export async function publishedSlugs(database: AppDatabase) {
  return database
    .select({ slug: tools.slug, updatedAt: tools.updatedAt })
    .from(tools)
    .where(and(eq(tools.publishStatus, "published"), eq(tools.isExample, false)));
}

export async function dashboardCounts(database: AppDatabase) {
  const [grouped, categoryRow, moderationRow, withoutCta] = await Promise.all([
    database
      .select({ status: tools.publishStatus, total: sql<number>`count(*)` })
      .from(tools)
      .groupBy(tools.publishStatus),
    database.select({ total: sql<number>`count(*)` }).from(categories),
    database
      .select({ total: sql<number>`count(*)` })
      .from(tools)
      .where(
        and(eq(tools.publishStatus, "draft"), inArray(tools.discoverySource, ["import", "submission", "futuretools-top100"])),
      ),
    database
      .select({ total: sql<number>`count(*)` })
      .from(tools)
      .where(
        and(
          eq(tools.publishStatus, "published"),
          sql`not exists (
            select 1 from affiliate_programs
            where affiliate_programs.tool_id = ${tools.id}
              and affiliate_programs.is_active = 1
              and affiliate_programs.status = 'active'
              and affiliate_programs.affiliate_url is not null
              and affiliate_programs.affiliate_url != ''
          )`,
        ),
      ),
  ]);
  const byStatus = new Map(grouped.map((row) => [row.status, Number(row.total)]));
  return {
    published: byStatus.get("published") ?? 0,
    drafts: byStatus.get("draft") ?? 0,
    archived: byStatus.get("archived") ?? 0,
    categories: Number(categoryRow[0]?.total ?? 0),
    moderation: Number(moderationRow[0]?.total ?? 0),
    publishedWithoutCta: Number(withoutCta[0]?.total ?? 0),
  };
}

export async function listTopTools(database: AppDatabase, limit = 20) {
  const rows = await database
    .select()
    .from(tools)
    .where(and(eq(tools.publishStatus, "published"), eq(tools.isExample, false), sql`${tools.editorialRank} is not null`))
    .orderBy(asc(tools.editorialRank), asc(tools.name))
    .limit(limit);
  if (rows.length > 0) return attachRelations(database, rows);
  // Nur wenn noch keine Datenbank-Rangliste besteht: explizite redaktionelle Startauswahl.
  const starter = await database.select().from(tools)
    .where(and(eq(tools.publishStatus, "published"), eq(tools.isExample, false), inArray(tools.slug, [...editorialStarterSlugs])))
    .orderBy(starterOrder()).limit(limit);
  return attachRelations(database, starter.map((tool) => ({ ...tool, editorialRank: starterRank(tool.slug) })));
}

export async function listHomepageFresh(database: AppDatabase, limit = 6) {
  return (await listTools(database, publicListQuery({}, { datedOnly: true, pageSize: limit }))).items;
}

export async function totalClicks(database: AppDatabase) {
  const rows = await database.select({ total: sql<number>`coalesce(sum(count), 0)` }).from(clickDaily);
  return Number(rows[0]?.total ?? 0);
}

export async function getNewsBySlug(database: AppDatabase, slug: string) {
  const rows = await database.select().from(newsPosts).where(eq(newsPosts.slug, slug)).limit(1);
  return rows[0] ?? null;
}

export async function listAllNews(database: AppDatabase) {
  return database.select().from(newsPosts).orderBy(desc(newsPosts.updatedAt));
}

export async function getSetting(database: AppDatabase, key: string) {
  const rows = await database.select().from(siteSettings).where(eq(siteSettings.key, key)).limit(1);
  return rows[0]?.value ?? "";
}

export async function setSetting(database: AppDatabase, key: string, value: string) {
  await database
    .insert(siteSettings)
    .values({ key, value })
    .onConflictDoUpdate({ target: siteSettings.key, set: { value } });
}

export async function listCompaniesInDirectory(database: AppDatabase) {
  const rows = await database
    .select({ slug: tools.slug, domain: tools.domain })
    .from(tools)
    .where(and(eq(tools.publishStatus, "published"), eq(tools.isExample, false)));
  return companiesForTools(rows satisfies CompanyToolRef[]);
}

export async function socialProofText(database: AppDatabase) {
  const stored = (await getSetting(database, "social_proof")).trim();
  if (stored) return stored;
  return (process.env.NEXT_PUBLIC_SOCIAL_PROOF || "").trim();
}

export async function listSubscribers(database: AppDatabase) {
  return database.select().from(newsletterSubscribers).orderBy(desc(newsletterSubscribers.createdAt));
}
