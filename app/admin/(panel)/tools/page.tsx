import Link from "next/link";
import { getDb } from "@/db/client";
import { Flash } from "@/components/admin/shell";
import { affiliateStatusLabel, pricingLabel, publishLabels } from "@/lib/labels";
import { listTools } from "@/lib/tools/repository";
import type { ToolListQuery } from "@/lib/tools/query";

export const dynamic = "force-dynamic";

export default async function AdminToolsPage({
  searchParams,
}: {
  searchParams: { gespeichert?: string; fehler?: string; status?: string };
}) {
  const status = searchParams.status === "draft" || searchParams.status === "archived" || searchParams.status === "published" ? searchParams.status : "all";
  const query: ToolListQuery = {
    q: "",
    categorySlug: "",
    pricing: "",
    sort: "newest",
    page: 1,
    pageSize: 100,
    status,
    featuredOnly: false,
    rankedOnly: false,
    discoverySources: [],
  };
  const result = await listTools(await getDb(), query);
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
      </div>
      <div className="mt-4 overflow-hidden rounded-2xl border border-border bg-card">
        <table className="w-full min-w-[720px] text-left text-sm">
          <thead className="border-b border-border text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th className="px-4 py-3 font-medium">Name</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium">Preis</th>
              <th className="px-4 py-3 font-medium">Partner</th>
            </tr>
          </thead>
          <tbody>
            {result.items.map((tool) => {
              const active = tool.programs.find((program) => program.isActive);
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
                  <td className="px-4 py-3">{active ? affiliateStatusLabel(active.status) : "Keiner aktiv"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
