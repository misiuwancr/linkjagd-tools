import type { AffiliateProgram, Category, LicenseType, PricingModel, Tag, Tool } from "@/db/schema";
import { decideRedirect } from "@/lib/affiliate/redirect";
import { platformText } from "@/lib/branding";
import { parseStringList } from "@/lib/utils";
import { videosFromUrls, type PublicVideo } from "@/lib/videos";
import type { ToolEditorial, LinkjagdVideo } from "@/lib/tool-editorial";

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
  licenseType: LicenseType;
  ossProjectUrl: string | null;
  ossRepoUrl: string | null;
  ossLicense: string | null;
  ossOperatingSystems: string[];
  ossInstallNotes: string | null;
  useCasesDe: string[];
  beginnerFriendly: boolean;
  germanUi: "ja" | "nein" | "unklar";
  noSignup: "ja" | "nein" | "unklar";
  editorRating: number | null;
  lastCheckedAt: string | null;
  featured: boolean;
  editorialRank: number | null;
  isExample: boolean;
  createdAt: string;
  updatedAt: string;
  categories: PublicCategory[];
  tags: PublicTag[];
  ctaEnabled: boolean;
  ctaKind: "affiliate" | "official" | "disabled";
  fromVideo: boolean;
  videos: PublicVideo[];
  linkjagdVideos?: LinkjagdVideo[];
  publishedAt?: string | null;
};

type ToolRelations = Tool & {
  categories: PublicCategory[];
  tags: PublicTag[];
  programs: Pick<AffiliateProgram, "id" | "affiliateUrl" | "status" | "isActive" | "priority">[];
  editorial?: ToolEditorial;
};

export function toPublicTool(tool: ToolRelations, siteHost?: string): PublicTool {
  const decision = decideRedirect(tool, tool.programs, siteHost);
  const videos = videosFromUrls(tool);
  return {
    id: tool.id,
    name: tool.name,
    slug: tool.slug,
    domain: tool.domain,
    logo: tool.logo,
    shortDescriptionDe: platformText(tool.shortDescriptionDe),
    longDescriptionDe: platformText(tool.longDescriptionDe),
    featuresDe: parseStringList(tool.featuresDe).map(platformText),
    screenshots: parseStringList(tool.screenshots).filter((item) => item.startsWith("/")),
    pricingModel: tool.pricingModel,
    licenseType: tool.licenseType,
    ossProjectUrl: tool.ossProjectUrl,
    ossRepoUrl: tool.ossRepoUrl,
    ossLicense: tool.ossLicense,
    ossOperatingSystems: parseStringList(tool.ossOperatingSystems),
    ossInstallNotes: tool.ossInstallNotes,
    useCasesDe: parseStringList(tool.useCasesDe).map(platformText),
    beginnerFriendly: tool.beginnerFriendly,
    germanUi: tool.germanUi ?? "unklar",
    noSignup: tool.noSignup ?? "unklar",
    editorRating: tool.editorRating,
    lastCheckedAt: tool.lastCheckedAt ? tool.lastCheckedAt.toISOString() : null,
    featured: tool.featured,
    editorialRank: tool.editorialRank,
    isExample: tool.isExample,
    createdAt: tool.createdAt.toISOString(),
    updatedAt: tool.updatedAt.toISOString(),
    categories: tool.categories,
    tags: tool.tags,
    ctaEnabled: decision.ok,
    ctaKind: decision.ok ? decision.kind : "disabled",
    videos,
    linkjagdVideos: tool.editorial?.videos ?? [],
    publishedAt: tool.editorial?.publishedAt ?? null,
    fromVideo: videos.length > 0,
  };
}
