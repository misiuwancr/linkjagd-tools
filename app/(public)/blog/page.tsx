import type { Metadata } from "next";
import Link from "next/link";
import { getDb } from "@/db/client";
import { listPublishedNews, publishedBlogCount } from "@/lib/tools/repository";
import { Pagination } from "@/components/directory";
import { publicListQuery } from "@/lib/tools/query";

export const revalidate = 60;

export const metadata: Metadata = {
  title: "Blog",
  description: "Notizen der Redaktion von Linkjagd Tools. Es werden keine Artikel erfunden.",
  alternates: { canonical: "/blog" },
};

export default async function BlogPage({ searchParams }: { searchParams: Record<string, string | string[] | undefined> }) {
  const database = await getDb();
  const total = await publishedBlogCount(database);
  const requested = publicListQuery(searchParams);
  const query = publicListQuery({}, { page: Math.min(requested.page, Math.max(1, Math.ceil(total / 24))) });
  const news = await listPublishedNews(database, 24, (query.page - 1) * 24);
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
      <Pagination query={query} total={total} basePath="/blog" />
    </div>
  );
}
