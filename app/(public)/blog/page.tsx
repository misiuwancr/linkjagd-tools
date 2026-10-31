import type { Metadata } from "next";
import Link from "next/link";
import { getDb } from "@/db/client";
import { listPublishedNews } from "@/lib/tools/repository";

export const revalidate = 60;

export const metadata: Metadata = {
  title: "Blog",
  description: "Notizen der Redaktion von Linkjagd Tools. Es werden keine Artikel erfunden.",
  alternates: { canonical: "/blog" },
};

export default async function BlogPage() {
  const news = await listPublishedNews(await getDb(), 24);
  return (
    <div className="page-wrap py-12 sm:py-16">
      <h1 className="text-center text-4xl font-bold tracking-tight sm:text-5xl">Blog</h1>
      <p className="mx-auto mt-3 max-w-2xl text-center text-muted-foreground">Nur Beiträge, die die Redaktion veröffentlicht hat.</p>
      {news.length === 0 ? (
        <p className="mt-8 rounded-2xl border border-dashed border-border bg-card p-6 text-center text-sm">Noch kein veröffentlichtes Stück.</p>
      ) : (
        <ul className="mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {news.map((item) => (
            <li key={item.id}>
              <Link href={`/blog/${item.slug}`} className="block h-full rounded-2xl border border-border bg-card p-5 hover:border-hunt/40">
                <p className="text-xs uppercase tracking-[0.14em] text-hunt">Beitrag</p>
                <h2 className="mt-2 text-xl font-bold tracking-tight">{item.title}</h2>
                <p className="mt-2 line-clamp-3 text-sm leading-6 text-muted-foreground">{item.excerpt}</p>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
