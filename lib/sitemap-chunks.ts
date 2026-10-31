export const TOOLS_PER_SITEMAP = 5000;

export function sitemapChunkCount(toolCount: number) {
  return Math.max(1, Math.ceil(toolCount / TOOLS_PER_SITEMAP));
}
