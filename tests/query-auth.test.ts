import fs from "fs";
import { describe, expect, it } from "vitest";
import { bearerMatches, roleAllows } from "@/lib/auth/roles";
import { isProtectedAdminPath } from "@/lib/auth/paths";
import { safeAdminNext } from "@/lib/auth/token";
import { directoryHref, publicListQuery } from "@/lib/tools/query";
import { normalizeSearch, slugify } from "@/lib/utils";

describe("Suche und Filter", () => {
  it("liest deutsche URL-Parameter", () => {
    const query = publicListQuery({
      q: "  Bild  ",
      kategorie: "bildgenerierung",
      preis: "kostenlos",
      sort: "alphabetisch",
      seite: "2",
    });
    expect(query).toMatchObject({
      q: "Bild",
      categorySlug: "bildgenerierung",
      pricing: "free",
      sort: "alpha",
      page: 2,
      status: "published",
    });
  });

  it("verwirft unbekannte Filter und erzwingt veröffentlichte Tools", () => {
    const query = publicListQuery({ kategorie: "../admin", preis: "gratis", sort: "votes", seite: "-3" });
    expect(query.categorySlug).toBe("");
    expect(query.pricing).toBe("");
    expect(query.sort).toBe("newest");
    expect(query.page).toBe(1);
    expect(query.status).toBe("published");
  });

  it("baut teilbare Filter-URLs", () => {
    const query = publicListQuery({ q: "chat", kategorie: "ki-chatbots", preis: "freemium", sort: "beliebteste", seite: "3" });
    expect(directoryHref("/tools", query)).toBe("/tools?q=chat&kategorie=ki-chatbots&preis=freemium&sort=beliebteste&seite=3");
  });

  it("faltet Umlaute für die Suche", () => {
    expect(slugify("Audio und Sprache")).toBe("audio-und-sprache");
    expect(normalizeSearch("Größe fürs Üben")).toContain("groesse");
  });
});

describe("Admin-Schutz", () => {
  it("unterscheidet Rollen", () => {
    expect(roleAllows("admin", "editor")).toBe(true);
    expect(roleAllows("admin", "admin")).toBe(true);
    expect(roleAllows("editor", "editor")).toBe(true);
    expect(roleAllows("editor", "admin")).toBe(false);
  });

  it("schützt Admin-Routen und lässt die Anmeldung offen", () => {
    expect(isProtectedAdminPath("/admin")).toBe(true);
    expect(isProtectedAdminPath("/admin/tools")).toBe(true);
    expect(isProtectedAdminPath("/admin/login")).toBe(false);
    expect(isProtectedAdminPath("/api/admin/irgendwas")).toBe(true);
    expect(isProtectedAdminPath("/tools")).toBe(false);
    expect(isProtectedAdminPath("/go/nordlicht-chat")).toBe(false);
  });

  it("verhindert offene Weiterleitungen nach dem Login", () => {
    expect(safeAdminNext("/admin/tools")).toBe("/admin/tools");
    expect(safeAdminNext("https://evil.example")).toBe("/admin");
    expect(safeAdminNext("//evil.example")).toBe("/admin");
    expect(safeAdminNext("/admin/login")).toBe("/admin");
  });

  it("verlangt ein konfiguriertes Import-Token", () => {
    expect(bearerMatches("Bearer geheim", undefined)).toBe("missing_config");
    expect(bearerMatches("Bearer geheim", "geheim")).toBe("ok");
    expect(bearerMatches("Bearer falsch", "geheim")).toBe("unauthorized");
    expect(bearerMatches(null, "geheim")).toBe("unauthorized");
  });
});

describe("Klick-Tabelle", () => {
  it("speichert keine IP, kein Cookie und keinen User-Agent", () => {
    const sql = fs.readFileSync("migrations/0001_init.sql", "utf8").toLowerCase();
    expect(sql).not.toMatch(/\bip_address\b|\buser_agent\b|\bcookie\b/);
    expect(sql).toContain("create table click_daily");
  });
});
