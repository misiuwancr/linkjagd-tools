export function germanFromHtml(html: string) {
  if (/<html\b[^>]*\blang=["']de(?:-[A-Za-z]+)?["']/i.test(html)) return "ja" as const;
  if (/hreflang=["']de(?:-[A-Za-z]+)?["']/i.test(html)) return "ja" as const;
  return null;
}
