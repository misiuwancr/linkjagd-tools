import Link from "next/link";
import { siteConfig } from "@/site.config";
import { cn } from "@/lib/utils";

export function BrandMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={cn("h-8 w-8", className)} aria-hidden="true">
      <rect width="32" height="32" rx="8" fill="#0B0E0C" />
      <circle cx="15" cy="14" r="7.2" fill="none" stroke="#C6F531" strokeWidth="1.4" />
      <circle cx="15" cy="14" r="2.6" fill="none" stroke="#C6F531" strokeWidth="1.4" />
      <path d="M15 5.2v2.4M15 20.2v2.4M6.4 14h2.4M21.2 14h2.4" stroke="#C6F531" strokeWidth="1.3" strokeLinecap="round" />
      <path d="M17.4 12.4 23.2 14l-3.6 2.1z" fill="#D8FF6A" />
    </svg>
  );
}

export function BrandLockup({ compact = false }: { compact?: boolean }) {
  return (
    <Link href="/" className="flex items-center gap-2.5 rounded-lg">
      <BrandMark />
      <span className="leading-none">
        <span className="block text-[15px] font-bold tracking-tight">
          <span className="text-foreground">Link</span>
          <span className="text-hunt">jagd</span>
        </span>
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
