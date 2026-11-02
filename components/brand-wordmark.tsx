import { brandGlyphs, brandViewBox } from "@/lib/brand-assets";

export function BrandWordmark({ className, color = "currentColor", width = 188, height = 37 }: { className?: string; color?: string; width?: number; height?: number }) {
  return <svg viewBox={brandViewBox} width={width} height={height} className={className} fill={color} aria-hidden="true">
    {brandGlyphs.map(glyph => <path key={glyph.x} transform={`translate(${glyph.x} 0)`} d={glyph.path} fillRule="evenodd" />)}
  </svg>;
}
