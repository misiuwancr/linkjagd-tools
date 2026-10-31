import { describe, expect, it } from "vitest";
import { optionalVideoUrl, videosFromUrls } from "@/lib/videos";
import { publicListQuery, directoryHref } from "@/lib/tools/query";

describe("Video-Adressen", () => {
  it("erlaubt nur die drei Plattformen und leere Felder", () => {
    expect(optionalVideoUrl("", "tiktok")).toBe("");
    expect(optionalVideoUrl("https://www.tiktok.com/@linkjagd/video/1", "tiktok")).toContain("tiktok.com");
    expect(optionalVideoUrl("https://vm.tiktok.com/ZMabc/", "tiktok")).toContain("tiktok.com");
    expect(optionalVideoUrl("https://example.com/video", "tiktok")).toBeNull();
    expect(optionalVideoUrl("https://youtu.be/abc123", "youtube")).toContain("youtu.be");
    expect(optionalVideoUrl("https://vimeo.com/1", "youtube")).toBeNull();
    expect(optionalVideoUrl("https://www.instagram.com/reel/AbC/", "instagram")).toContain("instagram.com");
  });

  it("baut Einbettungen erst als Adresse, nicht als geladenes Frame", () => {
    const videos = videosFromUrls({
      tiktokUrl: "https://www.tiktok.com/@linkjagd/video/1234567890",
      youtubeShortUrl: "https://www.youtube.com/shorts/abcdefghijk",
      instagramReelUrl: "https://www.instagram.com/reel/AbCdEf/",
    });
    expect(videos.map((item) => item.embedUrl)).toEqual([
      "https://www.tiktok.com/embed/v2/1234567890",
      "https://www.instagram.com/reel/AbCdEf/embed",
      "https://www.youtube-nocookie.com/embed/abcdefghijk",
    ]);
  });

  it("filtert das Verzeichnis auf Videos aus dem Kanal", () => {
    const query = publicListQuery({ video: "ja", seite: "2" });
    expect(query.fromVideo).toBe(true);
    expect(directoryHref("/tools", query)).toBe("/tools?video=ja&seite=2");
    expect(publicListQuery({ video: "nein" }).fromVideo).toBe(false);
  });
});
