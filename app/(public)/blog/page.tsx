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
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Redaktion</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">Blog</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">Nur Beiträge, die die Redaktion veröffentlicht hat.</p>
      {news.length === 0 ? (
        <p className="mt-8 rounded-2xl border border-dashed border-border bg-card p-6 text-sm">Noch kein veröffentlichtes Stück.</p>
      ) : (
        <ul className="mt-8 grid gap-4">
          {news.map((item) => (
            <li key={item.id}>
              <Link href={`/blog/${item.slug}`} className="block rounded-2xl border border-border bg-card p-5 hover:border-hunt/40">
                <h2 className="text-2xl font-bold tracking-tight">{item.title}</h2>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.excerpt}</p>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
