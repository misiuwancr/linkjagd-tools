import { z } from "zod";
import entries from "@/data/ai-news.json";

const httpsUrl = z.string().url().refine((url) => new URL(url).protocol === "https:");
export const aiNewsSchema = z.object({
  id: z.string().min(1), title: z.string().min(1), summary: z.string().min(1),
  category: z.string().min(1), publishedAt: z.string().datetime({ offset: true }),
  sourceName: z.string().min(1), sourceUrl: httpsUrl,
  imageUrl: z.string().refine((url) => /^\/(?!\/)/.test(url) || (url.startsWith("https:") && httpsUrl.safeParse(url).success)).optional(),
});
export type AiNews = z.infer<typeof aiNewsSchema>;
export function publishedAiNews(now = new Date()): AiNews[] {
  return z.array(aiNewsSchema).parse(entries)
    .filter((item) => new Date(item.publishedAt).getTime() <= now.getTime())
    .sort((a, b) => b.publishedAt.localeCompare(a.publishedAt));
}
