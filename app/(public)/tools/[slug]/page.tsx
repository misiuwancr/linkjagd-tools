import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { CategoryBadge, ExampleBadge, LicenseBadge, PriceBadge, RecommendBadge } from "@/components/badges";
import { licenseLabel, pricingLabel } from "@/lib/labels";
import { JsonLd } from "@/components/json-ld";
import { ToolCard } from "@/components/tool-card";
import { ToolLogo } from "@/components/tool-logo";
import { getToolBySlug, listSimilar } from "@/lib/tools/repository";
import { toPublicTool } from "@/lib/tools/public";

export const revalidate = 60;

function host() {
  try {
    return new URL(siteConfig.url).hostname;
  } catch {
    return undefined;
  }
}

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const database = await getDb();
  const tool = await getToolBySlug(database, params.slug);
  if (!tool || tool.publishStatus !== "published") return { title: "Tool nicht gefunden" };
  const publicTool = toPublicTool(tool, host());
  return {
    title: publicTool.name,
    description: publicTool.shortDescriptionDe,
    alternates: { canonical: `/tools/${publicTool.slug}` },
    openGraph: {
      title: publicTool.name,
      description: publicTool.shortDescriptionDe,
      url: `/tools/${publicTool.slug}`,
    },
  };
}

export default async function ToolDetailPage({ params }: { params: { slug: string } }) {
  const database = await getDb();
  const record = await getToolBySlug(database, params.slug);
  if (!record || record.publishStatus !== "published") notFound();
  const siteHost = host();
  const tool = toPublicTool(record, siteHost);
  const similar = (await listSimilar(database, record)).map((item) => toPublicTool(item, siteHost));
  const canonical = new URL(`/tools/${tool.slug}`, siteConfig.url).toString();

  return (
    <div className="page-wrap py-8 sm:py-12">
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "SoftwareApplication",
          name: tool.name,
          description: tool.shortDescriptionDe,
          applicationCategory: tool.categories[0]?.name,
          url: canonical,
          inLanguage: "de",
        }}
      />
      <nav aria-label="Brotkrumen" className="text-sm text-muted-foreground">
        <Link href="/tools" className="hover:text-foreground">
          Alle Tools
        </Link>
        <span aria-hidden="true"> / </span>
        <span className="text-foreground">{tool.name}</span>
      </nav>

      <header className="mt-6 grid gap-8 lg:grid-cols-[minmax(0,1fr)_320px] lg:items-start">
        <div>
          <div className="flex items-start gap-4">
            <ToolLogo name={tool.name} logo={tool.logo} size={72} />
            <div>
              <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">{tool.name}</h1>
              <p className="mt-3 max-w-2xl text-lg leading-8 text-muted-foreground">{tool.shortDescriptionDe}</p>
            </div>
          </div>
          <div className="mt-5 flex flex-wrap gap-2">
            {tool.featured ? <RecommendBadge /> : null}
            {tool.isExample ? <ExampleBadge /> : null}
            <PriceBadge value={tool.pricingModel} />
            <LicenseBadge value={tool.licenseType} />
            {tool.beginnerFriendly ? (
              <span className="inline-flex items-center rounded-full bg-secondary px-2.5 py-1 text-xs font-medium">Für Anfänger</span>
            ) : null}
            {tool.categories.map((category) => (
              <CategoryBadge key={category.slug} name={category.name} slug={category.slug} />
            ))}
          </div>
          {tool.isExample ? (
            <p className="note mt-4 max-w-2xl">
              Dieser Eintrag ist ein Beispieldatensatz. Es ist kein reales Angebot und es ist kein Partnerlink hinterlegt.
            </p>
          ) : null}
        </div>
        <aside className="rounded-3xl border border-border bg-card p-5 shadow-card lg:sticky lg:top-24">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-muted-foreground">Auf einen Blick</p>
          <dl className="mt-4 space-y-3 text-sm">
            <div className="flex justify-between gap-4">
              <dt className="text-muted-foreground">Preismodell</dt>
              <dd className="font-medium">{pricingLabel(tool.pricingModel)}</dd>
            </div>
            <div className="flex justify-between gap-4">
              <dt className="text-muted-foreground">Lizenz</dt>
              <dd className="font-medium">{licenseLabel(tool.licenseType)}</dd>
            </div>
            <div className="flex justify-between gap-4">
              <dt className="text-muted-foreground">Website</dt>
              <dd className="font-medium">{tool.domain}</dd>
            </div>
          </dl>
          <div className="mt-5">
            {tool.ctaKind === "disabled" ? (
              <button
                type="button"
                disabled
                className="flex h-12 w-full cursor-not-allowed items-center justify-center rounded-xl bg-secondary px-4 text-sm font-semibold text-muted-foreground"
              >
                Zur Website
              </button>
            ) : (
              <a
                href={`/go/${tool.slug}`}
                rel={tool.ctaKind === "affiliate" ? "sponsored nofollow noopener" : "noopener noreferrer"}
                className="flex h-12 items-center justify-center rounded-xl bg-primary px-4 text-sm font-semibold text-primary-foreground"
              >
                {tool.ctaKind === "affiliate" ? "Jetzt Tool ausprobieren" : "Zur offiziellen Website"}
              </a>
            )}
            <p className="mt-3 text-xs leading-5 text-muted-foreground">
              {tool.ctaKind === "affiliate"
                ? "Werbung. Der Button ist ein Partnerlink. Für dich entsteht dadurch kein Aufpreis."
                : tool.ctaKind === "official"
                  ? "Kein Partnerlink. Der Button führt zur offiziellen Website, ohne zusätzliche Empfehlungsparameter."
                  : "Für dieses Tool ist keine gültige Zieladresse hinterlegt."}
            </p>
            <Link href="/affiliate-hinweis" className="mt-2 inline-block text-xs font-medium underline">
              Affiliate-Hinweis
            </Link>
          </div>
        </aside>
      </header>

      <div className="mt-12 grid gap-12 lg:grid-cols-[minmax(0,1fr)_320px]">
        <div className="space-y-12">
          <section>
            <h2 className="text-2xl font-bold tracking-tight">Über das Tool</h2>
            <div className="mt-4 max-w-3xl whitespace-pre-wrap text-base leading-8 text-foreground/90">
              {tool.longDescriptionDe || "Eine ausführliche Beschreibung folgt."}
            </div>
          </section>
          {tool.featuresDe.length > 0 ? (
            <section>
              <h2 className="text-2xl font-bold tracking-tight">Besondere Funktionen</h2>
              <ul className="mt-4 max-w-3xl space-y-3">
                {tool.featuresDe.map((feature) => (
                  <li key={feature} className="rounded-2xl border border-border bg-card px-4 py-3 text-sm leading-6">
                    {feature}
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
          {tool.useCasesDe.length > 0 ? (
            <section>
              <h2 className="text-2xl font-bold tracking-tight">Typische Anwendungen</h2>
              <ul className="mt-4 max-w-3xl list-disc space-y-2 pl-5 text-sm leading-6">
                {tool.useCasesDe.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </section>
          ) : null}
          {tool.licenseType === "open_source" ? (
            <section>
              <h2 className="text-2xl font-bold tracking-tight">Open Source</h2>
              <dl className="mt-4 max-w-3xl space-y-2 text-sm">
                <div className="flex justify-between gap-4">
                  <dt className="text-muted-foreground">Lizenz</dt>
                  <dd>{tool.ossLicense || "Unbekannt"}</dd>
                </div>
                {tool.ossOperatingSystems.length > 0 ? (
                  <div className="flex justify-between gap-4">
                    <dt className="text-muted-foreground">Systeme</dt>
                    <dd>{tool.ossOperatingSystems.join(", ")}</dd>
                  </div>
                ) : null}
              </dl>
              {tool.ossInstallNotes ? <p className="mt-3 max-w-3xl text-sm leading-6 text-muted-foreground">{tool.ossInstallNotes}</p> : null}
              <div className="mt-3 flex flex-wrap gap-3 text-sm">
                {tool.ossProjectUrl ? (
                  <a href={tool.ossProjectUrl} rel="noopener noreferrer" className="underline">Projektwebsite</a>
                ) : null}
                {tool.ossRepoUrl ? (
                  <a href={tool.ossRepoUrl} rel="noopener noreferrer" className="underline">Repository</a>
                ) : null}
              </div>
            </section>
          ) : null}
          {tool.editorRating ? (
            <p className="text-sm text-muted-foreground">Redaktionelle Bewertung: {tool.editorRating} von 5. Das ist keine Nutzerwertung.</p>
          ) : null}
          <section>
            <h2 className="text-2xl font-bold tracking-tight">Vorschau</h2>
            {tool.screenshots.length > 0 ? (
              <div className="mt-4 grid gap-4">
                {tool.screenshots.map((shot) =>
                  shot.endsWith(".svg") ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img key={shot} src={shot} alt={`Beispielvorschau von ${tool.name}`} className="w-full rounded-2xl border border-border bg-card" />
                  ) : (
                    <Image
                      key={shot}
                      src={shot}
                      alt={`Vorschau von ${tool.name}`}
                      width={1200}
                      height={750}
                      className="h-auto w-full rounded-2xl border border-border bg-card"
                    />
                  ),
                )}
              </div>
            ) : (
              <p className="mt-4 text-sm text-muted-foreground">Für dieses Tool sind noch keine Vorschaubilder hinterlegt.</p>
            )}
          </section>
          <section>
            <h2 className="text-2xl font-bold tracking-tight">Ähnliche Tools</h2>
            {similar.length === 0 ? (
              <p className="mt-4 text-sm text-muted-foreground">In dieser Kategorie gibt es noch keine weiteren veröffentlichten Tools.</p>
            ) : (
              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                {similar.map((item) => (
                  <ToolCard key={item.id} tool={item} />
                ))}
              </div>
            )}
          </section>
        </div>
        <div className="hidden lg:block" />
      </div>
    </div>
  );
}
