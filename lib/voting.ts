import { createHmac, randomUUID, timingSafeEqual } from "node:crypto";
import { isIP } from "node:net";
import { sql } from "drizzle-orm";
import type { AppDatabase } from "@/db/client";

export function votingEnabled() {
  return process.env.ANONYMOUS_VOTING_ENABLED === "true" && (process.env.VOTE_HASH_SECRET?.length ?? 0) >= 32;
}

export function voterHash(kind: string, value: string, secret: string) {
  return createHmac("sha256", secret).update(`${kind}:${value}`).digest("hex");
}

export function voterCookie(existing: string | undefined, secret: string) {
  const [id, signature] = (existing ?? "").split(".");
  const expected = id ? voterHash("cookie-signature", id, secret) : "";
  if (id && /^[0-9a-f-]{36}$/.test(id) && signature?.length === 64 && timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) return existing!;
  const next = randomUUID();
  return `${next}.${voterHash("cookie-signature", next, secret)}`;
}

export function trustedVoterIp(headers: Headers) {
  // Vercel overwrites this header; never trust arbitrary x-forwarded-for.
  const value = process.env.VERCEL === "1"
    ? headers.get("x-vercel-forwarded-for")?.split(",")[0]?.trim()
    : process.env.NODE_ENV !== "production" ? "127.0.0.1" : undefined;
  return value && isIP(value) ? value : null;
}

export async function voteTotal(database: AppDatabase, toolId: string) {
  const rows = await database.all<{ count: number }>(sql`select count(*) as count from tool_votes where tool_id = ${toolId}`);
  const realVotes = Number(rows[0]?.count ?? 0);
  return { count: realVotes + 1, realVotes };
}

export async function castVote(database: AppDatabase, input: { toolId: string; cookieHash: string; ipHash: string; now: number }) {
  const windowStart = Math.floor(input.now / 3_600_000) * 3_600_000;
  return database.transaction(async (tx) => {
    await tx.run(sql`delete from vote_rate_limits where window_start < ${windowStart - 86_400_000}`);
    const allowed = await tx.all(sql`insert into vote_rate_limits (ip_hash, window_start, attempts)
      values (${input.ipHash}, ${windowStart}, 1)
      on conflict(ip_hash, window_start) do update set attempts = attempts + 1 where attempts < 10
      returning attempts`);
    if (!allowed.length) return "limited" as const;
    const inserted = await tx.all(sql`insert into tool_votes (tool_id, cookie_hash, ip_hash, created_at)
      values (${input.toolId}, ${input.cookieHash}, ${input.ipHash}, ${input.now})
      on conflict do nothing returning tool_id`);
    return inserted.length ? "created" as const : "duplicate" as const;
  });
}
