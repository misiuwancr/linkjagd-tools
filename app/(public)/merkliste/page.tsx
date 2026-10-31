import type { Metadata } from "next";
import Link from "next/link";
import { getDb } from "@/db/client";
import { BookmarkList } from "@/components/bookmark-list";
import { ToolCard } from "@/components/tool-card";
import { bookmarkHref, parseBookmarkSlugs } from "@/lib/bookmarks";
import { getToolBySlug } from "@/lib/tools/repository";
import { toPublicTool } from "@/lib/tools/public";

export const metadata: Metadata = {
  title: "Merkliste",
  description: "Gemerkte Tools bleiben in diesem Browser. Ein Link mit den Kurznamen lässt sich teilen.",
  robots: { index: false, follow: false },
};

export default async function BookmarkPage({
  searchParams,
}: {
  searchParams: { tools?: string };
}) {
  const slugs = parseBookmarkSlugs(searchParams.tools);
  const database = await getDb();
  const tools = [];
  for (const slug of slugs) {
    const record = await getToolBySlug(database, slug);
    if (record && record.publishStatus === "published" && !record.isExample) tools.push(toPublicTool(record));
  }
  return (
    <div className="page-wrap py-10 sm:py-14">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Lokal</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">Merkliste</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Ohne Konto. Die Liste liegt in diesem Browser. Zum Teilen steht die Auswahl in der Adresse.
      </p>
      {slugs.length > 0 ? (
        <p className="mt-4 text-sm">
          <Link href={bookmarkHref(tools.map((tool) => tool.slug))} className="underline">
            Diesen Stand teilen
          </Link>
        </p>
      ) : (
        <BookmarkList />
      )}
      <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {tools.map((tool) => (
          <ToolCard key={tool.id} tool={tool} />
        ))}
      </div>
    </div>
  );
}
