import Link from "next/link";
import { siteConfig } from "@/site.config";

const columns = [
  {
    title: "Verzeichnis",
    links: [
      { href: "/tools", label: "Alle Tools" },
      { href: "/top-20", label: "Top 20" },
      { href: "/neu", label: "Neu hinzugefügt" },
      { href: "/einreichen", label: "Tool einreichen" },
      { href: "/kategorien", label: "Kategorien" },
    ],
  },
  {
    title: "Redaktion",
    links: [
      { href: "/blog", label: "Blog" },
      { href: "/newsletter", label: "Newsletter-Archiv" },
      { href: "/glossar", label: "Glossar" },
      { href: "/faq", label: "FAQ" },
    ],
  },
  {
    title: "Mehr",
    links: [
      { href: "/ueber-uns", label: "Über uns" },
      { href: siteConfig.creator.channelUrl, label: "Videos", external: true },
      { href: "/kontakt", label: "Kontakt" },
      { href: "/merkliste", label: "Merkliste" },
    ],
  },
  {
    title: "Recht",
    links: [
      { href: "/impressum", label: "Impressum" },
      { href: "/datenschutz", label: "Datenschutz" },
      { href: "/affiliate-hinweis", label: "Affiliate-Hinweis" },
    ],
  },
];

export function SiteFooter() {
  return (
    <footer className="mt-20 border-t border-border bg-background">
      <div className="page-wrap grid gap-10 py-12 sm:grid-cols-2 lg:grid-cols-4">
        {columns.map((column) => (
          <nav key={column.title} aria-label={column.title}>
            <p className="text-sm font-semibold">{column.title}</p>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              {column.links.map((item) => (
                <li key={item.href}>
                  {item.external ? (
                    <a href={item.href} target="_blank" rel="noopener noreferrer" className="hover:text-foreground">
                      {item.label}
                    </a>
                  ) : (
                    <Link href={item.href} className="hover:text-foreground">
                      {item.label}
                    </Link>
                  )}
                </li>
              ))}
            </ul>
          </nav>
        ))}
      </div>
      <div className="border-t border-border">
        <div className="page-wrap flex flex-col gap-2 py-5 text-xs text-muted-foreground sm:flex-row sm:items-center sm:justify-between">
          <p>
            © {new Date().getFullYear()} {siteConfig.name}
          </p>
          <p>Keine erfundenen Bewertungen oder Nutzerzahlen.</p>
        </div>
      </div>
    </footer>
  );
}
