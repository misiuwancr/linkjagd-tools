import type { AffiliateProgram, Category, PricingModel, Tag, Tool } from "@/db/schema";
import { decideRedirect } from "@/lib/affiliate/redirect";
import { parseStringList } from "@/lib/utils";

export type PublicCategory = Pick<Category, "name" | "slug">;
export type PublicTag = Pick<Tag, "name" | "slug">;

export type PublicTool = {
  id: string;
  name: string;
  slug: string;
  domain: string;
  logo: string | null;
  shortDescriptionDe: string;
  longDescriptionDe: string;
  featuresDe: string[];
  screenshots: string[];
  pricingModel: PricingModel;
  featured: boolean;
  editorialRank: number | null;
  isExample: boolean;
  createdAt: string;
  updatedAt: string;
  categories: PublicCategory[];
  tags: PublicTag[];
  ctaEnabled: boolean;
};

type ToolRelations = Tool & {
  categories: PublicCategory[];
  tags: PublicTag[];
  programs: Pick<AffiliateProgram, "id" | "affiliateUrl" | "status" | "isActive" | "priority">[];
};

export function toPublicTool(tool: ToolRelations, siteHost?: string): PublicTool {
  const decision = decideRedirect(tool, tool.programs, siteHost);
  return {
    id: tool.id,
    name: tool.name,
    slug: tool.slug,
    domain: tool.domain,
    logo: tool.logo,
    shortDescriptionDe: tool.shortDescriptionDe,
    longDescriptionDe: tool.longDescriptionDe,
    featuresDe: parseStringList(tool.featuresDe),
    screenshots: parseStringList(tool.screenshots).filter((item) => item.startsWith("/")),
    pricingModel: tool.pricingModel,
    featured: tool.featured,
    editorialRank: tool.editorialRank,
    isExample: tool.isExample,
    createdAt: tool.createdAt.toISOString(),
    updatedAt: tool.updatedAt.toISOString(),
    categories: tool.categories,
    tags: tool.tags,
    ctaEnabled: decision.ok,
  };
}
