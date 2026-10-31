import { describe, expect, it } from "vitest";
import { germanFromHtml } from "@/lib/facts";
import { publicListQuery } from "@/lib/tools/query";

describe("Faktenleiste", () => {
  it("setzt Deutsch nur bei einem belegten Sprachhinweis", () => {
    expect(germanFromHtml("<html lang=\"de-DE\"><head></head>")).toBe("ja");
    expect(germanFromHtml("<link rel=\"alternate\" hreflang=\"de\" href=\"/de\">")).toBe("ja");
    expect(germanFromHtml("<html lang=\"en\"><p>Deutsch</p>")).toBeNull();
  });

  it("filtert Deutsch und Anmeldung über die Adresse", () => {
    const query = publicListQuery({ deutsch: "ja", anmeldung: "nein" });
    expect(query.germanUi).toBe("ja");
    expect(query.noSignup).toBe("nein");
    expect(publicListQuery({ deutsch: "vielleicht" }).germanUi).toBe("");
  });
});
