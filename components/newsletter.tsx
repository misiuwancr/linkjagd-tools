import { newsletterIntent } from "@/lib/actions/public";

export function Newsletter({ notice }: { notice?: boolean }) {
  return (
    <section id="newsletter" className="border-t border-hunt/25 bg-card">
      <div className="page-wrap grid gap-8 py-14 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-hunt">Newsletter</p>
          <h2 className="mt-3 text-3xl font-bold tracking-tight">Neue Tools, ohne Lärm.</h2>
          <p className="mt-3 max-w-xl text-sm leading-6 text-muted-foreground">
            Hier entsteht später ein Versand. Solange kein Anbieter eingerichtet ist, wird keine Adresse gespeichert und keine Mail verschickt.
          </p>
        </div>
        <form action={newsletterIntent} className="grid gap-3">
          <label htmlFor="newsletter-email" className="text-sm font-medium">
            E-Mail
          </label>
          <div className="flex flex-col gap-2 sm:flex-row">
            <input
              id="newsletter-email"
              name="email"
              type="email"
              autoComplete="email"
              placeholder="du@beispiel.de"
              className="field h-12"
            />
            <button type="submit" className="h-12 rounded-xl bg-primary px-5 text-sm font-semibold text-primary-foreground">
              Interesse zeigen
            </button>
          </div>
          <input name="firma" tabIndex={-1} autoComplete="off" className="hidden" aria-hidden="true" />
          {notice ? (
            <p role="status" className="text-sm text-foreground">
              Der Newsletter-Versand ist noch nicht eingerichtet. Wir haben keine Adresse gespeichert und nichts verschickt.
            </p>
          ) : (
            <p className="text-xs leading-5 text-muted-foreground">
              Mit dem Absenden bestätigst du nur, dass du die Fläche gesehen hast. Es entsteht kein Abonnement.
            </p>
          )}
        </form>
      </div>
    </section>
  );
}
