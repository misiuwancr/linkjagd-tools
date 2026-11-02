import { describe, expect, it } from "vitest";
import { createRetryingFetch, isRetryableDbError } from "@/db/http";

describe("Datenbank-Netz", () => {
  it("fragt zustandsbehaftete Datenbankantworten immer frisch ab", async () => {
    let calls = 0;
    let cached: string | undefined;
    const fetchImpl = (async (_input, init) => {
      if (init?.cache !== "no-store" && cached) return new Response(cached);
      const value = `stream-${++calls}`;
      cached = value;
      return new Response(value);
    }) as typeof fetch;
    const request = createRetryingFetch(fetchImpl);
    const first = await request(new Request("https://example.test/v3/pipeline", { method: "POST", body: "{}" }));
    const second = await request("https://example.test/v3/pipeline", { method: "POST", body: "{}", cache: "force-cache" });
    expect(await first.text()).toBe("stream-1");
    expect(await second.text()).toBe("stream-2");
  });

  it("wiederholt Timeouts und gibt danach auf", async () => {
    expect(isRetryableDbError(Object.assign(new Error("connect ETIMEDOUT 3.123.220.3:443"), { name: "TypeError" }))).toBe(true);
    expect(isRetryableDbError(new Error("SQL constraint failed"))).toBe(false);
    let calls = 0;
    const fetchImpl = (async () => {
      calls += 1;
      if (calls < 3) throw new TypeError("fetch failed");
      return new Response("ok", { status: 200 });
    }) as typeof fetch;
    const retrying = createRetryingFetch(fetchImpl, { timeoutMs: 50, attempts: 3 });
    const response = await retrying("https://example.test");
    expect(response.status).toBe(200);
    expect(calls).toBe(3);
  });
});
