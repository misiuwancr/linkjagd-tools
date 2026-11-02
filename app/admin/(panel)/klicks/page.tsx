import Link from "next/link";
import { getDb } from "@/db/client";
import { listClickStats } from "@/lib/tools/repository";
import { programPresenceLabel } from "@/lib/labels";
import { getComparison } from "@/lib/comparisons";
import { contextClickStats } from "@/lib/affiliate/context";
import { requireUser } from "@/lib/auth/session";
import { utcDay } from "@/lib/utils";

export const dynamic = "force-dynamic";

function shift(days: number) {
  const date = new Date();
  date.setUTCDate(date.getUTCDate() - (days - 1));
  return utcDay(date);
}

export default async function ClicksPage({
  searchParams,
}: {
  searchParams: { sort?: string };
}) {
  await requireUser("editor");
  const sort = searchParams.sort === "30" ? "30" : "7";
  const database = await getDb();
  const [rows, contexts] = await Promise.all([listClickStats(database, shift(7), shift(30)), contextClickStats(database, shift(sort === "30" ? 30 : 7))]);
  const sources = new Map<string, number>();
  for (const row of contexts) sources.set(row.source, (sources.get(row.source) ?? 0) + row.count);
  const editorialSources = [...sources].filter(([source]) => source.startsWith("/blog/")).sort((a, b) => b[1] - a[1]);
  const collectionClicks = [...sources].filter(([source]) => source === "/linkjagd" || source.startsWith("/fuer/")).reduce((sum, [, count]) => sum + count, 0);
  rows.sort((a, b) => (sort === "30" ? b.days30 - a.days30 : b.days7 - a.days7) || a.name.localeCompare(b.name, "de"));
  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight">Klicks</h1>
      <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
        Gezählt werden Aufrufe von /go, keine Personen, Verkäufe oder Conversion-Raten. Wiederholungen und automatische Aufrufe können enthalten sein. HEAD und erkennbare Vorabrufe werden nicht gezählt. Quellseiten/Positionen sind erst ab Einführung der erweiterten Messung verfügbar; sie werden nicht zu den Tool-Summen addiert.
      </p>
      <div className="mt-4 flex gap-2 text-sm">
        <Link href="/admin/klicks?sort=7" className={sort === "7" ? "font-semibold text-hunt" : "text-muted-foreground"}>7 Tage</Link>
        <Link href="/admin/klicks?sort=30" className={sort === "30" ? "font-semibold text-hunt" : "text-muted-foreground"}>30 Tage</Link>
      </div>
      <section className="mt-8 rounded-2xl border border-border bg-card p-5"><h2 className="text-xl font-bold">Redaktionelle Bereiche</h2><p className="mt-3 text-sm">Anbieter-Klicks aus Linkjagd und Sammlungen: <strong>{collectionClicks}</strong></p><h3 className="mt-5 font-semibold">Vergleiche und Artikel nach Anbieter-Klicks</h3>{editorialSources.length ? <ol className="mt-3 space-y-2 text-sm">{editorialSources.map(([source, count]) => <li key={source}><Link className="underline" href={source}>{getComparison(source.slice(6))?.title ?? source}</Link> · {count}</li>)}</ol> : <p className="mt-2 text-sm text-muted-foreground">Noch keine zugeordneten Artikel-Klicks in diesem Zeitraum.</p>}</section>
      <section className="mt-8"><h2 className="text-xl font-bold">Quellseiten und CTA-Positionen</h2><p className="mt-2 text-sm text-muted-foreground">Die Tabelle zeigt bis zu 200 Quell-/Positionskombinationen; Bereichssummen berücksichtigen alle. Vergleiche und Artikel: /blog/… · Linkjagd-Sammlung: /linkjagd. Fehlende oder ungültige Quellen werden als unbekannt gezählt. Die Quelle wird durch die Linkbeschriftung übergeben und ist keine manipulationssichere Herkunftsbestätigung.</p>{contexts.length ? <div className="mt-4 overflow-x-auto"><table className="min-w-full text-left text-sm"><thead><tr>{["Quelle", "Position", "Aufrufe", "Partnerlink", "Offiziell"].map((label) => <th key={label} className="p-3">{label}</th>)}</tr></thead><tbody>{contexts.slice(0, 200).map((row) => <tr key={row.source + row.position} className="border-t border-border"><td className="p-3">{row.source}</td><td className="p-3">{row.position}</td><td className="p-3">{row.count}</td><td className="p-3">{row.affiliate}</td><td className="p-3">{row.official}</td></tr>)}</tbody></table></div> : <p className="mt-3 text-sm text-muted-foreground">Für diesen Zeitraum sind noch keine zugeordneten Klicks vorhanden.</p>}</section>
      <h2 className="mt-10 text-xl font-bold">Tools nach Anbieter-Klicks</h2>
      <div className="mt-4 overflow-x-auto rounded-2xl border border-border">
        <table className="min-w-full text-sm">
          <thead className="bg-card text-left text-muted-foreground">
            <tr>
              <th className="px-3 py-2 font-medium">Tool</th>
              <th className="px-3 py-2 font-medium">7 Tage</th>
              <th className="px-3 py-2 font-medium">30 Tage</th>
              <th className="px-3 py-2 font-medium">Partnerprogramm</th>
            </tr>
          </thead>
          <tbody>
            {rows.slice(0, 200).map((row) => (
              <tr key={row.id} className="border-t border-border">
                <td className="px-3 py-2">
                  <Link href={`/admin/tools/${row.id}`} className="font-medium hover:underline">{row.name}</Link>
                </td>
                <td className="px-3 py-2">{row.days7}</td>
                <td className="px-3 py-2">{row.days30}</td>
                <td className="px-3 py-2">{programPresenceLabel(row.programPresence)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
