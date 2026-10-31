import Link from "next/link";
import { getDb } from "@/db/client";
import { listSubscribers } from "@/lib/tools/repository";

export const dynamic = "force-dynamic";

export default async function AdminNewsletterPage() {
  const rows = await listSubscribers(await getDb());
  return (
    <div>
      <div className="flex items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Newsletter</h1>
          <p className="mt-2 text-sm text-muted-foreground">{rows.length} Adressen. Bestätigt zählt erst nach dem Link.</p>
        </div>
        <Link href="/admin/newsletter/export" className="rounded-full border border-border px-4 py-2 text-sm">
          CSV
        </Link>
      </div>
      <div className="mt-6 overflow-x-auto rounded-2xl border border-border">
        <table className="min-w-full text-sm">
          <thead className="bg-card text-left text-muted-foreground">
            <tr>
              <th className="px-3 py-2 font-medium">E-Mail</th>
              <th className="px-3 py-2 font-medium">Status</th>
              <th className="px-3 py-2 font-medium">Angelegt</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id} className="border-t border-border">
                <td className="px-3 py-2">{row.email}</td>
                <td className="px-3 py-2">{row.status === "confirmed" ? "Bestätigt" : "Offen"}</td>
                <td className="px-3 py-2">{row.createdAt.toLocaleDateString("de-DE")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
