import type { AffiliateProgram, Tool } from "@/db/schema";

export type RedirectDecision =
  | { ok: true; location: string; programId: string; toolId: string }
  | { ok: false; reason: string };

export type UrlCheck =
  | { ok: true; url: string }
  | { ok: false; reason: string };

function normalizedUrl(value: string) {
  const url = new URL(value);
  url.hash = "";
  const host = url.hostname.replace(/^www\./i, "").toLowerCase();
  const path = url.pathname.replace(/\/$/, "") || "/";
  const params = [...url.searchParams.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, item]) => `${key}=${item}`)
    .join("&");
  return `${url.protocol}//${host}${path}?${params}`;
}

export function sameDestination(left: string, right: string) {
  try {
    return normalizedUrl(left) === normalizedUrl(right);
  } catch {
    return false;
  }
}

function isBlockedHost(hostname: string) {
  const host = hostname.toLowerCase().replace(/\.$/, "");
  if (
    host === "localhost" ||
    host.endsWith(".localhost") ||
    host.endsWith(".local") ||
    host === "0.0.0.0" ||
    host === "::1" ||
    host === "[::1]"
  ) {
    return true;
  }
  const match = host.match(/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/);
  if (!match) return false;
  const parts = match.slice(1).map(Number);
  if (parts.some((part) => part > 255)) return true;
  const [a, b] = parts;
  if (a === 10 || a === 127 || a === 0) return true;
  if (a === 192 && b === 168) return true;
  if (a === 172 && b >= 16 && b <= 31) return true;
  if (a === 169 && b === 254) return true;
  return false;
}

export function validateOutboundUrl(
  raw: string | null | undefined,
  originalUrl: string,
  siteHost?: string,
): UrlCheck {
  if (!raw || !raw.trim()) return { ok: false, reason: "missing_url" };
  let url: URL;
  try {
    url = new URL(raw.trim());
  } catch {
    return { ok: false, reason: "invalid_url" };
  }
  if (url.protocol !== "http:" && url.protocol !== "https:") {
    return { ok: false, reason: "bad_protocol" };
  }
  if (url.username || url.password) return { ok: false, reason: "credentials_in_url" };
  if (isBlockedHost(url.hostname)) return { ok: false, reason: "blocked_host" };
  if (siteHost && url.hostname.replace(/^www\./, "").toLowerCase() === siteHost.toLowerCase()) {
    return { ok: false, reason: "own_host" };
  }
  const href = url.toString();
  if (sameDestination(href, originalUrl)) return { ok: false, reason: "matches_original" };
  return { ok: true, url: href };
}

export function decideRedirect(
  tool: Pick<Tool, "id" | "publishStatus" | "originalUrl"> | null,
  programs: Pick<AffiliateProgram, "id" | "affiliateUrl" | "status" | "isActive" | "priority">[],
  siteHost?: string,
): RedirectDecision {
  if (!tool || tool.publishStatus !== "published") {
    return { ok: false, reason: "not_published" };
  }
  const candidates = programs
    .filter((program) => program.isActive && program.status === "active")
    .sort((a, b) => b.priority - a.priority);
  if (candidates.length === 0) return { ok: false, reason: "no_active_affiliate" };
  for (const program of candidates) {
    const checked = validateOutboundUrl(program.affiliateUrl, tool.originalUrl, siteHost);
    if (checked.ok) {
      return { ok: true, location: checked.url, programId: program.id, toolId: tool.id };
    }
  }
  return { ok: false, reason: "invalid_affiliate" };
}
