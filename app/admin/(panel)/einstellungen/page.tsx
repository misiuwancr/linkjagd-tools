import { getDb } from "@/db/client";
import { saveSocialProofAction } from "@/lib/actions/content";
import { getSetting } from "@/lib/tools/repository";

export const dynamic = "force-dynamic";

export default async function SettingsPage({
  searchParams,
}: {
  searchParams: { gespeichert?: string };
}) {
  const value = await getSetting(await getDb(), "social_proof");
  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight">Einstellungen</h1>
      <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
        Die Zeile unter dem Newsletter auf der Startseite. Leer lassen, dann erscheint nichts. Eine gesetzte Umgebungsvariable gilt nur, wenn dieses Feld leer ist.
      </p>
      {searchParams.gespeichert ? <p className="mt-4 text-sm">Gespeichert.</p> : null}
      <form action={saveSocialProofAction} className="mt-6 grid max-w-xl gap-3">
        <label className="grid gap-1 text-sm font-medium">
          Social-Proof-Text
          <input name="socialProof" defaultValue={value} className="field" maxLength={240} />
        </label>
        <button type="submit" className="h-11 rounded-xl bg-primary text-sm font-semibold text-primary-foreground">
          Speichern
        </button>
      </form>
    </div>
  );
}
