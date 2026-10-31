import Link from "next/link";
import { getDb } from "@/db/client";
import { listClickStats } from "@/lib/tools/repository";
import { programPresenceLabel } from "@/lib/labels";
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
  const sort = searchParams.sort === "30" ? "30" : "7";
  const rows = await listClickStats(await getDb(), shift(7), shift(30));
  rows.sort((a, b) => (sort === "30" ? b.days30 - a.days30 : b.days7 - a.days7) || a.name.localeCompare(b.name, "de"));
  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight">Klicks</h1>
      <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
        Gezählt werden nur Aufrufe von /go. Keine Reichweite, keine Personen. Die Partner-Spalte sagt, ob eine öffentliche Programmseite bekannt ist.
      </p>
      <div className="mt-4 flex gap-2 text-sm">
        <Link href="/admin/klicks?sort=7" className={sort === "7" ? "font-semibold text-hunt" : "text-muted-foreground"}>7 Tage</Link>
        <Link href="/admin/klicks?sort=30" className={sort === "30" ? "font-semibold text-hunt" : "text-muted-foreground"}>30 Tage</Link>
      </div>
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
