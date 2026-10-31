import { requireUser } from "@/lib/auth/session";
import { getDb } from "@/db/client";
import { listSubscribers } from "@/lib/tools/repository";

export const dynamic = "force-dynamic";

export async function GET() {
  await requireUser("editor");
  const rows = await listSubscribers(await getDb());
  const lines = ["email,status,created_at,confirmed_at"];
  for (const row of rows) {
    const email = `"${row.email.replace(/"/g, '""')}"`;
    lines.push([email, row.status, row.createdAt.toISOString(), row.confirmedAt?.toISOString() ?? ""].join(","));
  }
  return new Response(lines.join("\n"), {
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": "attachment; filename=newsletter.csv",
    },
  });
}
