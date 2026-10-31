import fs from "fs";
import path from "path";

const research = JSON.parse(fs.readFileSync("/tmp/ft-research.json", "utf8"));
const purposes = JSON.parse(fs.readFileSync(new URL("../data/futuretools-purposes.json", import.meta.url), "utf8"));

const priceModel = {
  free: "free",
  freemium: "freemium",
  paid: "paid",
  open_source: "open_source",
  github: "open_source",
};
const priceDe = {
  free: "Kostenlos",
  freemium: "Freemium",
  paid: "Kostenpflichtig",
  open_source: "Open Source",
};
const categoryDe = {
  "ki-chatbots": "KI-Chatbots",
  bildgenerierung: "Bildgenerierung",
  videogenerierung: "Videogenerierung",
  programmierung: "Programmierung",
  produktivitaet: "Produktivität",
  automatisierung: "Automatisierung",
  marketing: "Marketing",
  "social-media": "Social Media",
  recherche: "Recherche",
  textgenerierung: "Textgenerierung",
  "audio-und-sprache": "Audio und Sprache",
  design: "Design",
  bildung: "Bildung",
  "e-commerce": "E-Commerce",
};

const partnerOverride = {
  "Magnific AI": { partner: "ja", programUrl: "https://www.magnific.com/affiliates" },
  Mixo: { partner: "ja", programUrl: "https://mixo.io/affiliates" },
  "DeepBrain AI": { partner: "ja", programUrl: "https://www.aistudios.com/affiliate" },
};

function mapCategories(slugs) {
  const blob = ` ${(slugs || []).join(" ")} `;
  const out = [];
  const add = (id) => {
    if (!out.includes(id)) out.push(id);
  };
  if (/ chat |^chat | chat-/.test(blob) || blob.includes(" chat")) add("ki-chatbots");
  if (/generative-video|video-editing|motion-capture/.test(blob)) add("videogenerierung");
  if (/(^| )avatar/.test(blob) || blob.includes("avatar")) add("videogenerierung");
  if (/generative-art|image-improvement|image-scanning/.test(blob)) add("bildgenerierung");
  if (/generative-code/.test(blob)) add("programmierung");
  if (/automation/.test(blob)) add("automatisierung");
  if (/social-media/.test(blob)) add("social-media");
  if (/marketing|copywriting/.test(blob)) add("marketing");
  if (/research|aggregator|ai-detection/.test(blob)) add("recherche");
  if (/text-to-speech|speech-to-text|voice-modulation|podcast| music/.test(blob) || blob.includes("music")) {
    add("audio-und-sprache");
  }
  if (/prompt-guides/.test(blob)) add("textgenerierung");
  if (/productivity/.test(blob)) add("produktivitaet");
  if (/self-improvement|to-teach|teach/.test(blob)) add("bildung");
  if (/translation/.test(blob)) add("textgenerierung");
  if (/design/.test(blob)) add("design");
  if ((/for-fun|gaming/.test(blob)) && out.length === 0) add("bildgenerierung");
  if (out.length === 0) add("produktivitaet");
  return out.slice(0, 2);
}

const catalog = research.map((row, index) => {
  const purpose = purposes[row.name];
  if (!purpose) throw new Error(`Beschreibung fehlt: ${row.name}`);
  const pricingModel = priceModel[row.pricing];
  if (!pricingModel) throw new Error(`Preis fehlt: ${row.name} ${row.pricing}`);
  const categorySlugs = mapCategories(row.categories);
  const override = partnerOverride[row.name];
  const partner = override?.partner || row.partner;
  const programUrl = partner === "ja" ? override?.programUrl || row.programUrl || "" : "";
  if (partner === "ja" && !programUrl) throw new Error(`Programm-URL fehlt: ${row.name}`);
  if (/futuretools|ref=|via=matt|\?via=/i.test(row.url)) throw new Error(`Tracking-URL: ${row.name} ${row.url}`);
  const shortDescriptionDe = purpose.length <= 280 ? purpose : `${purpose.slice(0, 277)}...`;
  const labels = categorySlugs.map((slug) => categoryDe[slug]).join(" und ");
  const longDescriptionDe = [
    purpose,
    `${row.name} ist hier den Kategorien ${labels} zugeordnet. Das in der Beliebtheitsliste notierte Preismodell ist ${priceDe[pricingModel]}. Ob das noch stimmt, steht auf ${row.domain}.`,
    "Dieser Text ist für Linkjagd Tools neu auf Deutsch formuliert. Es ist kein Partnerlink hinterlegt, der Eintrag bleibt ein Entwurf.",
  ].join(" ");
  return {
    rank: index + 1,
    name: row.name,
    originalUrl: row.url,
    domain: row.domain,
    pricingModel,
    categorySlugs,
    shortDescriptionDe,
    longDescriptionDe,
    featuresDe: [purpose.replace(/\.$/, ""), "Maßgeblich für den Preis ist die eigene Website."],
    partner,
    programUrl,
    discoverySource: "futuretools-top100",
    urlNote: row.urlNote || "",
  };
});

const target = path.join(path.dirname(new URL(import.meta.url).pathname), "../data/futuretools-top100.json");
fs.writeFileSync(target, JSON.stringify(catalog, null, 2));
console.log("wrote", catalog.length, "ja", catalog.filter((item) => item.partner === "ja").length);
