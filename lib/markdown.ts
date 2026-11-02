function escapeHtml(value: string) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export type MarkdownOptions = { outbound?: Record<string, { href: string; affiliate: boolean }>; siteUrl?: string };
function inline(value: string, options: MarkdownOptions) {
  const safe = escapeHtml(value);
  return safe
    .replace(/\[([^\]]+)\]\(((?:https?:\/\/|\/(?!\/))[^\s)]+)\)/g, (_match, label: string, href: string) => {
      let local = href;
      if (options.siteUrl) { try { const parsed = new URL(href.replace(/&amp;/g, "&"), options.siteUrl); if (parsed.origin === new URL(options.siteUrl).origin) local = parsed.pathname; } catch { return label; } }
      const go = local.match(/^\/go\/([a-z0-9]+(?:-[a-z0-9]+)*)(?:\?[^ ]*)?$/);
      if (go) { const target = options.outbound?.[go[1]]; return target ? `<a href="${escapeHtml(target.href)}" rel="${target.affiliate ? "sponsored nofollow noopener" : "nofollow noopener"}">${label}${target.affiliate ? " · Anzeige" : ""}</a>` : label; }
      if (href.includes("\\") || /%5c|%2f/i.test(href)) return label;
      try { const url = new URL(href.replace(/&amp;/g, "&"), "https://internal.invalid"); if (url.username || url.password) return label; } catch { return label; }
      return `<a href="${href}" rel="noopener noreferrer">${label}</a>`;
    })
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
}

export function renderMarkdown(source: string, options: MarkdownOptions = {}) {
  const lines = source.replace(/\r\n/g, "\n").split("\n");
  const html: string[] = [];
  let list: string[] = [];
  const flush = () => {
    if (list.length === 0) return;
    html.push(`<ul>${list.join("")}</ul>`);
    list = [];
  };
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) {
      flush();
      continue;
    }
    if (trimmed.startsWith("- ")) {
      list.push(`<li>${inline(trimmed.slice(2), options)}</li>`);
      continue;
    }
    flush();
    if (trimmed.startsWith("### ")) html.push(`<h3>${inline(trimmed.slice(4), options)}</h3>`);
    else if (trimmed.startsWith("## ")) html.push(`<h2>${inline(trimmed.slice(3), options)}</h2>`);
    else if (trimmed.startsWith("# ")) html.push(`<h2>${inline(trimmed.slice(2), options)}</h2>`);
    else html.push(`<p>${inline(trimmed, options)}</p>`);
  }
  flush();
  return html.join("");
}
