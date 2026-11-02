import Link from "next/link";
import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { Pagination, ResultMeta, ToolGrid } from "@/components/directory";
import { listTools } from "@/lib/tools/repository";
import { directoryHref, publicListQuery } from "@/lib/tools/query";
import { toPublicTool } from "@/lib/tools/public";
import { listAssignedVideos } from "@/lib/tool-editorial";
export const revalidate = 60;
export function generateMetadata({ searchParams }: { searchParams: Record<string, string | string[] | undefined> }): Metadata {
  const query = publicListQuery(searchParams);
  return { title: "Bekannt aus Linkjagd", description: "Finde vorhandene Tools aus Linkjagd-Videos nach Teilnummer, Videotitel und Aufgabe.", alternates: { canonical: directoryHref("/linkjagd", query) }, ...(query.q || query.videoSearch || query.linkjagdVideo ? { robots: { index: false, follow: true } } : {}) };
}
export default async function LinkjagdPage({ searchParams }: { searchParams: Record<string, string | string[] | undefined> }) {
  const database = await getDb();
  const query = publicListQuery(searchParams, { linkjagdOnly: true, sort: "alpha" });
  const [result, videos] = await Promise.all([listTools(database, query), listAssignedVideos(database)]);
  const safe = { ...query, page: result.page };
  return <div className="page-wrap py-12"><p className="text-xs font-semibold uppercase tracking-widest text-hunt">Aus den Videos</p><h1 className="mt-3 text-4xl font-bold sm:text-5xl">Bekannt aus Linkjagd</h1><p className="mt-4 max-w-2xl leading-7 text-muted-foreground">Du hast eine Website im Video gesehen? Suche nach Teilnummer, Videotitel oder Kennung und grenze die Tools nach Name oder Aufgabe ein.</p>
    <form key={directoryHref("/linkjagd", safe)} action="/linkjagd" method="get" className="mt-7 grid gap-4 rounded-2xl border border-border bg-card p-5 sm:grid-cols-2"><label className="grid gap-2 text-sm font-semibold">Video suchen<input name="folge" defaultValue={query.videoSearch} placeholder="Teilnummer, Videotitel oder Kennung" className="field" maxLength={120} /></label><label className="grid gap-2 text-sm font-semibold">Tool oder Aufgabe<input name="q" defaultValue={query.q} placeholder="Name oder Aufgabe" className="field" maxLength={120} /></label><label className="grid gap-2 text-sm font-semibold sm:col-span-2">Bestimmtes Video<select name="video-id" defaultValue={query.linkjagdVideo} className="field"><option value="">Alle zugeordneten Videos</option>{videos.map((video) => <option key={video.id} value={video.id}>{video.part ? `Teil ${video.part} · ` : ""}{video.title} ({video.id})</option>)}</select></label><div className="flex flex-wrap items-center gap-4 sm:col-span-2"><button type="submit" className="min-h-11 rounded-full bg-primary px-5 font-semibold text-primary-foreground">Tools aus Videos finden</button><Link href="/linkjagd" className="text-sm underline">Suche zurücksetzen</Link></div></form>
    <div className="mt-8"><ResultMeta page={safe.page} pageSize={query.pageSize} total={result.total} /></div><div className="mt-4"><ToolGrid tools={result.items.map((tool) => toPublicTool(tool))} resetHref="/tools" /></div><Pagination query={safe} total={result.total} basePath="/linkjagd" />
    <p className="mt-8 text-sm text-muted-foreground">Business-Software suchst du nach Anforderungen? <Link href="/vergleiche" className="text-hunt underline">Zu den Vergleichen →</Link></p>
  </div>;
}
