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
  discoverySources: string[];
};

type SearchParams = Record<string, string | string[] | undefined>;

function first(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value;
}

function triParam(value: string | undefined): "ja" | "nein" | "unklar" | "" {
  if (value === "ja" || value === "nein" || value === "unklar") return value;
  return "";
}

function pageNumber(value: string | undefined) {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed < 1) return 1;
  return Math.min(parsed, 10000);
}

export function publicListQuery(params: SearchParams, overrides: Partial<ToolListQuery> = {}): ToolListQuery {
  const category = first(params.kategorie)?.trim().toLowerCase() ?? "";
  return {
    q: (first(params.q) ?? "").trim().slice(0, 120),
    categorySlug: /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(category) ? category : "",
    pricing: pricingFromParam(first(params.preis)),
    license: licenseFromParam(first(params.lizenz)),
    sort: sortFromParam(first(params.sort)),
    page: pageNumber(first(params.seite)),
    pageSize: PAGE_SIZE,
    status: "published",
    featuredOnly: false,
    rankedOnly: false,
    excludeExamples: true,
    partnerGap: false,
    fromVideo: first(params.video) === "ja",
    germanUi: triParam(first(params.deutsch)),
    noSignup: triParam(first(params.anmeldung)),
    discoverySources: [],
    ...overrides,
  };
}

export function directoryHref(
  basePath: string,
  query: Pick<ToolListQuery, "q" | "categorySlug" | "pricing" | "license" | "sort" | "page" | "fromVideo" | "germanUi" | "noSignup">,
  patch: Partial<Pick<ToolListQuery, "q" | "categorySlug" | "pricing" | "license" | "sort" | "page" | "fromVideo" | "germanUi" | "noSignup">> = {},
) {
  const next = { ...query, ...patch };
  const params = new URLSearchParams();
  if (next.q) params.set("q", next.q);
  if (next.categorySlug && basePath === "/tools") params.set("kategorie", next.categorySlug);
  if (next.pricing) params.set("preis", pricingParam(next.pricing));
  if (next.license) params.set("lizenz", licenseParam(next.license));
  if (next.fromVideo) params.set("video", "ja");
  if (next.germanUi) params.set("deutsch", next.germanUi);
  if (next.noSignup) params.set("anmeldung", next.noSignup);
  if (next.sort !== "newest") params.set("sort", sortParam(next.sort));
  if (next.page > 1) params.set("seite", String(next.page));
  const qs = params.toString();
  return qs ? `${basePath}?${qs}` : basePath;
}
