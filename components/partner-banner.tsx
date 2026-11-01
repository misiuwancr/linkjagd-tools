import { getSetting } from "@/lib/tools/repository";
import type { AppDatabase } from "@/db/client";

export async function PartnerBanner({ database, slot }: { database: AppDatabase; slot: "directory" | "top20" }) {
  const [title, url] = await Promise.all([
    getSetting(database, `partner_${slot}_title`), getSetting(database, `partner_${slot}_url`),
  ]);
  if (!title.trim() || !url.trim()) return null;
  try { if (new URL(url).protocol !== "https:") return null; } catch { return null; }
  return <a href={url} rel="sponsored nofollow noopener noreferrer" target="_blank" className="my-6 block rounded-2xl border border-hunt/40 bg-card p-5">
    <span className="text-xs uppercase tracking-widest text-muted-foreground">Anzeige</span>
    <span className="mt-2 block font-semibold">{title}</span>
  </a>;
}
