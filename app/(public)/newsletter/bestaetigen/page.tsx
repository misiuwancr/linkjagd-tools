import type { Metadata } from "next";
import { eq } from "drizzle-orm";
import { getDb } from "@/db/client";
import { newsletterSubscribers } from "@/db/schema";
import { confirmTokenHash } from "@/lib/newsletter";

export const metadata: Metadata = {
  title: "Anmeldung bestätigen",
  robots: { index: false, follow: false },
};

export default async function ConfirmPage({
  searchParams,
}: {
  searchParams: { token?: string };
}) {
  const token = (searchParams.token || "").trim();
  let ok = false;
  if (/^[a-f0-9]{64}$/.test(token)) {
    const database = await getDb();
    const hash = confirmTokenHash(token);
    const rows = await database.select().from(newsletterSubscribers).where(eq(newsletterSubscribers.confirmToken, hash)).limit(1);
    const row = rows[0];
    if (row && row.status === "pending") {
      await database
        .update(newsletterSubscribers)
        .set({ status: "confirmed", confirmedAt: new Date() })
        .where(eq(newsletterSubscribers.id, row.id));
      ok = true;
    }
    if (row?.status === "confirmed") ok = true;
  }
  return (
    <div className="page-wrap max-w-xl py-16">
      <h1 className="text-4xl font-bold tracking-tight">{ok ? "Anmeldung bestätigt" : "Link ungültig"}</h1>
      <p className="mt-4 text-muted-foreground">
        {ok
          ? "Die Adresse ist bestätigt. Weitere Mails gibt es erst, wenn eine Ausgabe verschickt wird."
          : "Dieser Bestätigungslink passt zu keinem offenen Eintrag."}
      </p>
    </div>
  );
}
