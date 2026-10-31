export function Newsletter({ notice }: { notice?: boolean }) {
  return (
    <section id="newsletter" className="border-t border-hunt/25 bg-card">
      <div className="page-wrap py-14">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-hunt">Newsletter</p>
        <h2 className="mt-3 text-3xl font-bold tracking-tight">Kein Newsletter-Versand.</h2>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
          Es ist kein Versanddienst angebunden. Es wird keine Adresse abgefragt, nichts gespeichert und keine Mail verschickt.
        </p>
        {notice ? (
          <p role="status" className="mt-4 text-sm text-foreground">
            Es wurde nichts gespeichert und nichts verschickt.
          </p>
        ) : null}
      </div>
    </section>
  );
}
