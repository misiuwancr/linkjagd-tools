import Link from "next/link";
import type { PublicTool } from "@/lib/tools/public";
import { CategoryBadge, ExampleBadge, LicenseBadge, PriceBadge, RecommendBadge } from "@/components/badges";
import { ToolLogo } from "@/components/tool-logo";

export function ToolCard({ tool }: { tool: PublicTool }) {
  return (
    <article className="flex h-full flex-col rounded-2xl border border-border bg-card p-4 shadow-card transition hover:-translate-y-0.5 hover:border-hunt/50">
      <div className="flex items-start gap-3">
        <Link href={`/tools/${tool.slug}`} className="shrink-0 rounded-xl" aria-label={tool.name}>
          <ToolLogo name={tool.name} logo={tool.logo} />
        </Link>
        <div className="min-w-0">
          <h3 className="text-[15px] font-semibold leading-5 tracking-tight">
            <Link href={`/tools/${tool.slug}`} className="hover:underline">
              {tool.name}
            </Link>
          </h3>
          <div className="mt-2 flex flex-wrap gap-1.5">
            {tool.featured ? <RecommendBadge /> : null}
            {tool.isExample ? <ExampleBadge /> : null}
          </div>
        </div>
      </div>
      <p className="mt-3 line-clamp-3 flex-1 text-sm leading-6 text-muted-foreground">{tool.shortDescriptionDe}</p>
      <div className="mt-4 flex flex-wrap gap-1.5">
        {tool.categories.slice(0, 2).map((category) => (
          <CategoryBadge key={category.slug} name={category.name} slug={category.slug} />
        ))}
        <PriceBadge value={tool.pricingModel} />
        {tool.licenseType === "open_source" ? <LicenseBadge value="open_source" /> : null}
      </div>
    </article>
  );
}
