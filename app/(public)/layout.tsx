import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";

import { publishedAiNews } from "@/lib/ai-news";
import { newsletterOpen } from "@/lib/newsletter";

export default function PublicLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col">
      <a
        href="#inhalt"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-full focus:bg-card focus:px-4 focus:py-2"
      >
        Zum Inhalt
      </a>
      <SiteHeader newsletterAvailable={newsletterOpen()} newsAvailable={publishedAiNews().length > 0} />
      <main id="inhalt" className="flex-1">
        {children}
      </main>
      <SiteFooter />
    </div>
  );
}
