import Link from "next/link";
import { siteConfig } from "@/site.config";

export function SiteFooter() {
  return (
    <footer className="mt-16 border-t border-border bg-white">
      <div className="page-wrap grid gap-8 py-10 sm:grid-cols-[1.4fr_1fr]">
        <div>
          <p className="text-sm font-semibold">{siteConfig.name}</p>
          <p className="mt-2 max-w-md text-sm leading-6 text-muted-foreground">
            Ein deutschsprachiges Verzeichnis von {siteConfig.creator.name}, bekannt vom TikTok-Kanal{" "}
            {siteConfig.creator.channel}. Empfehlungen sind redaktionell. Partnerlinks sind gekennzeichnet.
          </p>
        </div>
        <nav aria-label="Fußnavigation" className="grid grid-cols-2 gap-2 text-sm">
          {siteConfig.footer.map((item) => (
            <Link key={item.href} href={item.href} className="text-muted-foreground hover:text-foreground">
              {item.label}
            </Link>
          ))}
          <Link href="/admin" className="text-muted-foreground hover:text-foreground">
            Redaktion
          </Link>
        </nav>
      </div>
      <div className="border-t border-border">
        <div className="page-wrap flex flex-col gap-2 py-4 text-xs text-muted-foreground sm:flex-row sm:justify-between">
          <p>
            © {new Date().getFullYear()} {siteConfig.name}. Basiert auf dem MIT-lizenzierten Verzeichnis von 9d8.
          </p>
          <p>Keine erfundenen Bewertungen oder Nutzerzahlen.</p>
        </div>
      </div>
    </footer>
  );
}
