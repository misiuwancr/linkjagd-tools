import type { Metadata } from "next";
import { AiNewsCards } from "@/components/ai-news";
import { Pagination } from "@/components/directory";
import { publishedAiNews } from "@/lib/ai-news";
import { publicListQuery } from "@/lib/tools/query";

export const metadata: Metadata = { title: "KI-News", description: "KI-Nachrichten mit verlinkten Originalquellen.", alternates: { canonical: "/news" } };
export const revalidate = 60;
export default function NewsPage({ searchParams }: { searchParams: Record<string, string | string[] | undefined> }) {
  const news = publishedAiNews();
  const requested = publicListQuery(searchParams);
  const query = publicListQuery({}, { pageSize: 12, page: Math.min(requested.page, Math.max(1, Math.ceil(news.length / 12))) });
  return <div className="page-wrap py-14"><h1 className="text-4xl font-bold">KI-News</h1>
    <p className="mt-3 text-muted-foreground">Meldungen aus der KI-Welt – mit Einordnung und Originalquelle.</p>
    <AiNewsCards news={news.slice((query.page - 1) * 12, query.page * 12)} /><Pagination query={query} total={news.length} basePath="/news" />
  </div>;
}
