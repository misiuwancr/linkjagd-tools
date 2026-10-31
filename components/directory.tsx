import Link from "next/link";
import { licenseOptions, pricingOptions, sortOptions } from "@/lib/labels";
import { directoryHref, type ToolListQuery } from "@/lib/tools/query";
import type { PublicTool } from "@/lib/tools/public";
import { ToolCard } from "@/components/tool-card";

export function PriceChips({
  query,
  basePath,
}: {
  query: ToolListQuery;
  basePath: string;
}) {
  return (
    <div className="flex flex-wrap gap-2" aria-label="Preismodell">
      <Link
        href={directoryHref(basePath, query, { pricing: "", page: 1 })}
        className={chipClass(query.pricing === "")}
        aria-current={query.pricing === "" ? "true" : undefined}
      >
        Alle Preise
      </Link>
      {pricingOptions.map((item) => (
        <Link
          key={item.value}
          href={directoryHref(basePath, query, { pricing: item.value, page: 1 })}
          className={chipClass(query.pricing === item.value)}
          aria-current={query.pricing === item.value ? "true" : undefined}
        >
          {item.label}
        </Link>
      ))}
    </div>
  );
}

export function LicenseChips({
  query,
  basePath,
}: {
  query: ToolListQuery;
  basePath: string;
}) {
  return (
    <div className="mt-3 flex flex-wrap gap-2" aria-label="Lizenz">
      <Link href={directoryHref(basePath, query, { license: "", page: 1 })} className={chipClass(query.license === "")}>
        Alle Lizenzen
      </Link>
      {licenseOptions.map((item) => (
        <Link
          key={item.value}
          href={directoryHref(basePath, query, { license: item.value, page: 1 })}
          className={chipClass(query.license === item.value)}
        >
          {item.label}
        </Link>
      ))}
    </div>
  );
}

function chipClass(active: boolean) {
  return active
    ? "inline-flex h-9 items-center rounded-full bg-primary px-3 text-sm font-medium text-primary-foreground"
    : "inline-flex h-9 items-center rounded-full border border-border bg-card px-3 text-sm font-medium text-foreground hover:border-hunt/40";
}

export function DirectoryFilters({
  query,
  categories,
  action = "/tools",
}: {
  query: ToolListQuery;
  categories: { name: string; slug: string }[];
  action?: string;
}) {
  return (
    <form method="get" action={action} className="grid gap-3 rounded-2xl border border-border bg-card p-3 sm:p-4 lg:grid-cols-[1.4fr_1fr_1fr_1fr_auto]">
      <div>
        <label htmlFor="q" className="mb-1 block text-xs font-medium text-muted-foreground">
          Suche
        </label>
        <input id="q" name="q" defaultValue={query.q} placeholder="Name, Beschreibung, Kategorie" className="field" />
      </div>
      <div>
        <label htmlFor="kategorie" className="mb-1 block text-xs font-medium text-muted-foreground">
          Kategorie
        </label>
        <select id="kategorie" name="kategorie" defaultValue={query.categorySlug} className="field">
          <option value="">Alle Kategorien</option>
          {categories.map((category) => (
            <option key={category.slug} value={category.slug}>
              {category.name}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label htmlFor="preis" className="mb-1 block text-xs font-medium text-muted-foreground">
          Preis
        </label>
        <select id="preis" name="preis" defaultValue={query.pricing ? pricingOptions.find((item) => item.value === query.pricing)?.param : ""} className="field">
          <option value="">Alle Preismodelle</option>
          {pricingOptions.map((item) => (
            <option key={item.value} value={item.param}>
              {item.label}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label htmlFor="sort" className="mb-1 block text-xs font-medium text-muted-foreground">
          Sortierung
        </label>
        {query.company ? <input type="hidden" name="firma" value={query.company} /> : null}
        <select id="sort" name="sort" defaultValue={sortOptions.find((item) => item.value === query.sort)?.param ?? "neueste"} className="field">
          {sortOptions.map((item) => (
            <option key={item.value} value={item.param}>
              {item.label}
            </option>
          ))}
        </select>
      </div>
      <div className="flex items-end gap-2">
        <button type="submit" className="h-11 rounded-xl bg-primary px-4 text-sm font-medium text-primary-foreground">
          Filtern
        </button>
        <Link href={action} className="inline-flex h-11 items-center rounded-xl px-3 text-sm text-muted-foreground hover:text-foreground">
          Zurücksetzen
        </Link>
      </div>
    </form>
  );
}

export function ToolGrid({ tools }: { tools: PublicTool[] }) {
  if (tools.length === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-border bg-card px-6 py-16 text-center">
        <p className="text-base font-medium">Keine Tools passen zu dieser Auswahl.</p>
        <p className="mt-2 text-sm text-muted-foreground">Setze die Filter zurück oder such nach einem anderen Begriff.</p>
      </div>
    );
  }
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      {tools.map((tool) => (
        <ToolCard key={tool.id} tool={tool} />
      ))}
    </div>
  );
}

export function Pagination({
  query,
  total,
  basePath,
}: {
  query: ToolListQuery;
  total: number;
  basePath: string;
}) {
  const pages = Math.max(1, Math.ceil(total / query.pageSize));
  if (pages < 2) return null;
  const current = Math.min(query.page, pages);
  const from = Math.max(1, current - 2);
  const to = Math.min(pages, current + 2);
  const items = [];
  for (let page = from; page <= to; page += 1) items.push(page);
  const linkClass = "inline-flex h-10 min-w-10 items-center justify-center rounded-full px-3 text-sm";
  return (
    <nav aria-label="Seiten" className="mt-8 flex flex-wrap items-center justify-center gap-2">
      {current > 1 ? (
        <Link href={directoryHref(basePath, query, { page: current - 1 })} className={linkClass + " border border-border bg-card"}>
          Zurück
        </Link>
      ) : null}
      {items.map((page) => (
        <Link
          key={page}
          href={directoryHref(basePath, query, { page })}
          aria-current={page === current ? "page" : undefined}
          className={linkClass + (page === current ? " bg-primary text-primary-foreground" : " border border-border bg-card")}
        >
          {page}
        </Link>
      ))}
      {current < pages ? (
        <Link href={directoryHref(basePath, query, { page: current + 1 })} className={linkClass + " border border-border bg-card"}>
          Weiter
        </Link>
      ) : null}
    </nav>
  );
}

export function ResultMeta({ page, pageSize, total }: { page: number; pageSize: number; total: number }) {
  if (total === 0) return <p className="text-sm text-muted-foreground">0 Tools</p>;
  const start = (page - 1) * pageSize + 1;
  const end = Math.min(total, page * pageSize);
  return (
    <p className="text-sm text-muted-foreground">
      {start}–{end} von {total} {total === 1 ? "Tool" : "Tools"}
    </p>
  );
}
