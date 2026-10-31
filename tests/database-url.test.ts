import { describe, expect, it } from "vitest";
import { adminPasswordStatus, resolveAppDatabase, resolveLocalDatabase, sessionSecretStatus } from "@/db/resolve";
import { publicExportRow } from "@/db/transfer";

describe("Datenbank-Ziel", () => {
  it("nutzt lokal die Datei und Turso nur mit Token", () => {
    expect(resolveAppDatabase({ DATABASE_URL: "file:./data/linkjagd.db" }).kind).toBe("file");
    expect(resolveAppDatabase({}).url).toBe("file:./data/linkjagd.db");
    expect(() => resolveAppDatabase({ TURSO_DATABASE_URL: "libsql://example.turso.io" })).toThrow(/TURSO_AUTH_TOKEN/);
    expect(
      resolveAppDatabase({ TURSO_DATABASE_URL: "libsql://example.turso.io", TURSO_AUTH_TOKEN: "token" }).kind,
    ).toBe("turso");
    expect(() => resolveAppDatabase({ VERCEL: "1" })).toThrow(/TURSO_DATABASE_URL/);
    expect(resolveLocalDatabase({ DATABASE_URL: "file:./data/linkjagd.db" }).url).toContain("file:");
  });

  it("lehnt Platzhalter-Geheimnisse ab und exportiert kein Passwort", () => {
    expect(sessionSecretStatus({ JWT_SECRET: "ersetze-mich-mit-einem-langen-geheimnis" })).toBe("placeholder");
    expect(sessionSecretStatus({ JWT_SECRET: "a".repeat(32) })).toBe("ok");
    expect(adminPasswordStatus({ ADMIN_PASSWORD: "kurz" })).toBe("missing");
    const row = publicExportRow("users", { id: "1", email: "a@b.c", password_hash: "geheim", role: "admin" });
    expect(row).not.toHaveProperty("password_hash");
    expect(row.email).toBe("a@b.c");
  });
});
