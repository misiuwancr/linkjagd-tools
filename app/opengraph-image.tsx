import { ImageResponse } from "next/og";

export const alt = "Linkjagd Tools";
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
          background: "#1C1915",
          color: "#F6F1EA",
          padding: "72px",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", fontSize: 28, letterSpacing: 6, color: "#E08A45" }}>LINKJAGD TOOLS</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div style={{ display: "flex", fontSize: 68, fontWeight: 600, lineHeight: 1.05, maxWidth: 900 }}>
            Entdecke die besten KI-Tools.
          </div>
          <div style={{ display: "flex", fontSize: 28, color: "#D9D0C5" }}>
            Alltag, Arbeit und Projekte.
          </div>
        </div>
      </div>
    ),
    { ...size },
  );
}
