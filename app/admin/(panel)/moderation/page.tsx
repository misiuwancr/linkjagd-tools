import Link from "next/link";
import { getDb } from "@/db/client";
import { listTools } from "@/lib/tools/repository";
import type { ToolListQuery } from "@/lib/tools/query";

export const dynamic = "force-dynamic";

export default async function ModerationPage() {
  const query: ToolListQuery = {
    q: "",
    categorySlug: "",
    pricing: "",
    license: "",
    sort: "newest",
    page: 1,
    pageSize: 200,
    status: "draft",
    featuredOnly: false,
    rankedOnly: false,
    excludeExamples: false,
    partnerGap: false,
    discoverySources: ["import", "submission", "futuretools-top100"],
  };
  const result = await listTools(await getDb(), query);
  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight">Moderation</h1>
      <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
        Entwürfe aus Import, Einreichung und der FutureTools-Beliebtheitsliste. Nichts davon ist öffentlich, bis du es veröffentlichst.
      </p>
      {result.items.length === 0 ? (
        <p className="mt-8 rounded-2xl border border-dashed border-border bg-card p-6 text-sm">Keine offenen Fundstücke.</p>
      ) : (
        <ul className="mt-6 divide-y divide-border rounded-2xl border border-border bg-card">
          {result.items.map((tool) => (
            <li key={tool.id} className="flex flex-col gap-1 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="font-medium">{tool.name}</p>
                <p className="text-sm text-muted-foreground">
                  {tool.discoverySource === "import" ? "Import" : "Einreichung"} · {tool.domain}
                </p>
              </div>
              <Link href={`/admin/tools/${tool.id}`} className="text-sm font-medium underline">
                Prüfen
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
