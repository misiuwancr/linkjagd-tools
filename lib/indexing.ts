export type RobotsDirective = { index: boolean; follow: boolean };

/**
 * Produktion bleibt indexierbar, solange INDEXING_ENABLED nicht ausdrücklich aus ist.
 * Vorschau und der lokale Rechner sind immer noindex, unabhängig von diesem Schalter.
 */
export function indexingPolicy(env: { [key: string]: string | undefined } = process.env): { index: boolean; reason: "production" | "switch" | "preview" | "local" } {
  if (env.VERCEL_ENV === "preview") return { index: false, reason: "preview" };
  if (env.VERCEL_ENV !== "production") return { index: false, reason: "local" };
  const flag = (env.INDEXING_ENABLED ?? "").trim().toLowerCase();
  if (flag === "0" || flag === "false" || flag === "aus") return { index: false, reason: "switch" };
  return { index: true, reason: "production" };
}

export function robotsDirective(index: boolean): RobotsDirective {
  return index ? { index: true, follow: true } : { index: false, follow: true };
}

export function toolIsIndexable(input: { globalIndex: boolean; allowIndex: boolean; published: boolean }) {
  return input.globalIndex && input.published && input.allowIndex;
}
