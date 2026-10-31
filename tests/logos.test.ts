import { describe, expect, it } from "vitest";
import { isFaviconProxy, parseIconCandidates, parseManifestIcons, robotsAllows } from "@/lib/logos";

describe("Logo-Auswahl", () => {
  it("bevorzugt das Apple-Touch-Icon der eigenen Seite", () => {
    const html = `
      <link rel="icon" href="/favicon.ico" sizes="32x32">
      <link rel="apple-touch-icon" href="/apple-touch-icon.png">
      <link rel="icon" href="https://www.google.com/s2/favicons?domain=example.com">
    `;
    const icons = parseIconCandidates(html, "https://example.com/app");
    expect(icons[0]?.href).toBe("https://example.com/apple-touch-icon.png");
    expect(icons.some((item) => isFaviconProxy(item.href))).toBe(false);
  });

  it("liest Icons aus einem Manifest und achtet robots.txt", () => {
    const icons = parseManifestIcons(
      { icons: [{ src: "/icon-192.png", sizes: "192x192" }, { src: "/mono.svg", purpose: "monochrome" }] },
      "https://example.com/manifest.webmanifest",
    );
    expect(icons.map((item) => item.href)).toEqual(["https://example.com/icon-192.png"]);
    const robots = "User-agent: *\nDisallow: /private\nAllow: /private/icon.png\n";
    expect(robotsAllows(robots, "/private/icon.png")).toBe(true);
    expect(robotsAllows(robots, "/private/secret")).toBe(false);
    expect(robotsAllows("User-agent: linkjagdtools\nDisallow: /\n\nUser-agent: *\nAllow: /\n", "/", "linkjagdtools")).toBe(false);
  });
});
