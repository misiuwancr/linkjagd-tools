import Link from "next/link";
import type { PricingModel } from "@/db/schema";
import { pricingLabel } from "@/lib/labels";
import { cn } from "@/lib/utils";

const priceClass: Record<PricingModel, string> = {
  free: "bg-emerald-50 text-emerald-900 ring-emerald-200",
  freemium: "bg-sky-50 text-sky-900 ring-sky-200",
  paid: "bg-amber-50 text-amber-950 ring-amber-200",
  open_source: "bg-violet-50 text-violet-900 ring-violet-200",
};

export function PriceBadge({ value }: { value: PricingModel }) {
  return (
    <span className={cn("inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset", priceClass[value])}>
      {pricingLabel(value)}
    </span>
  );
}

export function CategoryBadge({ name, slug }: { name: string; slug?: string }) {
  const className =
    "inline-flex items-center rounded-full bg-secondary px-2.5 py-1 text-xs font-medium text-secondary-foreground";
  if (!slug) return <span className={className}>{name}</span>;
  return (
    <Link href={`/kategorien/${slug}`} className={cn(className, "hover:bg-[#E7E1D8]")}>
      {name}
    </Link>
  );
}

export function RecommendBadge() {
  return (
    <span className="inline-flex items-center rounded-full bg-[#F8E7DC] px-2.5 py-1 text-xs font-semibold text-[#8A3E16]">
      Empfohlen
    </span>
  );
}

export function ExampleBadge() {
  return (
    <span className="inline-flex items-center rounded-full bg-white px-2.5 py-1 text-xs font-medium text-muted-foreground ring-1 ring-inset ring-border">
      Beispiel
    </span>
  );
}
