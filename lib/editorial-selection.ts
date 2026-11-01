/** Redaktionelle Startauswahl zur Prüfung im PR, keine Community-Rangliste. */
export const editorialStarterSlugs = [
  "chatgpt", "claude", "gemini", "notebooklm", "deepl", "github-copilot",
  "cursor", "ollama", "comfyui", "midjourney", "adobe-firefly", "runway",
  "whisper-cpp", "n8n", "make", "zapier", "notion", "obsidian", "open-webui", "microsoft-copilot",
] as const;
export function starterRank(slug: string): number | null {
  const index = editorialStarterSlugs.findIndex((item) => item === slug);
  return index < 0 ? null : index + 1;
}
