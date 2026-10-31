"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu } from "lucide-react";
import { siteConfig } from "@/site.config";
import { BrandLockup } from "@/components/brand";
import { Sheet, SheetClose, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { cn } from "@/lib/utils";

function active(pathname: string, href: string) {
  if (href === "/tools") return pathname === "/tools" || pathname.startsWith("/tools/");
  return pathname === href || pathname.startsWith(`${href}/`);
}

export function SiteHeader() {
  const pathname = usePathname();
  return (
    <header className="sticky top-0 z-40 border-b border-border/80 bg-[#F7F5F2]/90 backdrop-blur">
      <div className="page-wrap flex h-16 items-center justify-between gap-4">
        <BrandLockup />
        <nav aria-label="Hauptnavigation" className="hidden items-center gap-1 lg:flex">
          {siteConfig.nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "rounded-full px-3 py-2 text-[13px] font-medium text-muted-foreground hover:bg-white hover:text-foreground",
                active(pathname, item.href) && "bg-white text-foreground shadow-sm",
              )}
              aria-current={active(pathname, item.href) ? "page" : undefined}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <Sheet>
          <SheetTrigger
            className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-border bg-white lg:hidden"
            aria-label="Menü öffnen"
          >
            <Menu className="h-4 w-4" />
          </SheetTrigger>
          <SheetContent side="right" className="w-[86vw] max-w-sm">
            <SheetHeader>
              <SheetTitle>Menü</SheetTitle>
            </SheetHeader>
            <nav aria-label="Mobilnavigation" className="mt-8 grid gap-1">
              {siteConfig.nav.map((item) => (
                <SheetClose asChild key={item.href}>
                  <Link
                    href={item.href}
                    className="rounded-xl px-3 py-3 text-base font-medium hover:bg-secondary"
                    aria-current={active(pathname, item.href) ? "page" : undefined}
                  >
                    {item.label}
                  </Link>
                </SheetClose>
              ))}
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}
