import Link from "next/link";
import { getDb } from "@/db/client";
import { saveNewsAction } from "@/lib/actions/content";
import { listAllNews } from "@/lib/tools/repository";

import { blogTopics, defaultPostEditorial, readPostEditorial } from "@/lib/blog-metadata";
import { getComparison } from "@/lib/comparisons";

export const dynamic = "force-dynamic";

export default async function AdminBlogPage({
  searchParams,
}: {
  searchParams: { id?: string; fehler?: string; gespeichert?: string };
}) {
  const database = await getDb();
  const posts = await listAllNews(database);
  const current = searchParams.id ? posts.find((post) => post.id === searchParams.id) : undefined;
  const editorial = current ? await readPostEditorial(database, current.id, current.slug) : defaultPostEditorial("");
  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight">Blog</h1>
      <p className="mt-2 text-sm text-muted-foreground">Entwürfe sind nicht öffentlich. Die erste Veröffentlichung setzt das Datum; spätere Bearbeitungen erhalten es.</p>
      {searchParams.fehler ? <p className="mt-4 text-sm text-red-300">{searchParams.fehler}</p> : null}
      {searchParams.gespeichert ? <p className="mt-4 text-sm">Gespeichert.</p> : null}
      {current && getComparison(current.slug) ? <p className="mt-4 rounded-xl border border-hunt p-4 text-sm">Dieser Vergleich wird im Code gepflegt. Die bestehende URL bleibt erhalten; Änderungen am Datenbanktext ersetzen das Vergleichstemplate nicht.</p> : null}
      <form key={current?.id ?? "neu"} action={saveNewsAction} className="mt-6 grid max-w-3xl gap-3">
        <input type="hidden" name="id" value={current?.id ?? ""} />
        <input name="title" required defaultValue={current?.title ?? ""} placeholder="Titel" className="field" />
        <input name="slug" defaultValue={current?.slug ?? ""} placeholder="Kurzname, leer = aus dem Titel" className="field" />
        <textarea name="excerpt" required defaultValue={current?.excerpt ?? ""} placeholder="Teaser" className="area" />
        <textarea name="body" defaultValue={current?.body ?? ""} placeholder="Markdown" className="area min-h-48" />
        <input name="coverImageUrl" defaultValue={current?.coverImageUrl ?? ""} placeholder="Cover-Bild-URL, https://" className="field" />
        <input name="seoTitle" defaultValue={current?.seoTitle ?? ""} placeholder="SEO-Titel, optional" className="field" />
        <input name="seoDescription" defaultValue={current?.seoDescription ?? ""} placeholder="SEO-Beschreibung, optional" className="field" />
        <input name="sourceName" defaultValue={current?.sourceName ?? ""} placeholder="Quellenname, optional" className="field" />
        <label className="grid gap-2 text-sm">Themenbereich<select name="topic" defaultValue={editorial.topic} className="field">{blogTopics.map((topic) => <option key={topic.value} value={topic.value}>{topic.label}</option>)}</select></label>
        <label className="grid gap-2 text-sm">Verknüpfte Tool-Kurznamen (Komma oder Leerzeichen)<input name="toolSlugs" defaultValue={editorial.toolSlugs.join(", ")} placeholder="z. B. zapier, make, n8n" className="field" /></label>
        <label className="grid gap-2 text-sm">Verwandte Artikel-Kurznamen (optional)<input name="relatedSlugs" defaultValue={editorial.relatedSlugs.join(", ")} className="field" /></label>
        <p className="text-sm leading-6 text-muted-foreground">Tool-Verknüpfung im Text: [Tool-Profil](/tools/kurzname). Anbieterlink: [Zum Anbieter](/go/kurzname). Aktive hinterlegte Partnerlinks werden auf der öffentlichen Seite automatisch als Anzeige gekennzeichnet. Keine eigenen Empfehlungsparameter erfinden. Inhalte und Quellen vor Veröffentlichung fachlich prüfen.</p>
        <select name="status" defaultValue={current?.status ?? "draft"} className="field">
          <option value="draft">Entwurf</option>
          <option value="published">Veröffentlicht</option>
        </select>
        <button type="submit" className="h-11 rounded-xl bg-primary text-sm font-semibold text-primary-foreground">
          Speichern
        </button>
      </form>
      <ul className="mt-8 divide-y divide-border rounded-2xl border border-border">
        {posts.map((post) => (
          <li key={post.id} className="flex items-center justify-between gap-3 px-4 py-3 text-sm">
            <Link href={`/admin/blog?id=${post.id}`} className="font-medium hover:underline">
              {post.title}
            </Link>
            <span className="text-muted-foreground">{post.status === "published" ? "Öffentlich" : "Entwurf"}</span>
          </li>
        ))}
      </ul>
      {posts.length === 0 ? <p className="mt-4 text-sm text-muted-foreground">Noch kein Beitrag.</p> : null}
    </div>
  );
}
