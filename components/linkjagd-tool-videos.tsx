import Link from "next/link";
import type { PublicTool } from "@/lib/tools/public";
export function LinkjagdToolVideos({ tool }: { tool: PublicTool }) {
  if (!tool.linkjagdVideos?.length) return null;
  return <section className="mt-8 rounded-2xl border border-hunt/30 bg-card p-5"><h2 className="text-xl font-bold">Bekannt aus Linkjagd</h2><ul className="mt-4 grid gap-4">{tool.linkjagdVideos.map((video) => <li key={video.id}><Link href={"/linkjagd?video-id=" + encodeURIComponent(video.id)} className="break-words font-semibold text-hunt [overflow-wrap:anywhere]">{video.part ? `Teil ${video.part} · ` : ""}{video.title}</Link>{video.url ? <a href={video.url} target="_blank" rel="noopener noreferrer" className="ml-3 inline-block py-2 text-sm underline">Video öffnen ↗</a> : null}</li>)}</ul></section>;
}
