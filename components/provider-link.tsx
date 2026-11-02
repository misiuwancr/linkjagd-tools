import { cache } from "react";
import { getDb } from "@/db/client";
import { getToolBySlug } from "@/lib/tools/repository";
import { decideRedirect } from "@/lib/affiliate/redirect";
import { goHref, type CtaPosition } from "@/lib/affiliate/context";
import { siteConfig } from "@/site.config";
export const outboundTool = cache(async (slug: string) => {
  const tool = await getToolBySlug(await getDb(), slug);
  if (!tool || tool.publishStatus !== "published" || tool.isExample) return null;
  const decision = decideRedirect(tool, tool.programs, new URL(siteConfig.url).hostname);
  return decision.ok ? { tool, decision } : null;
});
export async function ProviderLink({ slug, source, position, className, label }: { slug: string; source: string; position: CtaPosition; className?: string; label?: string }) {
  const result = await outboundTool(slug);
  if (!result) return null;
  const sponsored = result.decision.kind === "affiliate";
  return <a href={goHref(slug, source, position)} rel={sponsored ? "sponsored nofollow noopener" : "nofollow noopener"} className={className}>{label ?? `Zu ${result.tool.name}`} {sponsored ? "· Anzeige " : ""}↗</a>;
}
