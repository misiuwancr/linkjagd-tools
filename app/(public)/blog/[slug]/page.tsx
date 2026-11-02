import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getDb } from "@/db/client";
import { JsonLd } from "@/components/json-ld";
import { renderMarkdown } from "@/lib/markdown";
import { getNewsBySlug } from "@/lib/tools/repository";
import { siteConfig } from "@/site.config";
import { comparisonHref, getComparison } from "@/lib/comparisons";
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
  return (
    <article className="page-wrap max-w-3xl py-12 sm:py-16">
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "BlogPosting",
          headline: post.title,
          description: post.excerpt,
          datePublished: post.publishedAt?.toISOString(),
          inLanguage: "de",
          url: new URL(`/blog/${post.slug}`, siteConfig.url).toString(),
        }}
      />
      <Link href="/blog" className="text-sm text-muted-foreground hover:text-foreground">
        Blog
      </Link>
      <h1 className="mt-4 text-4xl font-bold tracking-tight sm:text-5xl">{post.title}</h1>
      <p className="mt-4 text-lg text-muted-foreground">{post.excerpt}</p>
      {post.coverImageUrl ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={post.coverImageUrl} alt="" className="mt-6 w-full rounded-2xl border border-border" />
      ) : null}
      <div
        className="prose-invert mt-8 space-y-4 text-base leading-8 [&_a]:underline [&_h2]:mt-8 [&_h2]:text-2xl [&_h2]:font-bold [&_ul]:list-disc [&_ul]:pl-5"
        dangerouslySetInnerHTML={{ __html: renderMarkdown(post.body) }}
      />
    </article>
  );
}
