"use client";

import { useFormState } from "react-dom";
import { saveToolAction, type ActionState } from "@/lib/actions/admin";
import { licenseOptions, pricingOptions, publishLabels } from "@/lib/labels";
import type { LicenseType, PricingModel, PublishStatus } from "@/db/schema";

const publishStatuses = ["draft", "published", "archived"] as const;

export type ToolFormInitial = {
  id?: string;
  name: string;
  slug: string;
  originalUrl: string;
  shortDescriptionDe: string;
  longDescriptionDe: string;
  featuresDe: string;
  pricingModel: PricingModel;
  licenseType: LicenseType;
  useCasesDe: string;
  beginnerFriendly: boolean;
  ossProjectUrl: string;
  ossRepoUrl: string;
  ossLicense: string;
  ossOperatingSystems: string;
  ossInstallNotes: string;
  tiktokUrl: string;
  instagramReelUrl: string;
  youtubeShortUrl: string;
  editorRating: string;
  publishStatus: PublishStatus;
  featured: boolean;
  editorialRank: string;
  isExample: boolean;
  categoryIds: string[];
  tags: string;
  internalNotes: string;
  discoverySource: string;
  logo: string | null;
  screenshots: string[];
};

const empty: ActionState = {};

export function ToolForm({
  initial,
  categories,
}: {
  initial: ToolFormInitial;
  categories: { id: string; name: string }[];
}) {
  const [state, action] = useFormState(saveToolAction, empty);
  return (
    <form action={action} className="grid gap-4" encType="multipart/form-data">
      {initial.id ? <input type="hidden" name="id" value={initial.id} /> : null}
      <input type="hidden" name="discoverySource" value={initial.discoverySource} />
      {state.error ? (
        <p role="alert" className="rounded-xl border border-red-800 bg-red-950 px-4 py-3 text-sm text-red-100">
          {state.error}
        </p>
      ) : null}
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="grid gap-1 text-sm font-medium">
          Name
          <input name="name" required defaultValue={initial.name} className="field" />
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Kurzname
          <input name="slug" defaultValue={initial.slug} className="field" placeholder="wird aus dem Namen gebildet" />
        </label>
      </div>
      <label className="grid gap-1 text-sm font-medium">
        Original-URL, nur intern
        <input name="originalUrl" type="url" required defaultValue={initial.originalUrl} className="field" />
      </label>
      <label className="grid gap-1 text-sm font-medium">
        Kurzbeschreibung
        <textarea name="shortDescriptionDe" required defaultValue={initial.shortDescriptionDe} className="area" />
      </label>
      <label className="grid gap-1 text-sm font-medium">
        Ausführliche Beschreibung
        <textarea name="longDescriptionDe" defaultValue={initial.longDescriptionDe} className="area min-h-40" />
      </label>
      <label className="grid gap-1 text-sm font-medium">
        Besondere Funktionen, eine pro Zeile
        <textarea name="featuresDe" defaultValue={initial.featuresDe} className="area" />
      </label>
      <div className="grid gap-4 sm:grid-cols-3">
        <label className="grid gap-1 text-sm font-medium">
          Preismodell
          <select name="pricingModel" defaultValue={initial.pricingModel} className="field">
            {pricingOptions.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Lizenztyp
          <select name="licenseType" defaultValue={initial.licenseType} className="field">
            {licenseOptions.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Status
          <select name="publishStatus" defaultValue={initial.publishStatus} className="field">
            {publishStatuses.map((status) => (
              <option key={status} value={status}>
                {publishLabels[status]}
              </option>
            ))}
          </select>
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Top-20-Position
          <input name="editorialRank" inputMode="numeric" defaultValue={initial.editorialRank} className="field" placeholder="1–20 oder leer" />
        </label>
      </div>
      <fieldset className="grid gap-2">
        <legend className="text-sm font-medium">Kategorien</legend>
        <div className="grid gap-2 sm:grid-cols-2">
          {categories.map((category) => (
            <label key={category.id} className="flex items-center gap-2 text-sm">
              <input type="checkbox" name="categoryIds" value={category.id} defaultChecked={initial.categoryIds.includes(category.id)} />
              {category.name}
            </label>
          ))}
        </div>
      </fieldset>
      <label className="grid gap-1 text-sm font-medium">
        Anwendungsfälle, eine pro Zeile
        <textarea name="useCasesDe" defaultValue={initial.useCasesDe} className="area" />
      </label>
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="grid gap-1 text-sm font-medium">
          Projektwebsite, nur bei Open Source
          <input name="ossProjectUrl" defaultValue={initial.ossProjectUrl} className="field" />
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Repository
          <input name="ossRepoUrl" defaultValue={initial.ossRepoUrl} className="field" />
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Lizenzname, nur wenn bekannt
          <input name="ossLicense" defaultValue={initial.ossLicense} className="field" placeholder="leer lassen, wenn unbekannt" />
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Betriebssysteme, durch Komma
          <input name="ossOperatingSystems" defaultValue={initial.ossOperatingSystems} className="field" />
        </label>
      </div>
      <label className="grid gap-1 text-sm font-medium">
        Installationshinweis
        <textarea name="ossInstallNotes" defaultValue={initial.ossInstallNotes} className="area" />
      </label>
      <div className="grid gap-4 sm:grid-cols-3">
        <label className="grid gap-1 text-sm font-medium">
          TikTok-Video
          <input name="tiktokUrl" defaultValue={initial.tiktokUrl} className="field" />
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Instagram-Reel
          <input name="instagramReelUrl" defaultValue={initial.instagramReelUrl} className="field" />
        </label>
        <label className="grid gap-1 text-sm font-medium">
          YouTube-Short
          <input name="youtubeShortUrl" defaultValue={initial.youtubeShortUrl} className="field" />
        </label>
      </div>
      <label className="grid gap-1 text-sm font-medium">
        Eigene Bewertung, 1 bis 5, nur wenn wirklich vergeben
        <input name="editorRating" defaultValue={initial.editorRating} className="field" placeholder="leer" />
      </label>
      <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" name="beginnerFriendly" defaultChecked={initial.beginnerFriendly} />
        Für Anfänger geeignet
      </label>
      <label className="grid gap-1 text-sm font-medium">
        Tags, durch Komma getrennt
        <input name="tags" defaultValue={initial.tags} className="field" />
      </label>
      <div className="flex flex-wrap gap-4 text-sm">
        <label className="flex items-center gap-2">
          <input type="checkbox" name="featured" defaultChecked={initial.featured} />
          Empfohlen
        </label>
        <label className="flex items-center gap-2">
          <input type="checkbox" name="isExample" defaultChecked={initial.isExample} />
          Als Beispiel kennzeichnen
        </label>
      </div>
      <label className="grid gap-1 text-sm font-medium">
        Logo, PNG, JPEG oder WebP
        <input name="logo" type="file" accept="image/png,image/jpeg,image/webp" className="text-sm" />
      </label>
      {initial.logo ? (
        <label className="flex items-center gap-2 text-sm">
          <input type="checkbox" name="removeLogo" />
          Logo entfernen ({initial.logo})
        </label>
      ) : null}
      <label className="grid gap-1 text-sm font-medium">
        Weitere Vorschaubilder
        <input name="screenshots" type="file" accept="image/png,image/jpeg,image/webp" multiple className="text-sm" />
      </label>
      {initial.screenshots.map((shot) => (
        <label key={shot} className="flex items-center gap-2 text-sm">
          <input type="checkbox" name="removeScreenshots" value={shot} />
          Vorschau entfernen ({shot})
        </label>
      ))}
      <label className="grid gap-1 text-sm font-medium">
        Interne Notiz
        <textarea name="internalNotes" defaultValue={initial.internalNotes} className="area" />
      </label>
      <p className="text-xs text-muted-foreground">
        Quelle: {initial.discoverySource}. Ein veröffentlichtes Tool ohne Partnerlink zeigt den Button „Zur offiziellen Website“. Mit aktivem Partnerlink heißt der Button „Jetzt Tool ausprobieren“ und ist als Werbung gekennzeichnet. Partnerlinks pflegst du unter dem Formular.
      </p>
      <button type="submit" className="h-11 rounded-xl bg-primary px-4 text-sm font-semibold text-primary-foreground">
        Speichern
      </button>
    </form>
  );
}
