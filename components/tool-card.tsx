import Link from "next/link";
import type { PublicTool } from "@/lib/tools/public";
import { CategoryBadge, ExampleBadge, LicenseBadge, PriceBadge, RecommendBadge, VideoBadge } from "@/components/badges";
import { ToolLogo } from "@/components/tool-logo";
import { VoteButton } from "@/components/vote-button";

export function ToolCard({ tool }: { tool: PublicTool }) {
  return (
    <article className="flex h-full flex-col rounded-2xl border border-border bg-card/80 p-4 transition hover:border-hunt/40">
      <div className="flex items-start gap-3">
        <Link href={`/tools/${tool.slug}`} className="shrink-0 rounded-xl" aria-label={tool.name}>
          <ToolLogo name={tool.name} logo={tool.logo} />
        </Link>
        <div className="min-w-0">
          <h3 className="text-base font-semibold leading-6 tracking-tight">
            <Link href={`/tools/${tool.slug}`} className="break-words hover:underline">
              {tool.name}
            </Link>
          </h3>
          <div className="mt-2 flex flex-wrap gap-1.5">
            {tool.featured ? <RecommendBadge /> : null}
            {tool.fromVideo ? <VideoBadge /> : null}
            {tool.isExample ? <ExampleBadge /> : null}
          </div>
        </div>
      </div>
      <p className="mt-3 line-clamp-3 flex-1 text-sm leading-6 text-muted-foreground">{tool.shortDescriptionDe}</p>
      <VoteButton slug={tool.slug} name={tool.name} />
      <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
        <Link href={`/tools/${tool.slug}`} className="inline-flex min-h-10 items-center text-sm font-semibold text-hunt">Details ansehen →</Link>
        <a
          href={`/go/${tool.slug}`}
          rel={tool.ctaKind === "affiliate" ? "sponsored nofollow noopener" : "nofollow noopener"}
          className="text-xs font-semibold text-muted-foreground hover:text-foreground"
        >
          {tool.ctaKind === "affiliate" ? "Zum Anbieter · Anzeige ↗" : "Zum Anbieter ↗"}
        </a>
      </div>
      <div className="mt-3 flex flex-wrap gap-1.5">
        {tool.categories.slice(0, 2).map((category) => (
          <CategoryBadge key={category.slug} name={category.name} slug={category.slug} />
        ))}
        <PriceBadge value={tool.pricingModel} />
        {tool.licenseType === "open_source" ? <LicenseBadge value="open_source" /> : null}
      </div>
    </article>
  );
}
