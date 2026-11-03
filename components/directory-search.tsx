"use client";

import { useRouter } from "next/navigation";
import { pricingOptions, sortOptions } from "@/lib/labels";
import { type ToolListQuery } from "@/lib/tools/query";

export function DirectorySearch({ query, categories }: {
  query: ToolListQuery; categories: { name: string; slug: string; toolCount: number }[];

}) {
  const router = useRouter();
  const apply = (form: HTMLFormElement) => { const params = new URLSearchParams(); new FormData(form).forEach((value, key) => { if (typeof value === "string" && value) params.append(key, value); }); router.push(`/tools?${params.toString()}`, { scroll: false }); };
  return <form method="get" action="/tools" onSubmit={(event) => { event.preventDefault(); apply(event.currentTarget); }} onChange={(event) => { if ((event.target as HTMLInputElement).type !== "search") apply(event.currentTarget); }} role="search" aria-label="Verzeichnis durchsuchen" className="space-y-2 rounded-2xl border border-border bg-card p-3">
    <div className="flex flex-wrap items-center gap-2">
      <input aria-label="Tools suchen" name="q" type="search" maxLength={120} defaultValue={query.q} placeholder="Tools suchen …" className="field !h-9 w-full sm:max-w-xs" />
      <button type="submit" className="sr-only">Suchen</button>
      <fieldset><legend className="sr-only">Preismodell</legend><div className="flex flex-wrap gap-2">{[{value: "", label: "Alle Preise", param: ""}, ...pricingOptions].map((item) => <label key={item.value} className="cursor-pointer"><input type="radio" name="preis" value={item.param} defaultChecked={query.pricing === item.value} className="peer sr-only" /><span className="inline-flex min-h-8 items-center rounded-full border border-border px-3 text-sm peer-checked:border-hunt peer-checked:bg-hunt/10 peer-checked:text-hunt peer-focus-visible:ring-2 peer-focus-visible:ring-hunt">{item.label}</span></label>)}</div></fieldset>
      <label className="cursor-pointer"><input className="peer sr-only" type="checkbox" name="lizenz" value="open-source" defaultChecked={query.license === "open_source"} /><span className="inline-flex min-h-8 items-center rounded-full border border-border px-3 text-sm peer-checked:border-hunt peer-checked:text-hunt peer-focus-visible:ring-2 peer-focus-visible:ring-hunt">Open Source</span></label>
      <label className="cursor-pointer"><input className="peer sr-only" type="checkbox" name="picks" value="ja" defaultChecked={query.featuredOnly} /><span className="inline-flex min-h-8 items-center rounded-full border border-border px-3 text-sm peer-checked:border-hunt peer-checked:text-hunt peer-focus-visible:ring-2 peer-focus-visible:ring-hunt">Empfehlungen</span></label>
    </div>
    <input type="hidden" name="sort" value={sortOptions.find((item) => item.value === query.sort)?.param ?? "neueste"} />
    <details className="border-t border-border pt-2"><summary className="cursor-pointer text-sm font-semibold">Kategorien ({query.categorySlugs.length || categories.length})</summary>
      <div className="mt-2 flex flex-wrap gap-2">{categories.map((category) => <label key={category.slug} className="cursor-pointer"><input type="checkbox" name="kategorie" value={category.slug} defaultChecked={query.categorySlugs.includes(category.slug)} className="peer sr-only" /><span className="inline-flex min-h-8 items-center rounded-full border border-border px-3 text-sm peer-checked:border-hunt peer-checked:text-hunt peer-focus-visible:ring-2 peer-focus-visible:ring-hunt">{category.name}</span></label>)}</div>
    </details>
    {query.company ? <input type="hidden" name="firma" value={query.company} /> : null}
    {query.linkjagdVideo ? <input type="hidden" name="video-id" value={query.linkjagdVideo} /> : null}
    {query.videoSearch ? <input type="hidden" name="folge" value={query.videoSearch} /> : null}
  </form>;
}
