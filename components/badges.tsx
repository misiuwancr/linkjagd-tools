import Link from "next/link";
import type { LicenseType, PricingModel } from "@/db/schema";
import { licenseLabel, pricingLabel } from "@/lib/labels";
import { cn } from "@/lib/utils";

const priceClass: Record<PricingModel, string> = {
  free: "bg-[#12352A] text-[#B7F7D4] ring-[#1F6B4E]",
  freemium: "bg-[#123044] text-[#D7EEFF] ring-[#1E4E73]",
  paid: "bg-[#3A2A10] text-[#FFE7B0] ring-[#6B5420]",
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
    <Link href={`/kategorien/${slug}`} className={cn(className, "hover:bg-hunt/15 hover:text-hunt")}>
      {name}
    </Link>
  );
}

export function VideoBadge() {
  return (
    <span className="inline-flex items-center rounded-full bg-black px-2.5 py-1 text-xs font-medium text-hunt ring-1 ring-hunt/40">
      Aus dem Video
    </span>
  );
}

export function RecommendBadge() {
  return (
    <span className="inline-flex items-center rounded-full bg-hunt px-2.5 py-1 text-xs font-bold text-primary-foreground">
      Empfohlen
    </span>
  );
}

export function LicenseBadge({ value }: { value: LicenseType }) {
  const className =
    value === "open_source"
      ? "bg-[#143028] text-[#D6FFE8] ring-[#1F6B4E]"
      : value === "proprietary"
        ? "bg-secondary text-foreground ring-border"
        : "bg-transparent text-muted-foreground ring-border";
  return (
    <span className={cn("inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset", className)}>
      {licenseLabel(value)}
    </span>
  );
}

export function ExampleBadge() {
  return (
    <span className="inline-flex items-center rounded-full bg-transparent px-2.5 py-1 text-xs font-medium text-muted-foreground ring-1 ring-inset ring-border">
      Beispiel
    </span>
  );
}
