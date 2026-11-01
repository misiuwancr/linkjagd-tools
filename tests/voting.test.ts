import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { randomUUID } from "node:crypto";
import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import { sql } from "drizzle-orm";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as schema from "@/db/schema";
import { applyMigrations } from "@/db/migrate";
import { castVote, voteTotal, voterCookie, voterHash, trustedVoterIp, votingEnabled } from "@/lib/voting";

async function setup() {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "linkjagd-vote-"));
  const client = createClient({ url: `file:${path.join(directory, randomUUID() + ".db")}` });
  await applyMigrations(client);
  expect((await client.execute("select name from sqlite_master where name = 'tool_votes'")).rows).toHaveLength(0);
  await client.executeMultiple(fs.readFileSync("migrations/manual/0008_anonymous_votes.sql", "utf8"));
  await client.execute("insert into tools (id,name,slug,original_url,domain,short_description_de,created_at,updated_at) values ('a','A','a','https://example.com','example.com','Test',0,0), ('b','B','b','https://example.org','example.org','Test',0,0)");
  return { client, db: drizzle(client, { schema }) };
}
afterEach(() => vi.unstubAllEnvs());
describe("anonyme Stimmen auf isolierter Vorschau-Datenbank", () => {
  it("aktiviert nichts ohne Freigabe und akzeptiert keine gefälschten Proxy-Header", () => {
    vi.stubEnv("ANONYMOUS_VOTING_ENABLED", "false");
    expect(votingEnabled()).toBe(false);
    vi.stubEnv("VERCEL", "1");
    expect(trustedVoterIp(new Headers({ "x-forwarded-for": "1.2.3.4" }))).toBeNull();
    expect(trustedVoterIp(new Headers({ "x-vercel-forwarded-for": "1.2.3.4" }))).toBe("1.2.3.4");
  });
  it("signiert Cookies und trennt IP- und Cookie-Hashes", () => {
    const secret = "s".repeat(32);
    const cookie = voterCookie(undefined, secret);
    expect(voterCookie(cookie, secret)).toBe(cookie);
    expect(voterCookie(cookie.replace(/.$/, "x"), secret)).not.toBe(cookie);
    expect(voterHash("ip", "value", secret)).not.toBe(voterHash("cookie", "value", secret));
  });
  it("zählt Startwert und echte Stimmen, verhindert Cookie- und IP-Doppelstimmen", async () => {
    const { client, db } = await setup();
    try {
      expect(await voteTotal(db, "a")).toEqual({ count: 1, realVotes: 0 });
      expect(await castVote(db, { toolId: "a", cookieHash: "c1", ipHash: "ip1", now: 100 })).toBe("created");
      expect(await castVote(db, { toolId: "a", cookieHash: "c1", ipHash: "ip2", now: 100 })).toBe("duplicate");
      expect(await castVote(db, { toolId: "a", cookieHash: "c2", ipHash: "ip1", now: 100 })).toBe("duplicate");
      expect(await castVote(db, { toolId: "b", cookieHash: "c1", ipHash: "ip1", now: 100 })).toBe("created");
      expect(await voteTotal(db, "a")).toEqual({ count: 2, realVotes: 1 });
      expect(await voteTotal(db, "b")).toEqual({ count: 2, realVotes: 1 });
    } finally { client.close(); }
  });
  it("begrenzt Versuche dauerhaft und setzt das Stundenfenster zurück", async () => {
    const { client, db } = await setup();
    try {
      for (let n = 0; n < 10; n++) await castVote(db, { toolId: "a", cookieHash: `c${n}`, ipHash: "ip", now: 0 });
      expect(await castVote(db, { toolId: "b", cookieHash: "new", ipHash: "ip", now: 0 })).toBe("limited");
      expect(await castVote(db, { toolId: "b", cookieHash: "new", ipHash: "ip", now: 3_600_000 })).toBe("created");
      expect(await voteTotal(db, "b")).toEqual({ count: 2, realVotes: 1 });
      expect((await db.all(sql`select * from vote_rate_limits`)).length).toBe(2);
    } finally { client.close(); }
  });
});
