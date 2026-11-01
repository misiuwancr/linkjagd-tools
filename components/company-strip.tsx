import Link from "next/link";
import { COMPANY_STRIP_LABEL, type DirectoryCompany } from "@/lib/companies";

export function CompanyStrip({ companies }: { companies: DirectoryCompany[] }) {
  if (companies.length === 0) return null;
  return (
    <section aria-label={COMPANY_STRIP_LABEL} className="mt-8 max-w-5xl">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-muted-foreground">{COMPANY_STRIP_LABEL}</p>
      <ul className="mt-3 flex flex-wrap gap-2">
        {companies.slice(0, 15).map((company) => (
          <li key={company.slug}>
            <Link
              href={company.href}
              className="inline-flex items-center gap-2 rounded-full border border-border bg-card/50 px-3 py-1.5 text-sm text-muted-foreground transition hover:border-foreground/20 hover:text-foreground"
            >
              {company.markPath ? (
                <svg viewBox="0 0 24 24" className="h-4 w-4 shrink-0 fill-current" aria-hidden="true">
                  <path d={company.markPath} />
                </svg>
              ) : (
                <span aria-hidden="true" className="inline-flex h-4 w-4 items-center justify-center text-[10px] font-bold">
                  {company.name.slice(0, 1)}
                </span>
              )}
              {company.name}
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
