import { describe, expect, it } from "vitest";
import { chooseCategory, EDITORIAL_TOP, isHomepageFresh } from "@/lib/taxonomy";
import { weeklyPopularVisible } from "@/lib/tools/popular";

describe("Kategorien und Top 20", () => {
  it("ordnet nach der bisherigen Kategorie und schiebt Zahlungs-APIs nicht in Code", () => {
    expect(chooseCategory(["ki-chatbots", "programmierung"], "ChatGPT beantwortet Fragen im Chat.").slug).toBe("chat-assistenten");
    expect(chooseCategory(["e-commerce"], "Zettle nimmt Zahlungen an der Kasse entgegen.").slug).toBe("e-commerce");
    expect(chooseCategory(["finanzen", "programmierung"], "finAPI verbindet Anwendungen mit Bankkonten.").slug).toBe("business-finanzen");
    expect(chooseCategory(["bildgenerierung", "videogenerierung"], "Runway erzeugt Videos.").slug).toBe("video");
    const review = chooseCategory(["finanzen", "recht"], "Die BaFin beaufsichtigt Banken und Versicherer.");
    expect(review.slug).toBe("spass-sonstiges");
    expect(review.review).toBe(true);
    expect(chooseCategory([], "Unklar").review).toBe(true);
  });

  it("lässt auf der Startseite nur beschriebene KI-Werkzeuge in Neu, nicht Kasse oder Fernwartung", () => {
    expect(isHomepageFresh("video", "Hailuo erzeugt kurze Videos aus Text oder einem Bild.")).toBe(true);
    expect(isHomepageFresh("e-commerce", "Zettle nimmt Zahlungen an der Kasse entgegen.")).toBe(false);
    expect(isHomepageFresh("code-entwicklung", "TightVNC ist eine Fernwartung.")).toBe(false);
    expect(isHomepageFresh("bild-design", "WordPress veröffentlicht Seiten.")).toBe(false);
  });

  it("nummeriert zwanzig bekannte Tools ohne Lücken und ohne erfundene Stimmen", () => {
    expect(EDITORIAL_TOP.map((item) => item.rank)).toEqual(Array.from({ length: 20 }, (_, index) => index + 1));
    expect(new Set(EDITORIAL_TOP.map((item) => item.slug)).size).toBe(20);
    expect(EDITORIAL_TOP.map((item) => item.slug).slice(0, 3)).toEqual(["chatgpt", "claude", "gemini"]);
    expect(weeklyPopularVisible(2)).toBe(false);
  });
});
