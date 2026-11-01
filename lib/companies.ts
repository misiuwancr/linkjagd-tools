import { companyMarkPaths } from "@/lib/company-marks";

export const COMPANY_STRIP_LABEL = "Für alle, die Tools von Firmen wie diesen nutzen:";

export type CompanyRule = {
  slug: string;
  name: string;
  /** Host equals this or is a subdomain of it. */
  suffixes: string[];
  /** Extra hosts that are not subdomains of suffixes. */
  exact: string[];
  /** Hosts that sit under a suffix but are third-party storefronts. */
  deny: string[];
  /** When the company shares a host with other projects, match these slugs only. */
  toolSlugs: string[];
};

/**
 * Geprüfte Zuordnung Firma → eigene Hosts oder einzelne Tool-Slugs.
 * Ein Treffer zählt nur, wenn das veröffentlichte Tool auf einem Host der Firma liegt
 * oder, bei geteilten Hosts wie github.com, der Slug ausdrücklich erlaubt ist.
 */
export const companyRules: CompanyRule[] = [
  { slug: "google", name: "Google", suffixes: ["google.com"], exact: [], deny: ["chromewebstore.google.com", "play.google.com", "sites.google.com"], toolSlugs: [] },
  { slug: "microsoft", name: "Microsoft", suffixes: ["microsoft.com"], exact: ["bing.com", "code.visualstudio.com"], deny: [], toolSlugs: [] },
  { slug: "openai", name: "OpenAI", suffixes: ["openai.com"], exact: ["chatgpt.com"], deny: [], toolSlugs: [] },
  { slug: "anthropic", name: "Anthropic", suffixes: ["anthropic.com"], exact: ["claude.com"], deny: [], toolSlugs: [] },
  { slug: "meta", name: "Meta", suffixes: ["meta.com", "facebook.com", "instagram.com", "whatsapp.com", "metademolab.com"], exact: [], deny: [], toolSlugs: [] },
  { slug: "nvidia", name: "NVIDIA", suffixes: ["nvidia.com"], exact: [], deny: [], toolSlugs: [] },
  { slug: "adobe", name: "Adobe", suffixes: ["adobe.com"], exact: [], deny: [], toolSlugs: [] },
  { slug: "amazon", name: "Amazon", suffixes: ["amazon.com", "amazonaws.com"], exact: [], deny: [], toolSlugs: [] },
  { slug: "apple", name: "Apple", suffixes: ["apple.com"], exact: [], deny: ["apps.apple.com", "itunes.apple.com"], toolSlugs: [] },
  { slug: "atlassian", name: "Atlassian", suffixes: [], exact: ["atlassian.com"], deny: [], toolSlugs: [] },
  { slug: "cloudflare", name: "Cloudflare", suffixes: [], exact: ["cloudflare.com"], deny: [], toolSlugs: [] },
  { slug: "cohere", name: "Cohere", suffixes: [], exact: ["cohere.com"], deny: [], toolSlugs: [] },
  { slug: "deepl", name: "DeepL", suffixes: [], exact: ["deepl.com"], deny: [], toolSlugs: [] },
  { slug: "discord", name: "Discord", suffixes: [], exact: ["discord.com"], deny: [], toolSlugs: [] },
  { slug: "docker", name: "Docker", suffixes: [], exact: ["docker.com"], deny: [], toolSlugs: [] },
  { slug: "dropbox", name: "Dropbox", suffixes: [], exact: ["dropbox.com"], deny: [], toolSlugs: [] },
  { slug: "figma", name: "Figma", suffixes: [], exact: ["figma.com"], deny: [], toolSlugs: [] },
  { slug: "github", name: "GitHub", suffixes: [], exact: [], deny: [], toolSlugs: ["github", "github-copilot"] },
  { slug: "grammarly", name: "Grammarly", suffixes: [], exact: ["grammarly.com"], deny: [], toolSlugs: [] },
  { slug: "midjourney", name: "Midjourney", suffixes: [], exact: ["midjourney.com"], deny: [], toolSlugs: [] },
  { slug: "mistral", name: "Mistral", suffixes: [], exact: ["mistral.ai"], deny: [], toolSlugs: [] },
  { slug: "mozilla", name: "Mozilla", suffixes: [], exact: ["mozilla.org"], deny: [], toolSlugs: [] },
  { slug: "notion", name: "Notion", suffixes: [], exact: ["notion.com"], deny: [], toolSlugs: [] },
  { slug: "paypal", name: "PayPal", suffixes: [], exact: ["paypal.com"], deny: [], toolSlugs: [] },
  { slug: "salesforce", name: "Salesforce", suffixes: [], exact: ["salesforce.com"], deny: [], toolSlugs: [] },
  { slug: "shopify", name: "Shopify", suffixes: [], exact: ["shopify.com"], deny: [], toolSlugs: [] },
  { slug: "slack", name: "Slack", suffixes: [], exact: ["slack.com"], deny: [], toolSlugs: [] },
  { slug: "spotify", name: "Spotify", suffixes: [], exact: ["spotify.com"], deny: [], toolSlugs: [] },
  { slug: "stability", name: "Stability AI", suffixes: [], exact: ["stability.ai"], deny: [], toolSlugs: [] },
  { slug: "stripe", name: "Stripe", suffixes: [], exact: ["stripe.com"], deny: [], toolSlugs: [] },
  { slug: "supabase", name: "Supabase", suffixes: [], exact: ["supabase.com"], deny: [], toolSlugs: [] },
  { slug: "telegram", name: "Telegram", suffixes: [], exact: ["telegram.org"], deny: [], toolSlugs: [] },
  { slug: "vercel", name: "Vercel", suffixes: [], exact: ["vercel.com"], deny: [], toolSlugs: [] },
  { slug: "zoom", name: "Zoom", suffixes: [], exact: ["zoom.us"], deny: [], toolSlugs: [] },
];

export type CompanyToolRef = { slug: string; domain: string };

export function companyBySlug(slug: string) {
  return companyRules.find((company) => company.slug === slug) ?? null;
}

function host(domain: string) {
  return domain.trim().toLowerCase().replace(/^www\./, "");
}

function hostIs(domain: string, root: string) {
  return domain === root || domain.endsWith(`.${root}`);
}

export function toolMatchesCompany(company: CompanyRule, tool: CompanyToolRef) {
  const domain = host(tool.domain);
  if (company.deny.some((denied) => hostIs(domain, denied))) return false;
  if (company.toolSlugs.includes(tool.slug)) return true;
  if (company.exact.includes(domain)) return true;
  return company.suffixes.some((suffix) => hostIs(domain, suffix));
}

export type DirectoryCompany = {
  slug: string;
  name: string;
  href: string;
  markPath: string | null;
  toolCount: number;
};

export function companiesForTools(rows: CompanyToolRef[]): DirectoryCompany[] {
  return companyRules.flatMap((company) => {
    const toolCount = rows.filter((row) => toolMatchesCompany(company, row)).length;
    if (toolCount < 1) return [];
    return [
      {
        slug: company.slug,
        name: company.name,
        href: `/tools?firma=${company.slug}`,
        markPath: companyMarkPaths[company.slug] ?? null,
        toolCount,
      },
    ];
  });
}
