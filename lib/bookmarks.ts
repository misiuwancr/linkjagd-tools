export const BOOKMARK_KEY = "linkjagd-merkliste";

export function parseBookmarkSlugs(value: string | undefined) {
  if (!value) return [];
  const slugs = value
    .split(",")
    .map((item) => item.trim().toLowerCase())
    .filter((item) => /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(item));
  return [...new Set(slugs)].slice(0, 100);
}

export function bookmarkHref(slugs: string[]) {
  if (slugs.length === 0) return "/merkliste";
  return `/merkliste?tools=${slugs.join(",")}`;
}
