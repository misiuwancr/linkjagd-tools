import type { LicenseType, PricingModel, PublishStatus } from "@/db/schema";
import {
  licenseFromParam,
  licenseParam,
  pricingFromParam,
  pricingParam,
  sortFromParam,
  sortParam,
  type SortKey,
} from "@/lib/labels";

export const PAGE_SIZE = 24;

export type ToolListQuery = {
  q: string;
  categorySlug: string;
  categorySlugs: string[];
  pricing: PricingModel | "";
  license: LicenseType | "";
  sort: SortKey;
  page: number;
  pageSize: number;
  status: PublishStatus | "all";
  featuredOnly: boolean;
  rankedOnly: boolean;
  excludeExamples: boolean;
  partnerGap: boolean;
  fromVideo: boolean;
  germanUi: "ja" | "nein" | "unklar" | "";
  noSignup: "ja" | "nein" | "unklar" | "";
  company: string;
  discoverySources: string[];
  linkjagdOnly?: boolean;
  linkjagdVideo?: string;
  videoSearch?: string;
  datedOnly?: boolean;
  manualRecommendationsOnly?: boolean;
};

type SearchParams = Record<string, string | string[] | undefined>;

function first(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value;
}

function triParam(value: string | undefined): "ja" | "nein" | "unklar" | "" {
  if (value === "ja" || value === "nein" || value === "unklar") return value;
  return "";
}

function companyParam(value: string | undefined) {
  const slug = (value ?? "").trim().toLowerCase();
  return /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug) ? slug : "";
}

function pageNumber(value: string | undefined) {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed < 1) return 1;
  return Math.min(parsed, 10000);
}

export function publicListQuery(params: SearchParams, overrides: Partial<ToolListQuery> = {}): ToolListQuery {
  const categorySlugs = [...new Set((Array.isArray(params.kategorie) ? params.kategorie : [params.kategorie ?? ""])
    .flatMap((value) => value.split(",")).map((value) => value.trim().toLowerCase())
    .filter((value) => /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value)))].sort().slice(0, 40);
  return {
    q: (first(params.q) ?? "").trim().slice(0, 120),
    categorySlug: categorySlugs[0] ?? "",
    categorySlugs,
    pricing: pricingFromParam(first(params.preis)),
    license: licenseFromParam(first(params.lizenz)),
    sort: sortFromParam(first(params.sort)),
    page: pageNumber(first(params.seite)),
    pageSize: PAGE_SIZE,
    status: "published",
    featuredOnly: first(params.picks) === "ja",
    rankedOnly: false,
    excludeExamples: true,
    partnerGap: false,
    fromVideo: first(params.video) === "ja",
    germanUi: triParam(first(params.deutsch)),
    noSignup: triParam(first(params.anmeldung)),
    company: companyParam(first(params.firma)),
    discoverySources: [],
    linkjagdVideo: (first(params["video-id"]) ?? "").trim().slice(0, 80),
    videoSearch: (first(params.folge) ?? "").trim().slice(0, 120),
    ...overrides,
    ...(overrides.categorySlug !== undefined && overrides.categorySlugs === undefined
      ? { categorySlugs: overrides.categorySlug ? [overrides.categorySlug] : [] } : {}),
  };
}

export function directoryHref(
  basePath: string,
  query: Pick<ToolListQuery, "q" | "categorySlug" | "pricing" | "license" | "sort" | "page" | "fromVideo" | "germanUi" | "noSignup" | "company"> & { featuredOnly?: boolean; categorySlugs?: string[]; linkjagdVideo?: string; videoSearch?: string },
  patch: Partial<Pick<ToolListQuery, "q" | "categorySlug" | "categorySlugs" | "pricing" | "license" | "sort" | "page" | "fromVideo" | "germanUi" | "noSignup" | "company" | "featuredOnly" | "linkjagdVideo" | "videoSearch">> = {},
) {
  const next = { ...query, ...patch };
  const params = new URLSearchParams();
  if (next.q) params.set("q", next.q);
  const selected = patch.categorySlug !== undefined && patch.categorySlugs === undefined
    ? (patch.categorySlug ? [patch.categorySlug] : []) : next.categorySlugs ?? (next.categorySlug ? [next.categorySlug] : []);
  if (basePath === "/tools") [...new Set(selected)].sort().forEach((slug) => params.append("kategorie", slug));
  if (next.pricing) params.set("preis", pricingParam(next.pricing));
  if (next.license) params.set("lizenz", licenseParam(next.license));
  if (next.fromVideo) params.set("video", "ja");
  if (next.germanUi) params.set("deutsch", next.germanUi);
  if (next.noSignup) params.set("anmeldung", next.noSignup);
  if (next.company) params.set("firma", next.company);
  if (next.featuredOnly) params.set("picks", "ja");
  if (next.linkjagdVideo) params.set("video-id", next.linkjagdVideo);
  if (next.videoSearch) params.set("folge", next.videoSearch);
  if (next.sort !== "newest") params.set("sort", sortParam(next.sort));
  if (next.page > 1) params.set("seite", String(next.page));
  const qs = params.toString();
  return qs ? `${basePath}?${qs}` : basePath;
}
