const RETRYABLE = /ETIMEDOUT|ECONNRESET|EAI_AGAIN|ENETUNREACH|fetch failed|AbortError|network|timed out|socket|HTTP 5/i;

export function isRetryableDbError(error: unknown) {
  const name = error instanceof Error ? error.name : "";
  const message = error instanceof Error ? error.message : String(error);
  return RETRYABLE.test(`${name} ${message}`);
}

function wait(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function createRetryingFetch(
  baseFetch: typeof fetch = fetch,
  options: { timeoutMs?: number; attempts?: number } = {},
) {
  const timeoutMs = options.timeoutMs ?? 5000;
  const attempts = options.attempts ?? 3;
  return async function retryingFetch(input: RequestInfo | URL, init?: RequestInit) {
    let last: unknown;
    for (let attempt = 1; attempt <= attempts; attempt += 1) {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeoutMs);
      const parent = init?.signal;
      const onParentAbort = () => controller.abort();
      parent?.addEventListener("abort", onParentAbort);
      try {
        // Hrana carries stream/session state. Next.js 14 also caches POST fetches;
        // replaying a cached response can leave the next request with an invalid baton.
        const response = await baseFetch(input, { ...init, cache: "no-store", signal: controller.signal });
        if (response.status >= 500 && attempt < attempts) {
          last = new Error(`HTTP ${response.status}`);
          await wait(150 * attempt);
          continue;
        }
        return response;
      } catch (error) {
        last = error;
        if (parent?.aborted || attempt >= attempts || !isRetryableDbError(error)) throw error;
        await wait(150 * attempt);
      } finally {
        clearTimeout(timer);
        parent?.removeEventListener("abort", onParentAbort);
      }
    }
    throw last instanceof Error ? last : new Error("Datenbank nicht erreichbar.");
  };
}
