import { siteConfig } from "@/site.config";

/** Display legacy platform wording without rewriting editorial records or social-media references. */
export function platformText(value: string) {
  return value.replace(/Linkjagd Tools/gi, siteConfig.name);
}
