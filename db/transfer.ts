export const DATA_TABLES = [
  "users",
  "categories",
  "tags",
  "tools",
  "tool_categories",
  "tool_tags",
  "affiliate_programs",
  "click_daily",
  "news_posts",
] as const;

export type DataTable = (typeof DATA_TABLES)[number];

const SECRET_COLUMNS: Record<string, string[]> = {
  users: ["password_hash"],
};

export function publicExportRow(table: string, row: Record<string, unknown>) {
  const hidden = new Set(SECRET_COLUMNS[table] ?? []);
  const copy: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(row)) {
    if (hidden.has(key)) continue;
    copy[key] = typeof value === "bigint" ? Number(value) : value;
  }
  return copy;
}

export function sqlCell(value: unknown) {
  if (typeof value === "bigint") return Number(value);
  if (value instanceof Uint8Array) return Buffer.from(value);
  return value ?? null;
}
