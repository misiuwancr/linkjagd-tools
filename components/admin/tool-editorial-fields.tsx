"use client";
import { useState } from "react";
import type { LinkjagdVideo } from "@/lib/tool-editorial";

export function ToolEditorialFields({ videos = [], publishedAt }: { videos?: LinkjagdVideo[]; publishedAt?: string | null }) {
  const [rows, setRows] = useState(() => videos.map((video, key) => ({ key, video })));
  const [nextKey, setNextKey] = useState(videos.length);
  return <fieldset className="grid gap-4 rounded-2xl border border-border p-4"><legend className="px-2 font-semibold">Linkjagd-Videos und Veröffentlichung</legend>
    <p className="text-sm leading-6 text-muted-foreground">Nur tatsächliche Videozuordnungen eintragen. Ein Tool kann in mehreren Videos vorkommen. Verwende dieselbe Kennung für dasselbe Video; ein öffentlicher Link ist optional.</p>
    <label className="grid gap-1 text-sm">Belegtes Veröffentlichungsdatum dieses Verzeichniseintrags<input type="date" name="publishedOn" defaultValue={publishedAt?.slice(0, 10) ?? ""} className="field" /></label>
    <p className="text-xs leading-6 text-muted-foreground">Bei alten Einträgen unbekannt lassen. Erstellungs- oder Importdaten sind kein Veröffentlichungsnachweis. Bei erstmaliger Freigabe eines Entwurfs wird das Datum automatisch erfasst. Bereits belegte Daten bleiben erhalten.</p>
    {rows.map(({ key, video }, index) => <div key={key} className="grid gap-3 rounded-xl border border-border p-3 sm:grid-cols-2"><p className="font-medium sm:col-span-2">Video {index + 1}</p>
      <label className="grid gap-1 text-sm">Video-Kennung<input name="linkjagdVideoId" required defaultValue={video.id} placeholder="z. B. websites-teil-36" className="field" /></label>
      <label className="grid gap-1 text-sm">Titel<input name="linkjagdVideoTitle" required defaultValue={video.title} className="field" /></label>
      <label className="grid gap-1 text-sm">Teilnummer (optional)<input name="linkjagdVideoPart" type="number" min={1} max={100000} defaultValue={video.part ?? ""} className="field" /></label>
      <label className="grid gap-1 text-sm">Öffentlicher Videolink (optional)<input name="linkjagdVideoUrl" type="url" defaultValue={video.url} placeholder="https://" className="field" /></label>
      <button type="button" onClick={() => setRows((current) => current.filter((row) => row.key !== key))} className="min-h-10 justify-self-start text-sm underline">Zuordnung entfernen</button>
    </div>)}
    <button type="button" disabled={rows.length >= 20} onClick={() => { setRows((current) => [...current, { key: nextKey, video: { id: "", title: "", part: null, url: "" } }]); setNextKey((current) => current + 1); }} className="min-h-11 justify-self-start rounded-full border border-border px-4 text-sm disabled:opacity-50">Video zuordnen</button>
  </fieldset>;
}
