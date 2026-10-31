import { newsletterIntent } from "@/lib/actions/public";

export function Newsletter({ notice }: { notice?: boolean }) {
  return (
    <section id="newsletter" className="bg-ink text-[#F6F1EA]">
      <div className="page-wrap grid gap-8 py-14 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#E08A45]">Newsletter</p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight">Neue Tools, ohne Lärm.</h2>
          <p className="mt-3 max-w-xl text-sm leading-6 text-[#D9D0C5]">
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
              className="h-12 flex-1 rounded-xl border border-white/10 bg-white px-3 text-sm text-ink"
            />
            <button type="submit" className="h-12 rounded-xl bg-[#E08A45] px-5 text-sm font-semibold text-ink">
              Interesse zeigen
            </button>
          </div>
          <input name="firma" tabIndex={-1} autoComplete="off" className="hidden" aria-hidden="true" />
          {notice ? (
            <p role="status" className="text-sm text-[#F6F1EA]">
              Der Newsletter-Versand ist noch nicht eingerichtet. Wir haben keine Adresse gespeichert und nichts verschickt.
            </p>
          ) : (
            <p className="text-xs leading-5 text-[#B7A99B]">
              Mit dem Absenden bestätigst du nur, dass du die Fläche gesehen hast. Es entsteht kein Abonnement.
            </p>
          )}
        </form>
      </div>
    </section>
  );
}
