export type IconCandidate = { href: string; score: number };

const PROXY_HOSTS = ["google.com", "gstatic.com", "duckduckgo.com", "yandex.net", "faviconkit.com"];

export function isFaviconProxy(href: string) {
  try {
    const host = new URL(href).hostname.replace(/^www\./, "");
    return PROXY_HOSTS.some((item) => host === item || host.endsWith(`.${item}`));
  } catch {
    return true;
  }
}

export function parseIconCandidates(html: string, pageUrl: string): IconCandidate[] {
  const found: IconCandidate[] = [];
  const linkTags = html.match(/<link\b[^>]*>/gi) ?? [];
  for (const tag of linkTags) {
    const rel = /rel=["']([^"']+)["']/i.exec(tag)?.[1]?.toLowerCase() ?? "";
    const href = /href=["']([^"']+)["']/i.exec(tag)?.[1];
    if (!href) continue;
    const sizes = /sizes=["']([^"']+)["']/i.exec(tag)?.[1] ?? "";
    const size = Math.max(
      0,
      ...sizes.split(/\s+/).map((part) => Number(part.split("x")[0]) || 0),
    );
    let score = 0;
    if (rel.includes("apple-touch-icon")) score = 300 + size;
    else if (rel.includes("icon")) score = 100 + size;
    else continue;
    try {
      const absolute = new URL(href, pageUrl).toString();
      if (!isFaviconProxy(absolute)) found.push({ href: absolute, score });
    } catch {
      continue;
    }
  }
  const manifest = /<link\b[^>]*rel=["'][^"']*manifest[^"']*["'][^>]*>/i.exec(html)?.[0];
  const manifestHref = manifest ? /href=["']([^"']+)["']/i.exec(manifest)?.[1] : undefined;
  return found.sort((a, b) => b.score - a.score).concat(
    manifestHref
      ? [{ href: new URL(manifestHref, pageUrl).toString(), score: 0 }].filter((item) => !isFaviconProxy(item.href))
      : [],
  );
}

export function parseManifestIcons(manifest: { icons?: { src?: string; sizes?: string; purpose?: string }[] }, pageUrl: string) {
  const icons = manifest.icons ?? [];
  return icons
    .flatMap((icon) => {
      if (!icon.src) return [];
      const size = Number(String(icon.sizes ?? "").split("x")[0]) || 0;
      const purpose = icon.purpose ?? "";
      if (purpose.includes("monochrome")) return [];
      try {
        const href = new URL(icon.src, pageUrl).toString();
        if (isFaviconProxy(href)) return [];
        return [{ href, score: 200 + size }];
      } catch {
        return [];
      }
    })
    .sort((a, b) => b.score - a.score);
}

type Rule = { agent: string; allow: string[]; disallow: string[] };

export function robotsAllows(robotsTxt: string, path: string, agent = "linkjagdtools") {
  const groups: Rule[] = [];
  let current: Rule | null = null;
  for (const raw of robotsTxt.split(/\r?\n/)) {
    const line = raw.replace(/#.*$/, "").trim();
    if (!line) continue;
    const match = /^([a-z-]+)\s*:\s*(.*)$/i.exec(line);
    if (!match) continue;
    const key = match[1].toLowerCase();
    const value = match[2].trim();
    if (key === "user-agent") {
      current = { agent: value.toLowerCase(), allow: [], disallow: [] };
      groups.push(current);
    } else if (current && (key === "allow" || key === "disallow")) {
      current[key].push(value);
    }
  }
  const specific = groups.filter((group) => group.agent === agent);
  const star = groups.filter((group) => group.agent === "*");
  const rules = specific.length > 0 ? specific : star;
  let allowed = true;
  let best = -1;
  for (const group of rules) {
    for (const pattern of group.disallow) {
      if (pattern && path.startsWith(pattern) && pattern.length > best) {
        best = pattern.length;
        allowed = false;
      }
    }
    for (const pattern of group.allow) {
      if (pattern && path.startsWith(pattern) && pattern.length >= best) {
        best = pattern.length;
        allowed = true;
      }
    }
  }
  return allowed;
}
