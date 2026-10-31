"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { BOOKMARK_KEY, bookmarkHref, parseBookmarkSlugs } from "@/lib/bookmarks";

export function BookmarkList() {
  const router = useRouter();
  useEffect(() => {
    try {
      const raw = window.localStorage.getItem(BOOKMARK_KEY);
      const slugs = parseBookmarkSlugs(raw ? (JSON.parse(raw) as string[]).join(",") : "");
      if (slugs.length > 0) router.replace(bookmarkHref(slugs));
    } catch {
      // Eine defekte lokale Liste bleibt leer.
    }
  }, [router]);
  return <p className="mt-6 text-sm text-muted-foreground">Noch nichts gemerkt. Auf einer Toolseite liegt der Schalter Merken.</p>;
}
