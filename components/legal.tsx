export function LegalDocument({
  title,
  intro,
  sections,
}: {
  title: string;
  intro: string;
  sections: readonly { heading: string; body: readonly string[] }[];
}) {
  return (
    <article className="page-wrap max-w-3xl py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-copper">Platzhalter</p>
      <h1 className="mt-3 text-4xl font-semibold tracking-tight">{title}</h1>
      <p className="mt-4 text-base leading-7 text-muted-foreground">{intro}</p>
      <div className="mt-10 space-y-8">
        {sections.map((section) => (
          <section key={section.heading}>
            <h2 className="text-xl font-semibold tracking-tight">{section.heading}</h2>
            <div className="mt-3 space-y-3 text-sm leading-7 text-foreground/90">
              {section.body.map((paragraph) => (
                <p key={paragraph} className={paragraph.startsWith("[PLATZHALTER") ? "rounded-xl bg-[#F8E7DC] px-3 py-2" : ""}>
                  {paragraph}
                </p>
              ))}
            </div>
          </section>
        ))}
      </div>
    </article>
  );
}
