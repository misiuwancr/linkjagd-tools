"use client";

import { useEffect, useState } from "react";
import { BOOKMARK_KEY } from "@/lib/bookmarks";

function read(): string[] {
  try {
    const raw = window.localStorage.getItem(BOOKMARK_KEY);
    const parsed = raw ? (JSON.parse(raw) as unknown) : [];
    return Array.isArray(parsed) ? parsed.filter((item) => typeof item === "string") : [];
  } catch {
    return [];
  }
}

export function BookmarkButton({ slug }: { slug: string }) {
  const [on, setOn] = useState(false);
  useEffect(() => {
    setOn(read().includes(slug));
  }, [slug]);
  return (
    <button
      type="button"
      aria-pressed={on}
      onClick={() => {
        const next = read().filter((item) => item !== slug);
        if (!on) next.push(slug);
        window.localStorage.setItem(BOOKMARK_KEY, JSON.stringify(next));
        setOn(!on);
      }}
      className="inline-flex h-9 items-center rounded-full border border-border px-3 text-sm font-medium hover:border-hunt/40"
    >
      {on ? "Gemerkt" : "Merken"}
    </button>
  );
}
