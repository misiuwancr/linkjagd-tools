export type QualityInput = {
  name: string;
  shortDescriptionDe: string;
  originalUrl: string;
  pricingModel: string;
  categoryCount: number;
  publishStatus: string;
};

const PLACEHOLDER = /platzhalter|lorem ipsum|todo|xxx+|beispielsatz|erfunden/i;

/** Checkliste aus den vorhandenen Feldern. Prüft nicht, ob die Website gerade antwortet. */
export function qualityIssues(tool: QualityInput) {
  const issues: string[] = [];
  if (tool.name.trim().length < 2) issues.push("Name fehlt oder ist zu kurz.");
  if (tool.shortDescriptionDe.trim().length < 40) issues.push("Die deutsche Kurzbeschreibung ist sehr kurz.");
  if (PLACEHOLDER.test(tool.shortDescriptionDe) || PLACEHOLDER.test(tool.name)) issues.push("Die Beschreibung enthält einen Platzhalter.");
  if (!/^https:\/\//i.test(tool.originalUrl.trim())) issues.push("Die offizielle Adresse beginnt nicht mit https.");
  if (tool.categoryCount < 1) issues.push("Keine Kategorie gesetzt.");
  if (!["free", "freemium", "paid"].includes(tool.pricingModel)) issues.push("Preismodell ist nicht kostenlos, Freemium oder kostenpflichtig.");
  if (tool.publishStatus === "archived") issues.push("Archiviert und damit keine aktive Empfehlung.");
  return issues;
}
