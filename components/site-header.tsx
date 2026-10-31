"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Menu, X } from "lucide-react";
import { BrandLockup } from "@/components/brand";
import { cn } from "@/lib/utils";

const groups = [
  {
    label: "Tools",
    links: [
      { href: "/top-20", label: "Top 20 Tools" },
      { href: "/tools", label: "Alle Tools" },
      { href: "/neu", label: "Neu hinzugefügt" },
      { href: "/einreichen", label: "Tool einreichen" },
    ],
  },
  {
    label: "Redaktion",
    links: [
      { href: "/blog", label: "Blog" },
      { href: "/newsletter", label: "Newsletter-Archiv" },
    ],
  },
  {
    label: "Mehr",
    links: [
      { href: "/ueber-uns", label: "Über uns" },
      { href: "https://www.tiktok.com/@linkjagd", label: "Videos", external: true },
      { href: "/glossar", label: "Glossar" },
      { href: "/faq", label: "FAQ" },
    ],
  },
];

export function SiteHeader() {
  const [open, setOpen] = useState(false);
  const [light, setLight] = useState(false);
  useEffect(() => {
    const stored = window.localStorage.getItem("linkjagd-theme");
    const next = stored === "light";
    setLight(next);
    document.documentElement.classList.toggle("light", next);
  }, []);
  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  function toggleTheme() {
    const next = !light;
    setLight(next);
    document.documentElement.classList.toggle("light", next);
    window.localStorage.setItem("linkjagd-theme", next ? "light" : "dark");
  }

  return (
    <header className="sticky top-0 z-40 border-b border-border/80 bg-background/85 backdrop-blur">
      <div className="page-wrap flex h-16 items-center justify-between gap-4">
        <BrandLockup />
        <nav aria-label="Hauptnavigation" className="hidden items-center gap-1 lg:flex">
          <Link href="/top-20" className="rounded-full px-3 py-2 text-[13px] font-medium text-muted-foreground hover:text-foreground">
            Top 20
          </Link>
          <Link href="/tools" className="rounded-full px-3 py-2 text-[13px] font-medium text-muted-foreground hover:text-foreground">
            Alle Tools
          </Link>
          <Link href="/neu" className="rounded-full px-3 py-2 text-[13px] font-medium text-muted-foreground hover:text-foreground">
            Neu
          </Link>
          <Link href="/blog" className="rounded-full px-3 py-2 text-[13px] font-medium text-muted-foreground hover:text-foreground">
            Blog
          </Link>
          <Link href="/ueber-uns" className="rounded-full px-3 py-2 text-[13px] font-medium text-muted-foreground hover:text-foreground">
            Über uns
          </Link>
          <a href="#anmeldung" className="ml-2 rounded-full bg-primary px-4 py-2 text-[13px] font-bold text-primary-foreground">
            Abonnieren
          </a>
          <button type="button" onClick={toggleTheme} className="ml-1 rounded-full border border-border px-3 py-2 text-[13px]">
            {light ? "Dunkel" : "Hell"}
          </button>
        </nav>
        <button
          type="button"
          className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-border bg-card lg:hidden"
          aria-label={open ? "Menü schließen" : "Menü öffnen"}
          aria-expanded={open}
          onClick={() => setOpen((value) => !value)}
        >
          {open ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
        </button>
      </div>
      {open ? (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-background lg:hidden">
          <div className="page-wrap flex h-16 items-center justify-between">
            <BrandLockup />
            <button type="button" aria-label="Menü schließen" onClick={() => setOpen(false)} className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-border">
              <X className="h-4 w-4" />
            </button>
          </div>
          <nav aria-label="Mobilnavigation" className="page-wrap space-y-8 pb-16">
            {groups.map((group) => (
              <div key={group.label}>
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">{group.label}</p>
                <ul className="mt-3 grid gap-1">
                  {group.links.map((item) => (
                    <li key={item.href}>
                      {item.external ? (
                        <a href={item.href} target="_blank" rel="noopener noreferrer" className="block py-2 text-2xl font-semibold tracking-tight" onClick={() => setOpen(false)}>
                          {item.label} ↗
                        </a>
                      ) : (
                        <Link href={item.href} className="block py-2 text-2xl font-semibold tracking-tight" onClick={() => setOpen(false)}>
                          {item.label}
                        </Link>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
            <a href="#anmeldung" onClick={() => setOpen(false)} className="flex h-14 items-center justify-center rounded-2xl bg-primary text-lg font-bold text-primary-foreground">
              Abonnieren
            </a>
            <button type="button" onClick={toggleTheme} className={cn("text-sm text-muted-foreground")}>
              Darstellung: {light ? "Hell" : "Dunkel"}
            </button>
          </nav>
        </div>
      ) : null}
    </header>
  );
}
