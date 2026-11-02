import Link from "next/link";
import { ArrowDown, ArrowUp } from "lucide-react";
import type { AppDatabase } from "@/db/client";
import type { PublicTool } from "@/lib/tools/public";
import { getSetting } from "@/lib/tools/repository";
import { previousRanks, rankMovement } from "@/lib/editorial-ranking";
import { PartnerBanner } from "@/components/partner-banner";
import { ToolLogo } from "@/components/tool-logo";

export async function TopToolsSidebar({ database, tools }: { database: AppDatabase; tools: PublicTool[] }) {
  const previous = previousRanks(await getSetting(database, "editorial_previous_ranks"));
  return <aside aria-labelledby="top-tools-heading" className="self-start lg:sticky lg:top-24">
    <PartnerBanner database={database} slot="top20" />
    <p className="text-xs font-semibold uppercase tracking-widest text-hunt">Redaktionelle Auswahl</p>
    <h2 id="top-tools-heading" className="mt-2 text-2xl font-bold">Top 20 KI-Tools</h2>
    <p className="mt-2 text-sm text-muted-foreground">Unsere Auswahl für deinen Werkzeugkasten.</p>
    {tools.length ? <ol tabIndex={0} aria-label="Top 20 – scrollbare Liste" className="mt-5 lg:max-h-[800px] lg:overflow-y-auto divide-y divide-border rounded-2xl border border-border bg-card">{tools.slice(0, 20).map((tool) => {
      const movement = rankMovement(tool.editorialRank, previous[tool.id]);
      return <li key={tool.id}><Link href={`/tools/${tool.slug}`} className="flex items-center gap-3 p-3 transition hover:bg-secondary/60">
        <span className="w-5 shrink-0 text-center text-sm text-muted-foreground">{tool.editorialRank}</span>
        <ToolLogo name={tool.name} logo={tool.logo} />
        <span className="min-w-0 flex-1"><span className="block font-semibold text-foreground">{tool.name}</span><span className="mt-1 line-clamp-1 block text-xs text-muted-foreground">{tool.shortDescriptionDe}</span></span>
        <span aria-label={movement === "up" ? "Platzierung gestiegen" : movement === "down" ? "Platzierung gefallen" : "Keine belegte Platzänderung"}>
          {movement === "up" ? <ArrowUp className="h-4 w-4 text-hunt" aria-hidden="true" /> : movement === "down" ? <ArrowDown className="h-4 w-4 text-muted-foreground" aria-hidden="true" /> : "–"}
        </span>
      </Link></li>;
    })}</ol> : <p className="mt-5 text-sm text-muted-foreground">Die erste Auswahl erscheint hier nach Veröffentlichung.</p>}
    <Link href="/top-20" className="mt-4 inline-block text-sm font-semibold text-hunt">Zur vollständigen Liste →</Link>
  </aside>;
}
