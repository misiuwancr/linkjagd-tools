import { relations } from "drizzle-orm";
import {
  index,
  integer,
  primaryKey,
  sqliteTable,
  text,
} from "drizzle-orm/sqlite-core";

export const publishStatuses = ["draft", "published", "archived"] as const;
export const pricingModels = ["free", "freemium", "paid", "open_source"] as const;
export const affiliateStatuses = [
  "none_found",
  "found",
  "application_pending",
  "approved",
  "active",
  "disabled",
] as const;
export const userRoles = ["admin", "editor"] as const;
export const newsStatuses = ["draft", "published"] as const;

export type PublishStatus = (typeof publishStatuses)[number];
export type PricingModel = (typeof pricingModels)[number];
export type AffiliateStatus = (typeof affiliateStatuses)[number];
export type UserRole = (typeof userRoles)[number];

const timestamp = (name: string) =>
  integer(name, { mode: "timestamp" }).notNull();

export const users = sqliteTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  passwordHash: text("password_hash").notNull(),
  role: text("role", { enum: userRoles }).notNull(),
  createdAt: timestamp("created_at"),
});

export const categories = sqliteTable("categories", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  slug: text("slug").notNull().unique(),
  description: text("description"),
  sortOrder: integer("sort_order").notNull().default(0),
  createdAt: timestamp("created_at"),
  updatedAt: timestamp("updated_at"),
});

export const tags = sqliteTable("tags", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  slug: text("slug").notNull().unique(),
});

export const tools = sqliteTable(
  "tools",
  {
    id: text("id").primaryKey(),
    name: text("name").notNull(),
    slug: text("slug").notNull().unique(),
    originalUrl: text("original_url").notNull(),
    domain: text("domain").notNull(),
    logo: text("logo"),
    shortDescriptionDe: text("short_description_de").notNull(),
    longDescriptionDe: text("long_description_de").notNull().default(""),
    featuresDe: text("features_de").notNull().default("[]"),
    screenshots: text("screenshots").notNull().default("[]"),
    pricingModel: text("pricing_model", { enum: pricingModels })
      .notNull()
      .default("freemium"),
    publishStatus: text("publish_status", { enum: publishStatuses })
      .notNull()
      .default("draft"),
    featured: integer("featured", { mode: "boolean" }).notNull().default(false),
    editorialRank: integer("editorial_rank"),
    discoverySource: text("discovery_source").notNull().default("manual"),
    isExample: integer("is_example", { mode: "boolean" }).notNull().default(false),
    searchText: text("search_text").notNull().default(""),
    internalNotes: text("internal_notes"),
    submitterEmail: text("submitter_email"),
    createdAt: timestamp("created_at"),
    updatedAt: timestamp("updated_at"),
  },
  (table) => ({
    domainIdx: index("tools_domain_idx").on(table.domain),
    statusIdx: index("tools_status_idx").on(table.publishStatus),
    createdIdx: index("tools_created_idx").on(table.createdAt),
    rankIdx: index("tools_rank_idx").on(table.editorialRank),
  }),
);

export const toolCategories = sqliteTable(
  "tool_categories",
  {
    toolId: text("tool_id")
      .notNull()
      .references(() => tools.id, { onDelete: "cascade" }),
    categoryId: text("category_id")
      .notNull()
      .references(() => categories.id, { onDelete: "cascade" }),
  },
  (table) => ({
    pk: primaryKey({ columns: [table.toolId, table.categoryId] }),
    categoryIdx: index("tool_categories_category_idx").on(table.categoryId),
  }),
);

export const toolTags = sqliteTable(
  "tool_tags",
  {
    toolId: text("tool_id")
      .notNull()
      .references(() => tools.id, { onDelete: "cascade" }),
    tagId: text("tag_id")
      .notNull()
      .references(() => tags.id, { onDelete: "cascade" }),
  },
  (table) => ({
    pk: primaryKey({ columns: [table.toolId, table.tagId] }),
  }),
);

export const affiliatePrograms = sqliteTable(
  "affiliate_programs",
  {
    id: text("id").primaryKey(),
    toolId: text("tool_id")
      .notNull()
      .references(() => tools.id, { onDelete: "cascade" }),
    affiliateUrl: text("affiliate_url"),
    network: text("network").notNull().default("manual"),
    partnerProgramId: text("partner_program_id"),
    status: text("status", { enum: affiliateStatuses }).notNull().default("none_found"),
    lastCheckedAt: integer("last_checked_at", { mode: "timestamp" }),
    priority: integer("priority").notNull().default(0),
    isActive: integer("is_active", { mode: "boolean" }).notNull().default(false),
    notes: text("notes"),
    createdAt: timestamp("created_at"),
    updatedAt: timestamp("updated_at"),
  },
  (table) => ({
    toolIdx: index("affiliate_tool_idx").on(table.toolId),
  }),
);

export const clickDaily = sqliteTable(
  "click_daily",
  {
    toolId: text("tool_id")
      .notNull()
      .references(() => tools.id, { onDelete: "cascade" }),
    programId: text("program_id")
      .notNull()
      .references(() => affiliatePrograms.id, { onDelete: "cascade" }),
    day: text("day").notNull(),
    count: integer("count").notNull().default(0),
  },
  (table) => ({
    pk: primaryKey({ columns: [table.toolId, table.programId, table.day] }),
  }),
);

export const newsPosts = sqliteTable("news_posts", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  slug: text("slug").notNull().unique(),
  excerpt: text("excerpt").notNull(),
  body: text("body").notNull().default(""),
  sourceName: text("source_name"),
  status: text("status", { enum: newsStatuses }).notNull().default("draft"),
  publishedAt: integer("published_at", { mode: "timestamp" }),
  createdAt: timestamp("created_at"),
  updatedAt: timestamp("updated_at"),
});

export const usersRelations = relations(users, () => ({}));

export const categoriesRelations = relations(categories, ({ many }) => ({
  toolCategories: many(toolCategories),
}));

export const tagsRelations = relations(tags, ({ many }) => ({
  toolTags: many(toolTags),
}));

export const toolsRelations = relations(tools, ({ many }) => ({
  toolCategories: many(toolCategories),
  toolTags: many(toolTags),
  programs: many(affiliatePrograms),
}));

export const toolCategoriesRelations = relations(toolCategories, ({ one }) => ({
  tool: one(tools, { fields: [toolCategories.toolId], references: [tools.id] }),
  category: one(categories, {
    fields: [toolCategories.categoryId],
    references: [categories.id],
  }),
}));

export const toolTagsRelations = relations(toolTags, ({ one }) => ({
  tool: one(tools, { fields: [toolTags.toolId], references: [tools.id] }),
  tag: one(tags, { fields: [toolTags.tagId], references: [tags.id] }),
}));

export const affiliateProgramsRelations = relations(affiliatePrograms, ({ one }) => ({
  tool: one(tools, {
    fields: [affiliatePrograms.toolId],
    references: [tools.id],
  }),
}));

export type User = typeof users.$inferSelect;
export type Category = typeof categories.$inferSelect;
export type Tag = typeof tags.$inferSelect;
export type Tool = typeof tools.$inferSelect;
export type AffiliateProgram = typeof affiliatePrograms.$inferSelect;
export type NewsPost = typeof newsPosts.$inferSelect;
