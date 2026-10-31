"use client";

import { useState } from "react";
import type { PublicVideo } from "@/lib/videos";

export function VideoGate({ video }: { video: PublicVideo }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="overflow-hidden rounded-2xl border border-border bg-card">
      {open && video.embedUrl ? (
        <iframe
          title={`${video.label}-Video`}
          src={video.embedUrl}
          className="aspect-[9/16] max-h-[640px] w-full bg-black"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      ) : (
        <div className="flex aspect-[9/16] max-h-[280px] flex-col items-start justify-end gap-3 bg-black p-5">
          <p className="text-sm text-white/80">
            Das Video von {video.label} wird erst geladen, wenn du es selbst öffnest. Vorher geht keine Anfrage an {video.label}.
          </p>
          {video.embedUrl ? (
            <button
              type="button"
              onClick={() => setOpen(true)}
              className="rounded-xl bg-hunt px-4 py-2 text-sm font-semibold text-primary-foreground"
            >
              Video laden
            </button>
          ) : (
            <a
              href={video.pageUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-xl bg-hunt px-4 py-2 text-sm font-semibold text-primary-foreground"
            >
              Video bei {video.label} öffnen
            </a>
          )}
        </div>
      )}
    </div>
  );
}
