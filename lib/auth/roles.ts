import { timingSafeEqual } from "crypto";
import type { UserRole } from "@/db/schema";

const rank: Record<UserRole, number> = { editor: 1, admin: 2 };

export function roleAllows(actual: UserRole, required: UserRole) {
  return rank[actual] >= rank[required];
}

export function bearerMatches(header: string | null, token: string | undefined) {
  if (!token) return "missing_config" as const;
  const expected = `Bearer ${token}`;
  const actual = header ?? "";
  const left = Buffer.from(actual);
  const right = Buffer.from(expected);
  if (left.length !== right.length) return "unauthorized" as const;
  return timingSafeEqual(left, right) ? ("ok" as const) : ("unauthorized" as const);
}
