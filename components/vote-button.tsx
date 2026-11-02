"use client";
import { useEffect, useState } from "react";
import { ChevronUp } from "lucide-react";

export function VoteButton({ slug, name }: { slug: string; name: string }) {
  const [count, setCount] = useState<number | null>(null);
  const [enabled, setEnabled] = useState(false);
  const [voted, setVoted] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  useEffect(() => {
    const controller = new AbortController();
    fetch(`/api/votes/${slug}`, { signal: controller.signal, cache: "no-store" }).then((r) => r.ok ? r.json() : null).then((data) => {
      if (data?.enabled) { setEnabled(true); setCount(data.count); }
    }).catch(() => {});
    return () => controller.abort();
  }, [slug]);
  async function vote() {
    setBusy(true); setMessage("");
    try {
      const response = await fetch(`/api/votes/${slug}`, { method: "POST" });
      const data = await response.json();
      if (!response.ok) { setMessage(data.error || "Bitte später erneut versuchen."); return; }
      setCount(data.count); setVoted(true);
      setMessage(data.duplicate ? "Du hast bereits abgestimmt." : "Danke für deine Stimme!");
    } catch { setMessage("Bitte später erneut versuchen."); } finally { setBusy(false); }
  }
  if (!enabled) return null;
  return <div className="mt-3">
    <button type="button" onClick={vote} disabled={!enabled || voted || busy} aria-label={`Für ${name} stimmen`} aria-pressed={voted} title="Zähler: 1 Startwert plus echte Stimmen. Ohne Konto abstimmen." className="inline-flex items-center gap-1 rounded-lg border border-border px-3 py-1.5 text-sm disabled:opacity-60">
      <ChevronUp className="h-4 w-4" aria-hidden="true" />{count ?? "–"}{busy ? " …" : ""}
    </button>
    <p className="mt-1 text-xs text-muted-foreground">{enabled ? "1 Startwert + echte Stimmen" : "Voting noch nicht freigeschaltet"}</p>
    <p aria-live="polite" className="text-xs text-muted-foreground">{message}</p>
  </div>;
}
