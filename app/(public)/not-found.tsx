import Link from "next/link";

export default function NotFound() {
  return (
    <div className="page-wrap py-24">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">404</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">Diese Seite gibt es nicht.</h1>
      <p className="mt-3 max-w-xl text-muted-foreground">Der Eintrag ist nicht veröffentlicht oder der Pfad ist unbekannt.</p>
      <Link href="/tools" className="mt-6 inline-flex h-11 items-center rounded-xl bg-primary px-4 text-sm font-medium text-primary-foreground">
        Zum Verzeichnis
      </Link>
    </div>
  );
}
