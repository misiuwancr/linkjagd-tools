"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { ChevronDown, Menu, Moon, Sun, X } from "lucide-react";
import { BrandLockup } from "@/components/brand";
import { cn } from "@/lib/utils";

const groups = [
  {
    label: "Tools",
    links: [
      { href: "/vergleiche", label: "Tools vergleichen" },
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
      { href: "/news", label: "KI-News" },
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
  const [activeGroup, setActiveGroup] = useState<string | null>(null);
  const header = useRef<HTMLElement>(null);
  useEffect(() => {
    const outside = (event: PointerEvent) => {
      if (!(event.target instanceof Element) || !event.target.closest("[data-navigation-group]")) setActiveGroup(null);
    };
    const escape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setOpen(false);
        if (activeGroup) header.current?.querySelector<HTMLButtonElement>(`[data-group="${activeGroup}"]`)?.focus();
        setActiveGroup(null);
      }
    };
    document.addEventListener("pointerdown", outside);
    document.addEventListener("keydown", escape);
    return () => {
      document.removeEventListener("pointerdown", outside);
      document.removeEventListener("keydown", escape);
    };
  }, [activeGroup]);
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
    <header ref={header} className="sticky top-0 z-40 border-b border-border/80 bg-background/85 backdrop-blur" onBlur={(event) => { if (!event.currentTarget.contains(event.relatedTarget as Node)) setActiveGroup(null); }}>
      <div className="page-wrap flex h-16 items-center justify-between gap-4">
        <BrandLockup />
        <nav aria-label="Hauptnavigation" className="hidden items-center gap-1 lg:flex">
          {groups.map((group) => (
            <div key={group.label} data-navigation-group className="relative" onMouseLeave={() => setActiveGroup(null)}>
              <button type="button" data-group={group.label} aria-expanded={activeGroup === group.label} aria-controls={`navigation-${group.label}`} onClick={() => setActiveGroup(activeGroup === group.label ? null : group.label)} className="inline-flex items-center gap-1.5 rounded-full px-3 py-2 text-base font-medium text-muted-foreground hover:text-foreground">
                {group.label}
                <ChevronDown aria-hidden="true" className={cn("h-4 w-4 transition-transform", activeGroup === group.label && "rotate-180")} />
              </button>
              <div id={`navigation-${group.label}`} hidden={activeGroup !== group.label} className="absolute left-0 top-full z-50 w-56 pt-2">
              <div className="rounded-2xl border border-border bg-card p-2 shadow-card" onClick={() => setActiveGroup(null)}>
                {group.links.map((item) =>
                  item.external ? (
                    <a key={item.href} href={item.href} target="_blank" rel="noopener noreferrer" className="block rounded-xl px-3 py-2 text-sm hover:bg-secondary">
                      {item.label} ↗
                    </a>
                  ) : (
                    <Link key={item.href} href={item.href} className="block rounded-xl px-3 py-2 text-sm hover:bg-secondary">
                      {item.label}
                    </Link>
                  ),
                )}
              </div>
              </div>
            </div>
          ))}
        </nav>
        <div className="hidden items-center gap-2 lg:flex">
          <button type="button" onClick={toggleTheme} className="rounded-full border border-border px-3 py-2 text-[13px] text-muted-foreground" aria-label="Darstellung umschalten">
            {light ? <Moon aria-hidden="true" className="h-5 w-5" /> : <Sun aria-hidden="true" className="h-5 w-5" />}
          </button>
          <a href="/newsletter#anmeldung" className="rounded-full bg-primary px-4 py-2 text-[13px] font-bold text-primary-foreground">
            Abonnieren
          </a>
        </div>
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
                        <a href={item.href} target="_blank" rel="noopener noreferrer" className="block py-2 text-lg font-medium" onClick={() => setOpen(false)}>
                          {item.label} ↗
                        </a>
                      ) : (
                        <Link href={item.href} className="block py-2 text-lg font-medium" onClick={() => setOpen(false)}>
                          {item.label}
                        </Link>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
            <a href="/newsletter#anmeldung" onClick={() => setOpen(false)} className="flex h-12 items-center justify-center rounded-full bg-primary text-base font-bold text-primary-foreground">
              Abonnieren
            </a>
            <button type="button" onClick={toggleTheme} aria-label="Darstellung umschalten" className="inline-flex items-center gap-2 text-base text-muted-foreground">
              {light ? <Moon className="h-5 w-5" aria-hidden="true" /> : <Sun className="h-5 w-5" aria-hidden="true" />} Darstellung: {light ? "Hell" : "Dunkel"}
            </button>
          </nav>
        </div>
      ) : null}
    </header>
  );
}
