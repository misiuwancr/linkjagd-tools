export type DatabaseTarget = {
  url: string;
  authToken?: string;
  kind: "turso" | "file";
};

const PLACEHOLDER = "ersetze-mich";

export function resolveAppDatabase(env: NodeJS.ProcessEnv = process.env): DatabaseTarget {
  const turso = env.TURSO_DATABASE_URL?.trim() ?? "";
  if (turso) {
    const authToken = env.TURSO_AUTH_TOKEN?.trim() ?? "";
    if (!authToken) {
      throw new Error("TURSO_AUTH_TOKEN fehlt, obwohl TURSO_DATABASE_URL gesetzt ist.");
    }
    if (!/^libsql:\/\//.test(turso) && !/^https:\/\//.test(turso)) {
      throw new Error("TURSO_DATABASE_URL muss mit libsql:// oder https:// beginnen.");
    }
    return { url: turso, authToken, kind: "turso" };
  }
  const local = env.DATABASE_URL?.trim() || "file:./data/linkjagd.db";
  if (env.VERCEL === "1") {
    throw new Error(
      "Auf Vercel TURSO_DATABASE_URL und TURSO_AUTH_TOKEN setzen. Eine SQLite-Datei überlebt dort keinen Neustart.",
    );
  }
  return { url: local, kind: "file" };
}

export function resolveLocalDatabase(env: NodeJS.ProcessEnv = process.env): DatabaseTarget {
  const local = env.DATABASE_URL?.trim() || "file:./data/linkjagd.db";
  if (!local.startsWith("file:")) {
    throw new Error("DATABASE_URL muss für Export und Übertragung eine file:-Adresse der lokalen SQLite-Datei sein.");
  }
  return { url: local, kind: "file" };
}

export function sessionSecretStatus(env: NodeJS.ProcessEnv = process.env): "ok" | "missing" | "placeholder" {
  const value = env.JWT_SECRET?.trim() ?? "";
  if (value.length < 16) return "missing";
  if (value.toLowerCase().includes(PLACEHOLDER)) return "placeholder";
  return "ok";
}

export function adminPasswordStatus(env: NodeJS.ProcessEnv = process.env): "ok" | "missing" | "placeholder" {
  const value = env.ADMIN_PASSWORD ?? "";
  if (value.length < 12) return "missing";
  if (value.toLowerCase().includes(PLACEHOLDER)) return "placeholder";
  return "ok";
}
