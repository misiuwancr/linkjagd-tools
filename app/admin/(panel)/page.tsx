import Link from "next/link";
import { getDb } from "@/db/client";
import { createEditorAction, saveNewsAction } from "@/lib/actions/admin";
import { requireUser } from "@/lib/auth/session";
import { Flash } from "@/components/admin/shell";
import { dashboardCounts } from "@/lib/tools/repository";

export const dynamic = "force-dynamic";

export default async function AdminHome({
  searchParams,
}: {
  searchParams: { gespeichert?: string; fehler?: string };
}) {
  const user = await requireUser("editor");
  const counts = await dashboardCounts(await getDb());
  const cards = [
    ["Veröffentlicht", counts.published],
    ["Ohne Partnerlink", counts.publishedWithoutCta],
    ["Entwürfe", counts.drafts],
    ["Moderation", counts.moderation],
    ["Archiv", counts.archived],
    ["Kategorien", counts.categories],
  ];
  return (
    <div>
      <h1 className="text-3xl font-semibold tracking-tight">Übersicht</h1>
      <p className="mt-2 text-sm text-muted-foreground">Werkzeuge, Partnerlinks und Entwürfe aus Import oder Einreichung.</p>
      <Flash gespeichert={searchParams.gespeichert} fehler={searchParams.fehler} />
      <div className="mt-6 grid gap-3 sm:grid-cols-3">
        {cards.map(([label, value]) => (
          <div key={label} className="rounded-2xl border border-border bg-white p-4">
            <p className="text-2xl font-semibold tabular-nums">{value}</p>
            <p className="text-sm text-muted-foreground">{label}</p>
          </div>
        ))}
      </div>
      <p className="mt-6 text-sm">
        <Link href="/admin/moderation" className="font-medium underline">
          Moderations-Warteschlange öffnen
        </Link>
      </p>

      <section id="meldungen" className="mt-12 rounded-3xl border border-border bg-white p-5">
        <h2 className="text-xl font-semibold">KI-News</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Manuelle Notiz für den Blog. Es wird keine Quelle automatisch gelesen.
        </p>
        <form action={saveNewsAction} className="mt-4 grid gap-3">
          <input name="title" placeholder="Titel" className="field" required />
          <textarea name="excerpt" placeholder="Kurztext" className="area" required />
          <textarea name="body" placeholder="Text" className="area" />
          <input name="sourceName" placeholder="Quellenname, nur als Text" className="field" />
          <select name="status" className="field" defaultValue="draft">
            <option value="draft">Entwurf</option>
            <option value="published">Veröffentlicht</option>
          </select>
          <button className="h-11 rounded-xl bg-ink text-sm font-semibold text-white" type="submit">
            Meldung speichern
          </button>
        </form>
      </section>

      {user.role === "admin" ? (
        <section className="mt-8 rounded-3xl border border-border bg-white p-5">
          <h2 className="text-xl font-semibold">Redaktionskonto</h2>
          <p className="mt-2 text-sm text-muted-foreground">Legt ein Konto mit der Rolle Redaktion an. Admins bleiben unangetastet.</p>
          <form action={createEditorAction} className="mt-4 grid gap-3 sm:grid-cols-2">
            <input name="email" type="email" required placeholder="E-Mail" className="field" />
            <input name="password" type="password" required minLength={12} placeholder="Passwort, mindestens 12 Zeichen" className="field" />
            <button className="h-11 rounded-xl border border-border text-sm font-semibold sm:col-span-2" type="submit">
              Konto anlegen
            </button>
          </form>
        </section>
      ) : null}
    </div>
  );
}
