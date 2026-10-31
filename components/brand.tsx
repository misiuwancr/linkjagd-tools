import Link from "next/link";
import { siteConfig } from "@/site.config";
import { cn } from "@/lib/utils";

export function BrandMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={cn("h-8 w-8", className)} aria-hidden="true">
      <rect width="32" height="32" rx="8" fill="#1C1915" />
      <path
        d="M8.5 16.2h6.4a3.3 3.3 0 1 0 0-6.6H12"
        fill="none"
        stroke="#F6F1EA"
        strokeWidth="1.8"
        strokeLinecap="round"
      />
      <path
        d="M23.5 15.8h-6.4a3.3 3.3 0 1 0 0 6.6H20"
        fill="none"
        stroke="#E08A45"
        strokeWidth="1.8"
        strokeLinecap="round"
      />
      <circle cx="23" cy="8.5" r="2" fill="#E08A45" />
    </svg>
  );
}

export function BrandLockup({ compact = false }: { compact?: boolean }) {
  return (
    <Link href="/" className="flex items-center gap-2.5 rounded-lg">
      <BrandMark />
      <span className="leading-none">
        <span className="block text-[15px] font-semibold tracking-tight text-ink">{siteConfig.shortName}</span>
        {!compact ? (
          <span className="mt-1 block text-[11px] font-medium uppercase tracking-[0.16em] text-muted-foreground">
            Tools
          </span>
        ) : null}
      </span>
      <span className="sr-only">{siteConfig.name}</span>
    </Link>
  );
}
