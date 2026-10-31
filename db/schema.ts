import { relations } from "drizzle-orm";
import {
  index,
  integer,
  primaryKey,
  sqliteTable,
  text,
} from "drizzle-orm/sqlite-core";

export const publishStatuses = ["draft", "published", "archived"] as const;
export const pricingModels = ["free", "freemium", "paid"] as const;
export const licenseTypes = ["open_source", "proprietary", "unknown"] as const;
export const affiliateStatuses = [
  "none_found",
  "found",
  "application_pending",
  "approved",
  "active",
  "disabled",
] as const;
export const programPresences = ["yes", "no", "unknown"] as const;
export const triStates = ["ja", "nein", "unklar"] as const;
export const userRoles = ["admin", "editor"] as const;
export const newsStatuses = ["draft", "published"] as const;

export type PublishStatus = (typeof publishStatuses)[number];
export type PricingModel = (typeof pricingModels)[number];
export type LicenseType = (typeof licenseTypes)[number];
export type AffiliateStatus = (typeof affiliateStatuses)[number];
export type ProgramPresence = (typeof programPresences)[number];
export type TriState = (typeof triStates)[number];
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
    licenseType: text("license_type", { enum: licenseTypes }).notNull().default("unknown"),
    ossProjectUrl: text("oss_project_url"),
    ossRepoUrl: text("oss_repo_url"),
    ossLicense: text("oss_license"),
    ossOperatingSystems: text("oss_operating_systems").notNull().default("[]"),
    ossInstallNotes: text("oss_install_notes"),
    useCasesDe: text("use_cases_de").notNull().default("[]"),
    tiktokUrl: text("tiktok_url"),
    instagramReelUrl: text("instagram_reel_url"),
    youtubeShortUrl: text("youtube_short_url"),
    editorRating: integer("editor_rating"),
    lastCheckedAt: integer("last_checked_at", { mode: "timestamp" }),
    beginnerFriendly: integer("beginner_friendly", { mode: "boolean" }).notNull().default(false),
    germanUi: text("german_ui", { enum: triStates }).notNull().default("unklar"),
    noSignup: text("no_signup", { enum: triStates }).notNull().default("unklar"),
    contentLocked: integer("content_locked", { mode: "boolean" }).notNull().default(false),
    missingFields: text("missing_fields").notNull().default("[]"),
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
    programInfoUrl: text("program_info_url"),
    programPresence: text("program_presence", { enum: programPresences }).notNull().default("unknown"),
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
    programSlot: text("program_slot").notNull().default(""),
    targetKind: text("target_kind", { enum: ["affiliate", "official"] }).notNull(),
    day: text("day").notNull(),
    count: integer("count").notNull().default(0),
  },
  (table) => ({
    pk: primaryKey({
      columns: [table.toolId, table.targetKind, table.day, table.programSlot],
    }),
  }),
);

export const newsPosts = sqliteTable("news_posts", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  slug: text("slug").notNull().unique(),
  excerpt: text("excerpt").notNull(),
  body: text("body").notNull().default(""),
  sourceName: text("source_name"),
  coverImageUrl: text("cover_image_url"),
  seoTitle: text("seo_title"),
  seoDescription: text("seo_description"),
  status: text("status", { enum: newsStatuses }).notNull().default("draft"),
  publishedAt: integer("published_at", { mode: "timestamp" }),
  createdAt: timestamp("created_at"),
  updatedAt: timestamp("updated_at"),
});

export const newsletterStatuses = ["pending", "confirmed"] as const;

export const newsletterSubscribers = sqliteTable("newsletter_subscribers", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  status: text("status", { enum: newsletterStatuses }).notNull().default("pending"),
  confirmToken: text("confirm_token").notNull().unique(),
  createdAt: timestamp("created_at"),
  confirmedAt: integer("confirmed_at", { mode: "timestamp" }),
});

export const siteSettings = sqliteTable("site_settings", {
  key: text("key").primaryKey(),
  value: text("value").notNull().default(""),
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
