import { describe, expect, it } from "vitest";
import { softwareOffer, toolMetaTitle } from "@/lib/seo";

describe("Tool-Titel und Angebote", () => {
  it("kürzt lange Titel und erfindet keinen Preis", () => {
    expect(toolMetaTitle("Otter").length).toBeLessThanOrEqual(65);
    expect(toolMetaTitle("Otter")).toContain("Linknarr");
    expect(toolMetaTitle("Ein sehr langer Werkzeugname der nicht in eine Zeile passt").length).toBeLessThanOrEqual(65);
    expect(softwareOffer("free")).toMatchObject({ price: "0" });
    expect(softwareOffer("freemium")).toBeNull();
    expect(softwareOffer("paid")).toBeNull();
  });
});