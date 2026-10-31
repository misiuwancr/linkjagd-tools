import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { submitTool } from "@/lib/actions/public";
import { listCategories } from "@/lib/tools/repository";

export const metadata: Metadata = {
  title: "Tool einreichen",
  description: "Schlage ein KI-Tool für die Redaktion vor. Es bleibt ein Entwurf, bis es geprüft wird.",
  alternates: { canonical: "/einreichen" },
};

export default async function SubmitPage({
  searchParams,
}: {
  searchParams: { fehler?: string; hinweis?: string };
}) {
  const categories = await listCategories(await getDb());
  return (
    <div className="page-wrap max-w-2xl py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Mitmachen</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">Tool einreichen</h1>
      <p className="mt-3 text-muted-foreground">
        Dein Vorschlag landet als Entwurf bei der Redaktion. Er wird nicht automatisch veröffentlicht und es wird keine Mail verschickt.
      </p>
      {searchParams.fehler ? (
        <p role="alert" className="mt-6 rounded-xl border border-red-800 bg-red-950 px-4 py-3 text-sm text-red-100">
          {searchParams.fehler}
        </p>
      ) : null}
      {searchParams.hinweis === "danke" ? (
        <p role="status" className="mt-6 rounded-xl border border-emerald-800 bg-emerald-950 px-4 py-3 text-sm text-emerald-100">
          Danke. Der Entwurf ist angekommen und noch nicht öffentlich.
        </p>
      ) : null}
      <form action={submitTool} className="mt-8 grid gap-4">
        <label className="grid gap-1 text-sm font-medium">
          Name
          <input name="name" required className="field" />
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Website
          <input name="originalUrl" type="url" required placeholder="https://" className="field" />
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Kurzbeschreibung
          <textarea name="shortDescriptionDe" required className="area" />
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Kategorie
          <select name="categoryId" className="field" defaultValue="">
            <option value="">Keine Angabe</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </label>
        <label className="grid gap-1 text-sm font-medium">
          E-Mail, falls wir nachfragen dürfen
          <input name="submitterEmail" type="email" className="field" />
        </label>
        <input name="firma" tabIndex={-1} autoComplete="off" className="hidden" aria-hidden="true" />
        <button type="submit" className="h-12 rounded-xl bg-primary text-sm font-semibold text-primary-foreground">
          Entwurf senden
        </button>
      </form>
    </div>
  );
}
