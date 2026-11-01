import { NextRequest, NextResponse } from "next/server";
import { getDb } from "@/db/client";
import { getToolBySlug } from "@/lib/tools/repository";
import { castVote, trustedVoterIp, voteTotal, voterCookie, voterHash, votingEnabled } from "@/lib/voting";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";
const json = (body: unknown, status = 200) => NextResponse.json(body, { status, headers: { "Cache-Control": "no-store" } });

async function published(slug: string) {
  const database = await getDb();
  const tool = await getToolBySlug(database, slug);
  return tool?.publishStatus === "published" && !tool.isExample ? { database, tool } : null;
}

export async function GET(_request: NextRequest, { params }: { params: { slug: string } }) {
  if (!votingEnabled()) return json({ enabled: false });
  try {
    const entry = await published(params.slug);
    if (!entry) return json({ error: "Tool nicht gefunden." }, 404);
    return json({ enabled: true, ...await voteTotal(entry.database, entry.tool.id) });
  } catch { return json({ error: "Voting ist vorübergehend nicht verfügbar." }, 503); }
}

export async function POST(request: NextRequest, { params }: { params: { slug: string } }) {
  if (!votingEnabled()) return json({ error: "Voting ist noch nicht freigeschaltet." }, 503);
  const origin = request.headers.get("origin");
  if (!origin || origin !== request.nextUrl.origin) return json({ error: "Ungültiger Ursprung." }, 403);
  const ip = trustedVoterIp(request.headers);
  if (!ip) return json({ error: "Voting ist hier nicht verfügbar." }, 503);
  try {
    const entry = await published(params.slug);
    if (!entry) return json({ error: "Tool nicht gefunden." }, 404);
    const secret = process.env.VOTE_HASH_SECRET!;
    const cookie = voterCookie(request.cookies.get("linkjagd-voter")?.value, secret);
    const result = await castVote(entry.database, {
      toolId: entry.tool.id, cookieHash: voterHash("cookie", cookie, secret), ipHash: voterHash("ip", ip, secret), now: Date.now(),
    });
    if (result === "limited") return json({ error: "Zu viele Versuche. Bitte versuche es in einer Stunde erneut." }, 429);
    const response = json({ ...await voteTotal(entry.database, entry.tool.id), voted: true, duplicate: result === "duplicate" });
    response.cookies.set("linkjagd-voter", cookie, { httpOnly: true, secure: request.nextUrl.protocol === "https:", sameSite: "lax", path: "/", maxAge: 60 * 60 * 24 * 365 });
    return response;
  } catch { return json({ error: "Deine Stimme konnte nicht gespeichert werden." }, 503); }
}
