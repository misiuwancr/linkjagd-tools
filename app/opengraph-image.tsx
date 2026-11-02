import { ImageResponse } from "next/og";
import { siteConfig } from "@/site.config";
import { BrandWordmark } from "@/components/brand-wordmark";

export const runtime = "edge";

export const alt = siteConfig.seo.title;
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpenGraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          display: "flex",
          height: "100%",
          width: "100%",
          background: "#0B0E0C",
          color: "#F4F7F2",
          padding: "72px",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex" }}><BrandWordmark width={470} height={93} color="#D0FF28" /></div>
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div style={{ display: "flex", fontSize: 68, fontWeight: 600, lineHeight: 1.05, maxWidth: 900 }}>
            {siteConfig.tagline}
          </div>
          <div style={{ display: "flex", fontSize: 28, color: "#C5CEC6" }}>
            Websites. KI-Tools. Digitale Entdeckungen.
          </div>
        </div>
      </div>
    ),
    { ...size },
  );
}
