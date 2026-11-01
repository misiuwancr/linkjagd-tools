export function rankMovement(current: number | null, previous: unknown): "up" | "down" | "unchanged" {
  if (!Number.isInteger(current) || current! < 1 || typeof previous !== "number" || !Number.isInteger(previous) || previous < 1) return "unchanged";
  return current! < previous ? "up" : current! > previous ? "down" : "unchanged";
}

export function previousRanks(value: string): Record<string, number> {
  try {
    const parsed: unknown = JSON.parse(value);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return {};
    return Object.fromEntries(Object.entries(parsed).filter(([, rank]) => typeof rank === "number" && Number.isInteger(rank) && rank > 0));
  } catch { return {}; }
}
