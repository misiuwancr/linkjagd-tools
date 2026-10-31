import { describe, expect, it } from "vitest";
import { bookmarkHref, parseBookmarkSlugs } from "@/lib/bookmarks";

describe("Merkliste", () => {
  it("nimmt nur gültige Kurznamen in die Adresse", () => {
    expect(parseBookmarkSlugs("Notion, chatgpt, ../admin, chatgpt")).toEqual(["notion", "chatgpt"]);
    expect(bookmarkHref(["chatgpt", "notion"])).toBe("/merkliste?tools=chatgpt,notion");
    expect(bookmarkHref([])).toBe("/merkliste");
  });
});
