"use client";

export default function PublicError({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div className="page-wrap py-24">
      <h1 className="text-3xl font-bold tracking-tight">Die Seite konnte nicht geladen werden.</h1>
      <p className="mt-3 text-muted-foreground">Bitte versuche es noch einmal. Wenn es wieder passiert, ist die Datenbank gerade nicht erreichbar.</p>
      <button type="button" onClick={reset} className="mt-6 h-11 rounded-xl bg-primary px-4 text-sm font-medium text-primary-foreground">
        Erneut versuchen
      </button>
    </div>
  );
}
