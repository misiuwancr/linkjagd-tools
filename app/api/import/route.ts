import { NextResponse } from "next/server";
import { getDb } from "@/db/client";
import { bearerMatches } from "@/lib/auth/roles";
import { importDiscoveredTool } from "@/lib/import/service";

export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  const verdict = bearerMatches(request.headers.get("authorization"), process.env.IMPORT_API_TOKEN);
  if (verdict === "missing_config") {
    return NextResponse.json({ error: "Import ist nicht konfiguriert." }, { status: 503 });
  }
  if (verdict !== "ok") {
    return NextResponse.json({ error: "Nicht autorisiert." }, { status: 401 });
  }
  let payload: unknown;
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json({ error: "Der Körper ist kein gültiges JSON." }, { status: 400 });
  }
  const database = await getDb();
  const result = await importDiscoveredTool(database, payload);
  if (!result.ok) {
    return NextResponse.json(
      { error: result.error, issues: "issues" in result ? result.issues : undefined, existingSlug: "existingSlug" in result ? result.existingSlug : undefined },
      { status: result.status },
    );
  }
  return NextResponse.json({ id: result.id, slug: result.slug, publishStatus: result.publishStatus }, { status: 201 });
}
