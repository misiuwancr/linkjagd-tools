import Link from "next/link";
import { siteConfig } from "@/site.config";
import { cn } from "@/lib/utils";
import { BrandWordmark } from "@/components/brand-wordmark";

export function BrandMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={cn("h-8 w-8", className)} aria-hidden="true">
      <rect width="32" height="32" rx="8" fill="#0B0E0C" />
      <path d="M8 7h6v18H8z" fill="#D0FF28" />
      <circle cx="23" cy="22" r="4" fill="#D0FF28" />
    </svg>
  );
}

export function BrandLockup({ compact = false }: { compact?: boolean }) {
  return (
    <Link href="/" aria-label={`${siteConfig.name} – Startseite`} className="brand-wordmark inline-flex shrink-0 items-center rounded-lg py-1">
      <BrandWordmark width={compact ? 150 : 188} height={compact ? 30 : 37} className="max-w-[44vw]" />
    </Link>
  );
}
