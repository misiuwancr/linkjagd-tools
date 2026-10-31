export type VideoPlatform = "tiktok" | "instagram" | "youtube";

export type PublicVideo = {
  platform: VideoPlatform;
  label: string;
  pageUrl: string;
  embedUrl: string | null;
};

const ALLOWED: Record<VideoPlatform, string[]> = {
  tiktok: ["tiktok.com"],
  instagram: ["instagram.com"],
  youtube: ["youtube.com", "youtu.be"],
};

function hostOf(value: string) {
  try {
    const url = new URL(value);
    if (url.protocol !== "https:" && url.protocol !== "http:") return null;
    return url.hostname.toLowerCase().replace(/^www\./, "");
  } catch {
    return null;
  }
}

export function videoHostAllowed(value: string, platform: VideoPlatform) {
  const host = hostOf(value);
  if (!host) return false;
  return ALLOWED[platform].some((domain) => host === domain || host.endsWith(`.${domain}`));
}

export function optionalVideoUrl(value: string, platform: VideoPlatform) {
  const trimmed = value.trim();
  if (!trimmed) return "";
  if (!videoHostAllowed(trimmed, platform)) return null;
  return trimmed;
}

function youtubeId(url: URL) {
  if (url.hostname.replace(/^www\./, "") === "youtu.be") {
    return url.pathname.split("/").filter(Boolean)[0] ?? "";
  }
  const shorts = url.pathname.match(/\/shorts\/([^/?#]+)/);
  if (shorts) return shorts[1];
  return url.searchParams.get("v") ?? "";
}

export function videosFromUrls(input: {
  tiktokUrl?: string | null;
  instagramReelUrl?: string | null;
  youtubeShortUrl?: string | null;
}): PublicVideo[] {
  const items: PublicVideo[] = [];
  const tiktok = input.tiktokUrl?.trim() ?? "";
  if (tiktok && videoHostAllowed(tiktok, "tiktok")) {
    const url = new URL(tiktok);
    const match = url.pathname.match(/\/video\/(\d+)/);
    items.push({
      platform: "tiktok",
      label: "TikTok",
      pageUrl: tiktok,
      embedUrl: match ? `https://www.tiktok.com/embed/v2/${match[1]}` : null,
    });
  }
  const instagram = input.instagramReelUrl?.trim() ?? "";
  if (instagram && videoHostAllowed(instagram, "instagram")) {
    const url = new URL(instagram);
    const match = url.pathname.match(/\/(?:reel|p)\/([^/?#]+)/);
    items.push({
      platform: "instagram",
      label: "Instagram",
      pageUrl: instagram,
      embedUrl: match ? `https://www.instagram.com/reel/${match[1]}/embed` : null,
    });
  }
  const youtube = input.youtubeShortUrl?.trim() ?? "";
  if (youtube && videoHostAllowed(youtube, "youtube")) {
    const id = youtubeId(new URL(youtube));
    items.push({
      platform: "youtube",
      label: "YouTube",
      pageUrl: youtube,
      embedUrl: id ? `https://www.youtube-nocookie.com/embed/${id}` : null,
    });
  }
  return items;
}

export function hasVideoUrls(input: {
  tiktokUrl?: string | null;
  instagramReelUrl?: string | null;
  youtubeShortUrl?: string | null;
}) {
  return videosFromUrls(input).length > 0;
}
