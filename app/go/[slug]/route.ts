import { NextResponse } from "next/server";
import { getDb } from "@/db/client";
import { handleGoRedirect } from "@/lib/affiliate/go";
import { recordClick, getToolBySlug } from "@/lib/tools/repository";
import { siteConfig } from "@/site.config";
import { clickContext } from "@/lib/affiliate/context";

export const dynamic = "force-dynamic";

function host() {
  try {
    return new URL(siteConfig.url).hostname;
  } catch {
    return undefined;
  }
}

async function redirect(request: Request, { params }: { params: { slug: string } }, head = false) {
  const database = await getDb();
  const url = new URL(request.url);
  const context = await clickContext(database, url.searchParams.get("quelle"), url.searchParams.get("position"));
  const result = await handleGoRedirect(params.slug, {
    siteHost: host(),
    context,
    officialOnly: url.searchParams.get("ziel") === "offiziell",
    skipTracking: head || request.headers.get("purpose") === "prefetch" || request.headers.get("sec-purpose")?.includes("prefetch"),
    load: async (slug) => {
      const tool = await getToolBySlug(database, slug);
      if (!tool) return { tool: null, programs: [] };
      return { tool: tool.isExample ? null : tool, programs: tool.programs };
    },
    track: (input) => recordClick(database, input),
  });
  if (result.status === 302) {
    return new NextResponse(null, { status: 302, headers: { location: result.location, "cache-control": "no-store", "x-robots-tag": "noindex, nofollow", "referrer-policy": "no-referrer" } });
  }
  return new NextResponse(result.body, {
    status: 404,
    headers: {
      "content-type": "text/plain; charset=utf-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex",
    },
  });
}
export const GET = (request: Request, context: { params: { slug: string } }) => redirect(request, context);
export const HEAD = (request: Request, context: { params: { slug: string } }) => redirect(request, context, true);
