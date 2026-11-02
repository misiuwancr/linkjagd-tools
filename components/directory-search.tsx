import Link from "next/link";
import { licenseOptions, pricingOptions, sortOptions } from "@/lib/labels";
import { directoryHref, type ToolListQuery } from "@/lib/tools/query";

export function DirectorySearch({ query, categories, showPopular, toolCount }: {
  query: ToolListQuery; categories: { name: string; slug: string; toolCount: number }[];
  showPopular: boolean; toolCount: number;
}) {
  const sorts = sortOptions.filter((item) => showPopular || item.value !== "popular");
  return <form method="get" action="/tools" role="search" aria-label="Verzeichnis durchsuchen" className="space-y-5 rounded-3xl border border-border bg-card p-4 sm:p-6">
    <div><label htmlFor="verzeichnis-suche" className="mb-2 block text-lg font-semibold">Was möchtest du entdecken?</label>
      <div className="flex flex-col gap-2 sm:flex-row"><input id="verzeichnis-suche" name="q" type="search" maxLength={120} defaultValue={query.q} placeholder="Name oder Aufgabe, z. B. Bilder bearbeiten" className="field min-w-0 flex-1 !py-3 text-base" /><button type="submit" className="min-h-12 shrink-0 rounded-xl bg-primary px-6 font-semibold text-primary-foreground">Tools finden</button></div>
      <p className="mt-2 text-xs text-muted-foreground">{toolCount.toLocaleString("de-DE")} vorhandene Tools und Websites · Auswahl über die Adresse teilbar</p>
    </div>
    <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_minmax(180px,0.5fr)]">
      <fieldset><legend className="mb-2 text-sm font-semibold">Preismodell</legend><div className="flex flex-wrap gap-2">{[{value: "", label: "Alle Preise", param: ""}, ...pricingOptions].map((item) => <label key={item.value} className="cursor-pointer"><input type="radio" name="preis" value={item.param} defaultChecked={query.pricing === item.value} className="peer sr-only" /><span className="inline-flex min-h-10 items-center rounded-full border border-border px-3 text-sm peer-checked:border-hunt peer-checked:bg-hunt/10 peer-checked:text-hunt peer-focus-visible:ring-2 peer-focus-visible:ring-hunt">{item.label}</span></label>)}</div></fieldset>
      <div><label htmlFor="sort" className="mb-2 block text-sm font-semibold">Sortierung</label><select id="sort" name="sort" defaultValue={sorts.find((item) => item.value === query.sort)?.param ?? "neueste"} className="field">{sorts.map((item) => <option key={item.value} value={item.param}>{item.label}</option>)}</select></div>
    </div>
    <details open={query.categorySlugs.length > 0} className="rounded-2xl border border-border p-4"><summary className="cursor-pointer text-sm font-semibold">Kategorien auswählen{query.categorySlugs.length ? ` (${query.categorySlugs.length} aktiv)` : ""}</summary>
      <fieldset className="mt-3"><legend className="mb-3 text-xs leading-6 text-muted-foreground">Mehrere Kategorien sind möglich: Treffer aus mindestens einer ausgewählten Kategorie. Preis und weitere Filter gelten zusätzlich.</legend><div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">{categories.map((category) => <label key={category.slug} className="flex min-h-10 cursor-pointer items-center gap-2 rounded-xl border border-border px-3 py-2 text-sm has-[:checked]:border-hunt has-[:checked]:bg-hunt/10"><input type="checkbox" name="kategorie" value={category.slug} defaultChecked={query.categorySlugs.includes(category.slug)} className="h-4 w-4 shrink-0 accent-hunt" /><span className="min-w-0 flex-1">{category.name}</span><span className="text-xs text-muted-foreground">{category.toolCount}</span></label>)}</div></fieldset>
      {query.categorySlugs.filter((slug) => !categories.some((category) => category.slug === slug)).map((slug) => <input type="hidden" key={slug} name="kategorie" value={slug} />)}
    </details>
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"><div><label htmlFor="lizenz" className="mb-2 block text-sm font-semibold">Lizenz</label><select id="lizenz" name="lizenz" defaultValue={licenseOptions.find((item) => item.value === query.license)?.param ?? ""} className="field"><option value="">Alle Lizenzen</option>{licenseOptions.map((item) => <option key={item.value} value={item.param}>{item.label}</option>)}</select></div>
    <div><label htmlFor="deutsch" className="mb-2 block text-sm font-semibold">Auf Deutsch nutzbar</label><select id="deutsch" name="deutsch" defaultValue={query.germanUi} className="field"><option value="">Alle</option><option value="ja">Ja</option><option value="nein">Nein</option><option value="unklar">Unklar</option></select></div>
    <div><label htmlFor="anmeldung" className="mb-2 block text-sm font-semibold">Ohne Anmeldung</label><select id="anmeldung" name="anmeldung" defaultValue={query.noSignup} className="field"><option value="">Alle</option><option value="ja">Ja</option><option value="nein">Nein</option><option value="unklar">Unklar</option></select></div></div>
    <div className="flex flex-wrap items-center gap-x-5 gap-y-3"><label className="flex min-h-10 cursor-pointer items-center gap-2 text-sm"><input type="checkbox" name="picks" value="ja" defaultChecked={query.featuredOnly} className="h-4 w-4 accent-hunt" />Nur redaktionelle Empfehlungen</label><label className="flex min-h-10 cursor-pointer items-center gap-2 text-sm"><input type="checkbox" name="video" value="ja" defaultChecked={query.fromVideo} className="h-4 w-4 accent-hunt" />Mit Videolink</label></div>
    {query.company ? <input type="hidden" name="firma" value={query.company} /> : null}
    <div className="flex flex-wrap items-center gap-3 border-t border-border pt-4"><button type="submit" className="min-h-11 rounded-xl bg-primary px-5 text-sm font-semibold text-primary-foreground">Auswahl anwenden</button><Link href="/tools" className="inline-flex min-h-11 items-center rounded-xl px-2 text-sm text-muted-foreground underline">Alles zurücksetzen</Link><span className="text-xs text-muted-foreground">Filter auswählen und anwenden.</span></div>
  </form>;
}

export function ActiveDirectoryFilters({ query, categories }: { query: ToolListQuery; categories: { slug: string; name: string }[] }) {
  const items: { label: string; href: string }[] = [];
  const remove = (label: string, patch: Parameters<typeof directoryHref>[2]) => items.push({ label, href: directoryHref("/tools", query, { ...patch, page: 1 }) });
  if (query.q) remove(`Suche: ${query.q}`, { q: "" });
  query.categorySlugs.forEach((slug) => remove(categories.find((item) => item.slug === slug)?.name ?? slug, { categorySlugs: query.categorySlugs.filter((value) => value !== slug) }));
  if (query.pricing) remove(pricingOptions.find((item) => item.value === query.pricing)?.label ?? query.pricing, { pricing: "" });
  if (query.license) remove(licenseOptions.find((item) => item.value === query.license)?.label ?? query.license, { license: "" });
  if (query.featuredOnly) remove("Redaktionelle Empfehlungen", { featuredOnly: false });
  if (query.fromVideo) remove("Mit Videolink", { fromVideo: false });
  if (query.germanUi) remove(`Auf Deutsch: ${query.germanUi}`, { germanUi: "" });
  if (query.noSignup) remove(`Ohne Anmeldung: ${query.noSignup}`, { noSignup: "" });
  if (query.company) remove(`Firma: ${query.company}`, { company: "" });
  if (!items.length) return null;
  return <nav aria-label="Aktive Filter" className="mt-4 flex flex-wrap gap-2">{items.map((item) => <Link key={item.label} href={item.href} aria-label={`Filter entfernen: ${item.label}`} className="inline-flex min-h-10 max-w-full items-center gap-2 rounded-full border border-hunt/40 bg-hunt/10 px-3 py-2 text-sm text-hunt"><span className="break-words [overflow-wrap:anywhere]">{item.label}</span><span aria-hidden="true">×</span></Link>)}</nav>;
}
