import { NextResponse } from "next/server";
import { getDb } from "@/db/client";
import { handleGoRedirect } from "@/lib/affiliate/go";
import { recordClick, getToolBySlug } from "@/lib/tools/repository";
import { siteConfig } from "@/site.config";

export const dynamic = "force-dynamic";

function host() {
  try {
    return new URL(siteConfig.url).hostname;
  } catch {
    return undefined;
  }
}

export async function GET(_request: Request, { params }: { params: { slug: string } }) {
  const database = await getDb();
  const result = await handleGoRedirect(params.slug, {
    siteHost: host(),
    load: async (slug) => {
      const tool = await getToolBySlug(database, slug);
      if (!tool) return { tool: null, programs: [] };
      return { tool, programs: tool.programs };
    },
    track: (input) => recordClick(database, input),
  });
  if (result.status === 302) {
    return NextResponse.redirect(result.location, 302);
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
