import fs from "fs";

const csvPath = "/home/ubuntu/.cursor/projects/workspace/uploads/futuretools_top100_research_6d15.csv";
const purposes = JSON.parse(fs.readFileSync(new URL("../data/futuretools-purposes.json", import.meta.url), "utf8"));
const previous = JSON.parse(fs.readFileSync(new URL("../data/futuretools-top100.json", import.meta.url), "utf8"));
const previousByName = new Map(previous.map((item) => [item.name, item]));

const dead = new Set([
  "GeoSpy.ai",
  "Maze",
  "Godmode",
  "Any Summary",
  "Stable WarpFusion",
  "Nack",
  "Intellisay",
  "Deepfakes.lol",
  "Scribble Diffusion",
  "Wonder Dynamics",
  "ChatGPT for Search Engines",
  "kAI",
  "Musenet (OpenAI)",
]);

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (quoted) {
      if (char === '"' && text[i + 1] === '"') {
        cell += '"';
        i++;
      } else if (char === '"') quoted = false;
      else cell += char;
    } else if (char === '"') quoted = true;
    else if (char === ",") {
      row.push(cell);
      cell = "";
    } else if (char === "\n") {
      row.push(cell);
      rows.push(row);
      row = [];
      cell = "";
    } else if (char !== "\r") cell += char;
  }
  if (cell || row.length) {
    row.push(cell);
    rows.push(row);
  }
  const [header, ...body] = rows.filter((line) => line.length > 1);
  return body.map((line) => Object.fromEntries(header.map((key, index) => [key, line[index] || ""])));
}

const price = {
  ChatGPT: "freemium",
  "Eleven Labs": "freemium",
  Midjourney: "paid",
  "Pika Labs": "freemium",
  "Adobe Firefly": "paid",
  "Bing Create": "freemium",
  "Luma Dream Machine": "freemium",
  Lexica: "free",
  "NVIDIA Canvas": "free",
  "Vocal Remover": "free",
  "Animated Drawings": "free",
  "MusicLM": "free",
  "OpenAI Playground": "freemium",
  "Star By Face": "free",
  ChainClarity: "free",
  "IllusionDiffusion": "free",
  Whisk: "free",
  "Adobe Speech Enhancer": "free",
  "Dewatermark.AI": "free",
  "Ask Your PDF": "free",
  "ProfilePicture.AI": "freemium",
  "PlayPhrase.me": "freemium",
  MemeCam: "free",
  Avaturn: "free",
};

function pricingFor(name, notes) {
  if (price[name]) return price[name];
  if (/kostenlos|free/i.test(notes) && /kein abo|without account|ohne konto/i.test(notes)) return "free";
  return "freemium";
}

function categoriesFor(name) {
  const n = name.toLowerCase();
  if (/chatgpt|character|visus|ask your pdf|hello ai|playground/.test(n)) return ["ki-chatbots"];
  if (/opus|2short|qlip|livestorm|followr|ghostcut|syllaby/.test(n)) return ["social-media", "videogenerierung"];
  if (/video|pika|luma|viggle|hera|dubber|translate.video|type studio|motionleap|pixamotion|genmo|showrunner/.test(n)) return ["videogenerierung"];
  if (/voice|vocal|eleven|verbatik|uniscribe|revocalize|myvocal|speech|cleanvoice|musiclm/.test(n)) return ["audio-und-sprache"];
  if (/code|emergent|prompt/.test(n)) return ["programmierung"];
  if (/logo|mixo/.test(n)) return ["marketing", "design"];
  if (/pdf|vimcal|map this|skipit|quiz|flowrite|aurora|kartiv|to teach|touchbase/.test(n)) return ["produktivitaet"];
  if (/chain|opinly|v0 report|geospy|star by/.test(n)) return ["recherche"];
  if (/room|interior|hairstyle|outfit|magnific|enhance|eraser|clipdrop|cutout|lexica|firefly|bing|diffusion|whisk|nack|lens|image|cartoon|upscal|time machine|profile|avaturn|face swap|akool|deepbrain|kreado|wishes|meme|nvidia|illusion|qr code/.test(n)) return ["bildgenerierung"];
  return ["produktivitaet"];
}

const rows = parseCsv(fs.readFileSync(csvPath, "utf8")).filter((row) => !dead.has(row.name));
const catalog = [];
const seen = new Set();
for (const row of rows) {
  const domain = new URL(row.website).hostname.replace(/^www\./, "").toLowerCase();
  if (seen.has(domain)) continue;
  seen.add(domain);
  const purpose = purposes[row.name] || `${row.name} ist ein öffentlich erreichbares Werkzeug. Die Beschreibung bleibt knapp, weil die Produktseite wenig Festes hergibt.`;
  const pricingModel = previousByName.get(row.name)?.pricingModel === "open_source"
    ? "free"
    : previousByName.get(row.name)?.pricingModel || pricingFor(row.name, row.signup_notes || "");
  const categorySlugs = categoriesFor(row.name);
  catalog.push({
    name: row.name,
    originalUrl: row.website,
    domain,
    pricingModel,
    licenseType: "proprietary",
    categorySlugs,
    shortDescriptionDe: purpose,
    longDescriptionDe: `${purpose} Das notierte Preismodell ist ${pricingModel === "free" ? "kostenlos" : pricingModel === "paid" ? "kostenpflichtig" : "Freemium"}. Ob das noch gilt, steht auf ${domain}. Ein eigener Partnerlink ist nicht hinterlegt.`,
    featuresDe: [purpose.replace(/\.$/, "")],
    useCasesDe: [],
    partnerStatus: row.affiliate_program === "yes" ? "found" : "none_found",
    verified: true,
    beginnerFriendly: false,
    discoverySource: "futuretools-recherche",
    oss: null,
  });
}

const oss = [
  ["Ollama", "https://ollama.com/", "ollama.com", "https://github.com/ollama/ollama", "MIT", ["ki-chatbots", "programmierung"], "Ollama startet Sprachmodelle lokal auf dem eigenen Rechner.", "macOS, Linux, Windows", "Die Website erklärt die Installation für das eigene System."],
  ["Open WebUI", "https://openwebui.com/", "openwebui.com", "https://github.com/open-webui/open-webui", "MIT", ["ki-chatbots"], "Open WebUI ist eine Bedienoberfläche für lokale und angebundene Sprachmodelle.", "Docker, Linux", "Das Projekt beschreibt den Start über Docker."],
  ["llama.cpp", "https://github.com/ggml-org/llama.cpp", "github.com", "https://github.com/ggml-org/llama.cpp", "MIT", ["programmierung"], "llama.cpp führt Sprachmodelle ohne große Abhängigkeiten auf gewöhnlicher Hardware aus.", "macOS, Linux, Windows", "Bauanleitung steht im Repository."],
  ["ComfyUI", "https://github.com/comfyanonymous/ComfyUI", "github.com", "https://github.com/comfyanonymous/ComfyUI", "GPL-3.0", ["bildgenerierung"], "ComfyUI verbindet Bildmodelle über eine Knotenoberfläche.", "Windows, Linux, macOS", "Der Start läuft über Python im Repository."],
  ["Fooocus", "https://github.com/lllyasviel/Fooocus", "github.com", "https://github.com/lllyasviel/Fooocus", "GPL-3.0", ["bildgenerierung"], "Fooocus vereinfacht die Bildgenerierung mit Stable Diffusion.", "Windows, Linux", "Das Repository nennt die Startschritte."],
  ["InvokeAI", "https://invoke.ai/", "invoke.ai", "https://github.com/invoke-ai/InvokeAI", "Apache-2.0", ["bildgenerierung"], "InvokeAI ist eine Arbeitsumgebung zum Erzeugen und Bearbeiten von Bildern.", "Windows, Linux, macOS", "Installation über das Repository."],
  ["whisper.cpp", "https://github.com/ggml-org/whisper.cpp", "github.com", "https://github.com/ggml-org/whisper.cpp", "MIT", ["audio-und-sprache"], "whisper.cpp schreibt Sprache lokal in Text um.", "macOS, Linux, Windows", "Das Repository beschreibt den Bau."],
  ["LibreTranslate", "https://libretranslate.com/", "libretranslate.com", "https://github.com/LibreTranslate/LibreTranslate", "AGPL-3.0", ["textgenerierung"], "LibreTranslate übersetzt Texte und lässt sich selbst betreiben.", "Docker, Linux", "Eine Instanz kann selbst gehostet werden."],
  ["Upscayl", "https://upscayl.org/", "upscayl.org", "https://github.com/upscayl/upscayl", "AGPL-3.0", ["bildgenerierung"], "Upscayl vergrößert Bilder lokal mit offenen Modellen.", "Windows, Linux, macOS", "Es gibt Installationspakete auf der Projektseite."],
  ["Stirling PDF", "https://stirlingpdf.com/", "stirlingpdf.com", "https://github.com/Stirling-Tools/Stirling-PDF", "MIT", ["produktivitaet"], "Stirling PDF bündelt viele PDF-Aufgaben in einem selbst betreibbaren Werkzeug.", "Docker", "Der übliche Start ist ein Docker-Container."],
  ["Excalidraw", "https://excalidraw.com/", "excalidraw.com", "https://github.com/excalidraw/excalidraw", "MIT", ["design"], "Excalidraw ist ein Zeichenbrett für schnelle Skizzen im Browser.", "Web", "Die Anwendung läuft direkt im Browser."],
  ["Penpot", "https://penpot.app/", "penpot.app", "https://github.com/penpot/penpot", "MPL-2.0", ["design"], "Penpot ist ein Entwurfswerkzeug für Oberflächen, das sich selbst betreiben lässt.", "Docker, Web", "Selbstbetrieb über Docker ist beschrieben."],
  ["AppFlowy", "https://appflowy.com/", "appflowy.com", "https://github.com/AppFlowy-IO/AppFlowy", "AGPL-3.0", ["produktivitaet"], "AppFlowy sammelt Notizen und Aufgaben und kann lokal laufen.", "Windows, Linux, macOS", "Clients stehen auf der Projektseite."],
  ["Logseq", "https://logseq.com/", "logseq.com", "https://github.com/logseq/logseq", "AGPL-3.0", ["produktivitaet", "recherche"], "Logseq ist ein Notizgraph auf lokalen Dateien.", "Windows, Linux, macOS", "Die Desktop-App lässt sich von der Projektseite laden."],
  ["Joplin", "https://joplinapp.org/", "joplinapp.org", "https://github.com/laurent22/joplin", "MIT", ["produktivitaet"], "Joplin hält Notizen und Aufgaben und synchronisiert sie auf Wunsch selbst.", "Windows, Linux, macOS, Android, iOS", "Clients stehen auf der Projektseite."],
  ["Immich", "https://immich.app/", "immich.app", "https://github.com/immich-app/immich", "AGPL-3.0", ["produktivitaet"], "Immich verwaltet Fotos und Videos auf dem eigenen Server.", "Docker, Linux", "Die Dokumentation beschreibt Docker Compose."],
  ["Kdenlive", "https://kdenlive.org/", "kdenlive.org", "https://invent.kde.org/multimedia/kdenlive", "GPL-2.0-or-later", ["videogenerierung"], "Kdenlive ist ein Schnittprogramm für Video.", "Windows, Linux, macOS", "Pakete stehen auf der Projektseite."],
  ["Krita", "https://krita.org/", "krita.org", "https://invent.kde.org/graphics/krita", "GPL-3.0", ["design", "bildgenerierung"], "Krita ist ein Malprogramm für Illustration und Bildbearbeitung.", "Windows, Linux, macOS", "Installationspakete stehen auf der Projektseite."],
  ["GIMP", "https://www.gimp.org/", "gimp.org", "https://gitlab.gnome.org/GNOME/gimp", "GPL-3.0", ["bildgenerierung"], "GIMP bearbeitet Bilder, Ebenen und Formate auf dem eigenen Rechner.", "Windows, Linux, macOS", "Pakete stehen auf der Projektseite."],
  ["Audacity", "https://www.audacityteam.org/", "audacityteam.org", "https://github.com/audacity/audacity", "GPL-2.0-or-later", ["audio-und-sprache"], "Audacity nimmt Ton auf und schneidet ihn.", "Windows, Linux, macOS", "Installationspakete stehen auf der Projektseite."],
  ["OBS Studio", "https://obsproject.com/", "obsproject.com", "https://github.com/obsproject/obs-studio", "GPL-2.0", ["videogenerierung"], "OBS Studio nimmt Bildschirm und Kamera auf und kann live senden.", "Windows, Linux, macOS", "Installer stehen auf der Projektseite."],
  ["LocalAI", "https://localai.io/", "localai.io", "https://github.com/mudler/LocalAI", "MIT", ["ki-chatbots", "programmierung"], "LocalAI stellt eine lokale Schnittstelle für Sprach- und Bildmodelle bereit.", "Docker, Linux", "Der übliche Start ist Docker."],
  ["AnythingLLM", "https://anythingllm.com/", "anythingllm.com", "https://github.com/Mintplex-Labs/anything-llm", "MIT", ["recherche", "ki-chatbots"], "AnythingLLM stellt Fragen an eigene Dokumente, auch lokal.", "Windows, Linux, macOS, Docker", "Desktop und Docker sind beschrieben."],
];

for (const [name, website, domain, repo, license, categorySlugs, purpose, systems, install] of oss) {
  if (seen.has(domain) && domain !== "github.com") continue;
  if (domain === "github.com") {
    const pathKey = new URL(website).pathname;
    if (seen.has("github.com" + pathKey)) continue;
    seen.add("github.com" + pathKey);
  } else seen.add(domain);
  catalog.push({
    name,
    originalUrl: website,
    domain: domain === "github.com" ? new URL(website).hostname.replace(/^www\./, "") : domain,
    pricingModel: "free",
    licenseType: "open_source",
    categorySlugs,
    shortDescriptionDe: purpose,
    longDescriptionDe: `${purpose} Das Projekt nennt die Lizenz ${license}. Der Betrieb ist kostenlos, sofern man es selbst installiert. Ein Partnerlink ist nicht hinterlegt.`,
    featuresDe: [purpose.replace(/\.$/, "")],
    useCasesDe: [],
    partnerStatus: "none_found",
    verified: true,
    beginnerFriendly: ["Excalidraw", "Audacity", "OBS Studio"].includes(name),
    discoverySource: "open-source-recherche",
    oss: {
      projectUrl: website.startsWith("https://github.com") ? null : website,
      repoUrl: repo,
      license,
      systems: systems.split(", "),
      install,
    },
  });
}

const unique = [];
const domains = new Set();
for (const item of catalog) {
  const key = item.domain === "github.com" ? item.originalUrl : item.domain;
  if (domains.has(key)) continue;
  domains.add(key);
  unique.push(item);
}

fs.writeFileSync(new URL("../data/verified-tools.json", import.meta.url), JSON.stringify(unique, null, 2));
console.log("catalog", unique.length, "oss", unique.filter((item) => item.licenseType === "open_source").length, "found", unique.filter((item) => item.partnerStatus === "found").length);
