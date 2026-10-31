export interface AffiliateNetworkAdapter {
  readonly id: string;
  readonly label: string;
  describe(): { termsNote: string };
}

class PlaceholderNetwork implements AffiliateNetworkAdapter {
  constructor(
    readonly id: string,
    readonly label: string,
    private readonly note: string,
  ) {}

  describe() {
    return { termsNote: this.note };
  }
}

const manualNote =
  "Links werden von der Redaktion eingetragen. Es gibt keine automatische Bewerbung und keine API.";

export const affiliateNetworks: AffiliateNetworkAdapter[] = [
  new PlaceholderNetwork("manual", "Manuell", manualNote),
  new PlaceholderNetwork(
    "direct",
    "Direktes Partnerprogramm",
    "Vormerkung für ein späteres direktes Programm. Keine Anbindung in Phase 1.",
  ),
  new PlaceholderNetwork(
    "awin",
    "Awin",
    "Platzhalter. Vor einer Anbindung AGB, Creator-Richtlinien und erlaubte Werbemittel prüfen.",
  ),
  new PlaceholderNetwork(
    "impact",
    "Impact",
    "Platzhalter. Keine Zugangsdaten und keine Programmsuche in dieser Version.",
  ),
  new PlaceholderNetwork(
    "cj",
    "CJ",
    "Platzhalter. Keine automatische Bewerbung.",
  ),
  new PlaceholderNetwork(
    "partnerize",
    "Partnerize",
    "Platzhalter. Keine automatische Link-Erzeugung.",
  ),
];

const byId = new Map(affiliateNetworks.map((network) => [network.id, network]));

export function listAffiliateNetworks() {
  return affiliateNetworks;
}

export function getAffiliateNetwork(id: string) {
  return byId.get(id) ?? null;
}
