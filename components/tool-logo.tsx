import Image from "next/image";
import { cn } from "@/lib/utils";

export function ToolLogo({
  name,
  logo,
  size = 48,
  className,
}: {
  name: string;
  logo?: string | null;
  size?: number;
  className?: string;
}) {
  const initials = name
    .split(/\s+/)
    .map((part) => part.replace(/[^A-Za-zÄÖÜäöüß]/g, ""))
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join("")
    .toUpperCase();
  const box = { width: size, height: size };
  if (logo && /\.(png|jpe?g|webp|gif)$/i.test(logo)) {
    return (
      <Image
        src={logo}
        alt=""
        width={size}
        height={size}
        className={cn("rounded-xl border border-border bg-card object-cover", className)}
        style={box}
      />
    );
  }
  if (logo && logo.endsWith(".svg")) {
    return (
      // SVG-Logos bleiben als Bild, next/image optimiert sie in dieser Version nicht.
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src={logo}
        alt=""
        width={size}
        height={size}
        className={cn("rounded-xl border border-border bg-card object-cover", className)}
      />
    );
  }
  return (
    <span
      aria-hidden="true"
      className={cn(
        "inline-grid shrink-0 place-items-center rounded-xl bg-black font-semibold text-hunt ring-1 ring-hunt/40",
        className,
      )}
      style={{ width: size, height: size, fontSize: size < 40 ? 12 : 15 }}
    >
      {initials || "LJ"}
    </span>
  );
}
