import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getDb } from "@/db/client";
import { JsonLd } from "@/components/json-ld";
import { renderMarkdown } from "@/lib/markdown";
import { getNewsBySlug } from "@/lib/tools/repository";
import { siteConfig } from "@/site.config";
import { comparisonHref, getComparison } from "@/lib/comparisons";
import { publicArticles, linkedToolSlugs } from "@/lib/content-hub";
import { ArticleConnections } from "@/components/article-connections";
import { blogTopics } from "@/lib/blog-metadata";
import { outboundTool } from "@/components/provider-link";
import { goHref } from "@/lib/affiliate/context";
import { ComparisonPage } from "@/components/comparison-page";

export const revalidate = 60;

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const comparison = getComparison(params.slug);
  if (comparison) return { title: comparison.title, description: comparison.intro, alternates: { canonical: comparisonHref(comparison) }, openGraph: { title: comparison.title, description: comparison.intro } };
  const post = await getNewsBySlug(await getDb(), params.slug);
  if (!post || post.status !== "published") return { title: "Beitrag" };
  const title = post.seoTitle || post.title;
  const description = post.seoDescription || post.excerpt;
  return { title, description, alternates: { canonical: `/blog/${post.slug}` }, openGraph: { title, description } };
}

export default async function BlogPostPage({ params }: { params: { slug: string } }) {
  const comparison = getComparison(params.slug);
  if (comparison) return <ComparisonPage comparison={comparison} />;
  const post = await getNewsBySlug(await getDb(), params.slug);
  if (!post || post.status !== "published") notFound();
  const articles = await publicArticles();
  const article = articles.find((item) => item.slug === post.slug)!;
  const outbound: Record<string, { href: string; affiliate: boolean }> = {};
  await Promise.all(linkedToolSlugs(post.body).map(async (slug) => { const target = await outboundTool(slug); if (target) outbound[slug] = { href: goHref(slug, `/blog/${post.slug}`, "article"), affiliate: target.decision.kind === "affiliate" }; }));
  return (
    <article className="page-wrap max-w-3xl py-12 sm:py-16">
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "BlogPosting",
          headline: post.title,
          description: post.excerpt,
          datePublished: post.publishedAt?.toISOString(),
          dateModified: post.updatedAt.toISOString(),
          articleSection: blogTopics.find((topic) => topic.value === article.topic)?.label,
          publisher: { "@type": "Organization", name: siteConfig.name },
          inLanguage: "de",
          url: new URL(`/blog/${post.slug}`, siteConfig.url).toString(),
        }}
      />
      <Link href="/blog" className="text-sm text-muted-foreground hover:text-foreground">
        Blog
      </Link>
      <p className="mt-4 text-sm font-semibold text-hunt">{blogTopics.find((topic) => topic.value === article.topic)?.label}</p>
      <h1 className="mt-4 text-4xl font-bold tracking-tight sm:text-5xl">{post.title}</h1>
      <p className="mt-4 text-lg text-muted-foreground">{post.excerpt}</p>
      <p className="mt-4 text-sm leading-7 text-muted-foreground">{post.publishedAt ? <>Veröffentlicht: <time dateTime={post.publishedAt.toISOString()}>{post.publishedAt.toLocaleDateString("de-DE", { timeZone: "Europe/Berlin" })}</time>. </> : null}Anbieterfunktionen können sich ändern. Mit „Anzeige“ gekennzeichnete Links können eine Provision auslösen. Redaktionelle Einordnung und Partnerstatus sind getrennt. <Link href="/affiliate-hinweis" className="underline">Affiliate-Hinweis</Link></p>
      {post.coverImageUrl ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={post.coverImageUrl} alt="" className="mt-6 w-full rounded-2xl border border-border" />
      ) : null}
      <div
        className="prose-invert mt-8 space-y-4 break-words text-base leading-8 [overflow-wrap:anywhere] [&_a]:underline [&_h2]:mt-8 [&_h2]:text-2xl [&_h2]:font-bold [&_ul]:list-disc [&_ul]:pl-5"
        dangerouslySetInnerHTML={{ __html: renderMarkdown(post.body, { outbound, siteUrl: siteConfig.url }) }}
      />
      <ArticleConnections article={article} />
    </article>
  );
}
