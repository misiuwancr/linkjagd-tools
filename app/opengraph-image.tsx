import { ImageResponse } from "next/og";

export const runtime = "edge";

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
          background: "#0B0E0C",
          color: "#F4F7F2",
          padding: "72px",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", fontSize: 28, letterSpacing: 6, color: "#C6F531" }}>LINKJAGD TOOLS</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div style={{ display: "flex", fontSize: 68, fontWeight: 600, lineHeight: 1.05, maxWidth: 900 }}>
            Entdecke die besten KI-Tools.
          </div>
          <div style={{ display: "flex", fontSize: 28, color: "#C5CEC6" }}>
            Alltag, Arbeit und Projekte.
          </div>
        </div>
      </div>
    ),
    { ...size },
  );
}
