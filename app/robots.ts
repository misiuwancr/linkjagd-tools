import type { MetadataRoute } from "next";
import { siteConfig } from "@/site.config";
import { indexingPolicy } from "@/lib/indexing";

export default function robots(): MetadataRoute.Robots {
  const base = siteConfig.url.replace(/\/$/, "");
  const policy = indexingPolicy();
  if (!policy.index) {
    return {
      rules: { userAgent: "*", disallow: "/" },
      host: base,
    };
  }
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/admin", "/api/", "/go/"],
    },
    sitemap: `${base}/sitemap.xml`,
    host: base,
  };
}
