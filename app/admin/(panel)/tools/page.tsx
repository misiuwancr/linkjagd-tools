import { affiliateTarget } from "@/lib/affiliate/redirect";
import { siteConfig } from "@/site.config";
import Link from "next/link";
import { getDb } from "@/db/client";
import { Flash } from "@/components/admin/shell";
import { pricingLabel, programPresenceLabel, publishLabels } from "@/lib/labels";
import { listTools } from "@/lib/tools/repository";
import { publicListQuery, type ToolListQuery } from "@/lib/tools/query";

export const dynamic = "force-dynamic";

export default async function AdminToolsPage({
  searchParams,
}: {
  searchParams: { gespeichert?: string; fehler?: string; status?: string; partner?: string; q?: string; seite?: string };
}) {
  const status = searchParams.status === "draft" || searchParams.status === "archived" || searchParams.status === "published" ? searchParams.status : "all";
  const partnerGap = searchParams.partner === "offen";
  const query: ToolListQuery = {
    q: publicListQuery(searchParams).q,
    categorySlug: "",
    categorySlugs: [],
    pricing: "",
    license: "",
    sort: "newest",
    page: publicListQuery(searchParams).page,
    pageSize: partnerGap ? 200 : 100,
    status,
    featuredOnly: false,
    rankedOnly: false,
    excludeExamples: false,
    partnerGap,
    fromVideo: false,
    germanUi: "",
    noSignup: "",
    company: "",
    discoverySources: [],
  };
  const result = await listTools(await getDb(), query);
  const pages = Math.max(1, Math.ceil(result.total / query.pageSize));
  const pageHref = (page: number) => { const params = new URLSearchParams(); if (query.q) params.set("q", query.q); if (status !== "all") params.set("status", status); if (partnerGap) params.set("partner", "offen"); if (page > 1) params.set("seite", String(page)); return "/admin/tools" + (params.size ? "?" + params.toString() : ""); };
  return (
    <div>
      <div className="flex items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Tools</h1>
          <p className="mt-2 text-sm text-muted-foreground">{result.total} Einträge in dieser Ansicht.</p>
        </div>
        <Link href="/admin/tools/neu" className="rounded-full bg-primary px-4 py-2 text-sm font-medium text-primary-foreground">
          Neu
        </Link>
      </div>
      <form action="/admin/tools" method="get" className="mt-5 flex flex-wrap gap-2"><label className="sr-only" htmlFor="redaktionssuche">Vorhandenes Tool suchen</label><input id="redaktionssuche" name="q" defaultValue={query.q} placeholder="Name oder Aufgabe suchen" className="field min-w-0 flex-1" />{status !== "all" ? <input type="hidden" name="status" value={status} /> : null}{partnerGap ? <input type="hidden" name="partner" value="offen" /> : null}<button type="submit" className="rounded-xl bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground">Suchen</button><Link href="/admin/tools" className="self-center px-2 text-sm underline">Zurücksetzen</Link></form>
      <Flash gespeichert={searchParams.gespeichert} fehler={searchParams.fehler} />
      <div className="mt-4 flex flex-wrap gap-2 text-sm">
        {[
          ["all", "Alle"],
          ["published", "Veröffentlicht"],
          ["draft", "Entwürfe"],
          ["archived", "Archiv"],
        ].map(([value, label]) => (
          <Link key={value} href={value === "all" ? "/admin/tools" : `/admin/tools?status=${value}`} className="rounded-full border border-border bg-card px-3 py-1">
            {label}
          </Link>
        ))}
        <Link
          href="/admin/tools?partner=offen"
          className={partnerGap ? "rounded-full bg-primary px-3 py-1 font-medium text-primary-foreground" : "rounded-full border border-border bg-card px-3 py-1"}
          aria-current={partnerGap ? "true" : undefined}
        >
          Partnerprogramm vorhanden, aber noch kein Link hinterlegt
        </Link>
      </div>
      <div className="mt-4 overflow-x-auto rounded-2xl border border-border bg-card">
        <table className="w-full min-w-[720px] text-left text-sm">
          <thead className="border-b border-border text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th className="px-4 py-3 font-medium">Name</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium">Preis</th>
              <th className="px-4 py-3 font-medium">Partnerprogramm vorhanden</th>
              <th className="px-4 py-3 font-medium">Eigenen Link</th>
            </tr>
          </thead>
          <tbody>
            {result.items.map((tool) => {
              const presence = tool.programs.some((program) => program.programPresence === "yes")
                ? "yes"
                : tool.programs.some((program) => program.programPresence === "no")
                  ? "no"
                  : "unknown";
              const hasOwnLink = Boolean(affiliateTarget(tool.programs, tool.originalUrl, new URL(siteConfig.url).hostname));
              return (
                <tr key={tool.id} className="border-b border-border last:border-0">
                  <td className="px-4 py-3">
                    <Link href={`/admin/tools/${tool.id}`} className="font-medium hover:underline">
                      {tool.name}
                    </Link>
                    <p className="text-xs text-muted-foreground">{tool.domain}</p>
                  </td>
                  <td className="px-4 py-3">{publishLabels[tool.publishStatus]}</td>
                  <td className="px-4 py-3">{pricingLabel(tool.pricingModel)}</td>
                  <td className="px-4 py-3">{programPresenceLabel(presence)}{presence === "yes" && !hasOwnLink ? ", Link fehlt" : ""}</td>
                  <td className="px-4 py-3">{hasOwnLink ? "hinterlegt" : "Affiliate-Link fehlt"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <nav aria-label="Redaktionsseiten" className="mt-5 flex flex-wrap items-center gap-4">{result.page > 1 ? <Link href={pageHref(result.page - 1)} className="rounded-full border border-border px-4 py-2">Zurück</Link> : null}<span className="text-sm">Seite {result.page} von {pages}</span>{result.page < pages ? <Link href={pageHref(result.page + 1)} className="rounded-full border border-border px-4 py-2">Weiter</Link> : null}</nav>
    </div>
  );
}
