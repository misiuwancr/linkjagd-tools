import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { listPublishedNews } from "@/lib/tools/repository";

export const revalidate = 60;

export const metadata: Metadata = {
  title: "Blog / KI-News",
  description: "Platz für spätere KI-Meldungen. In Phase 1 werden keine Artikel automatisch erzeugt.",
  alternates: { canonical: "/blog" },
};

export default async function BlogPage() {
  const news = await listPublishedNews(await getDb(), 24);
  return (
    <div className="page-wrap py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Blog</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">KI-News</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Automatische Meldungen sind vorbereitet, aber nicht gebaut. Es wird nichts gecrawlt und nichts erfunden.
      </p>
      {news.length === 0 ? (
        <div className="mt-8 rounded-2xl border border-dashed border-border bg-card p-6">
          <p className="font-medium">Noch keine Meldung.</p>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">
            Die Redaktion kann später eigene Notizen veröffentlichen. Eine Anbindung an Nachrichtenquellen gehört nicht zu Phase 1 und braucht vorher eine Prüfung von Nutzungsbedingungen und robots.txt.
          </p>
        </div>
      ) : (
        <div className="mt-8 grid gap-4">
          {news.map((item) => (
            <article key={item.id} className="rounded-2xl border border-border bg-card p-5">
              <h2 className="text-xl font-bold tracking-tight">{item.title}</h2>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.excerpt}</p>
              {item.body ? <p className="mt-4 whitespace-pre-wrap text-sm leading-7">{item.body}</p> : null}
              {item.sourceName ? <p className="mt-3 text-xs text-muted-foreground">Quelle: {item.sourceName}</p> : null}
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
