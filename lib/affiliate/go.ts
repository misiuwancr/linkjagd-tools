import { decideRedirect } from "@/lib/affiliate/redirect";
import type { AffiliateProgram, Tool } from "@/db/schema";
import { utcDay } from "@/lib/utils";

export type GoLoadResult = {
  tool: Pick<Tool, "id" | "publishStatus" | "originalUrl"> | null;
  programs: Pick<AffiliateProgram, "id" | "affiliateUrl" | "status" | "isActive" | "priority">[];
};

export type GoResult =
  | { status: 302; location: string }
  | { status: 404; body: string };

const unavailable = "Für dieses Tool gibt es keine Weiterleitung.";

export async function handleGoRedirect(
  slug: string,
  deps: {
    load: (slug: string) => Promise<GoLoadResult>;
    track: (input: {
      toolId: string;
      programId: string | null;
      kind: "affiliate" | "official";
      day: string;
    }) => Promise<void>;
    siteHost?: string;
    now?: Date;
  },
): Promise<GoResult> {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) {
    return { status: 404, body: unavailable };
  }
  const loaded = await deps.load(slug);
  const decision = decideRedirect(loaded.tool, loaded.programs, deps.siteHost);
  if (!decision.ok) return { status: 404, body: unavailable };
  try {
    await deps.track({
      toolId: decision.toolId,
      programId: decision.programId,
      kind: decision.kind,
      day: utcDay(deps.now),
    });
  } catch {
    // Der Zähler darf die Weiterleitung nicht verhindern und speichert keine Personendaten.
  }
  return { status: 302, location: decision.location };
}
