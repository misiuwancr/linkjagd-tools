import { notFound } from "next/navigation";
import { getDb } from "@/db/client";
import { deleteAffiliateAction, deleteToolAction, saveAffiliateAction, statusAction } from "@/lib/actions/admin";
import { Flash } from "@/components/admin/shell";
import { ToolForm } from "@/components/admin/tool-form";
import { listAffiliateNetworks } from "@/lib/affiliate/registry";
import { affiliateStatusOptions, programPresenceOptions, publishLabels } from "@/lib/labels";
import { parseStringList } from "@/lib/utils";
import { getToolById, listCategories } from "@/lib/tools/repository";
import { qualityIssues } from "@/lib/quality";

export const dynamic = "force-dynamic";

export default async function EditToolPage({
  params,
  searchParams,
}: {
  params: { id: string };
  searchParams: { gespeichert?: string; fehler?: string };
}) {
  const database = await getDb();
  const [tool, categories] = await Promise.all([getToolById(database, params.id), listCategories(database)]);
  if (!tool) notFound();
  const networks = listAffiliateNetworks();
  return (
    <div className="grid gap-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">{tool.name}</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          {publishLabels[tool.publishStatus]} · {tool.slug}
        </p>
      </div>
      <Flash gespeichert={searchParams.gespeichert} fehler={searchParams.fehler} />
      <div className="rounded-3xl border border-border bg-card p-5">
        <ToolForm
          categories={categories}
          initial={{
            id: tool.id,
            linkjagdVideos: tool.editorial.videos,
            publishedAt: tool.editorial.publishedAt,
            name: tool.name,
            slug: tool.slug,
            originalUrl: tool.originalUrl,
            shortDescriptionDe: tool.shortDescriptionDe,
            longDescriptionDe: tool.longDescriptionDe,
            featuresDe: parseStringList(tool.featuresDe).join("\n"),
            pricingModel: tool.pricingModel,
            licenseType: tool.licenseType,
            useCasesDe: parseStringList(tool.useCasesDe).join("\n"),
            beginnerFriendly: tool.beginnerFriendly,
            germanUi: tool.germanUi,
            noSignup: tool.noSignup,
            ossProjectUrl: tool.ossProjectUrl ?? "",
            ossRepoUrl: tool.ossRepoUrl ?? "",
            ossLicense: tool.ossLicense ?? "",
            ossOperatingSystems: parseStringList(tool.ossOperatingSystems).join(", "),
            ossInstallNotes: tool.ossInstallNotes ?? "",
            tiktokUrl: tool.tiktokUrl ?? "",
            instagramReelUrl: tool.instagramReelUrl ?? "",
            youtubeShortUrl: tool.youtubeShortUrl ?? "",
            editorRating: tool.editorRating ? String(tool.editorRating) : "",
            publishStatus: tool.publishStatus,
            featured: tool.featured,
            editorialRank: tool.editorialRank ? String(tool.editorialRank) : "",
            isExample: tool.isExample,
            categoryIds: categories.filter((category) => tool.categories.some((item) => item.slug === category.slug)).map((category) => category.id),
            tags: tool.tags.map((tag) => tag.name).join(", "),
            internalNotes: tool.internalNotes ?? "",
            discoverySource: tool.discoverySource,
            allowIndex: tool.allowIndex,
            qualityNotes: qualityIssues({
              name: tool.name,
              shortDescriptionDe: tool.shortDescriptionDe,
              originalUrl: tool.originalUrl,
              pricingModel: tool.pricingModel,
              categoryCount: tool.categories.length,
              publishStatus: tool.publishStatus,
            }),
            logo: tool.logo,
            screenshots: parseStringList(tool.screenshots),
          }}
        />
      </div>

      <section className="rounded-3xl border border-border bg-card p-5">
        <h2 className="text-xl font-bold">Partnerprogramme</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Der öffentliche Button bleibt /go und die Adresse der Detailseite ändert sich nicht. Liegt ein aktiver Partnerlink vor, geht die Weiterleitung dorthin und wird als Werbung gekennzeichnet. Sonst geht sie zur offiziellen Website, ohne Partnerkennzeichnung. Die Originaladresse wird nicht als Partnerlink gespeichert.
        </p>
        <div className="mt-4 grid gap-4">
          {tool.programs.map((program) => (
            <form key={program.id} action={saveAffiliateAction} className="grid gap-3 rounded-2xl border border-border p-4">
              <input type="hidden" name="toolId" value={tool.id} />
              <input type="hidden" name="programId" value={program.id} />
              <div className="grid gap-3 sm:grid-cols-2">
                <label className="grid gap-1 text-sm font-medium">
                  Partnerprogramm vorhanden
                  <select name="programPresence" defaultValue={program.programPresence} className="field">
                    {programPresenceOptions.map((item) => (
                      <option key={item.value} value={item.value}>
                        {item.label}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="grid gap-1 text-sm font-medium sm:col-span-2">
                  Programmseite, nur intern, keine Weiterleitung
                  <input name="programInfoUrl" type="url" defaultValue={program.programInfoUrl ?? ""} className="field" placeholder="Öffentliche Anmelde- oder Infoseite" />
                </label>
                <label className="grid gap-1 text-sm font-medium">
                  Affiliate-URL, nur der eigene Link
                  <input name="affiliateUrl" defaultValue={program.affiliateUrl ?? ""} className="field" />
                </label>
                <label className="grid gap-1 text-sm font-medium">
                  Netzwerk
                  <select name="network" defaultValue={program.network} className="field">
                    {networks.map((network) => (
                      <option key={network.id} value={network.id}>
                        {network.label}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="grid gap-1 text-sm font-medium">
                  Programm-ID
                  <input name="partnerProgramId" defaultValue={program.partnerProgramId ?? ""} className="field" />
                </label>
                <label className="grid gap-1 text-sm font-medium">
                  Status
                  <select name="status" defaultValue={program.status} className="field">
                    {affiliateStatusOptions.map((item) => (
                      <option key={item.value} value={item.value}>
                        {item.label}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="grid gap-1 text-sm font-medium">
                  Priorität
                  <input name="priority" type="number" defaultValue={program.priority} className="field" />
                </label>
                <label className="mt-6 flex items-center gap-2 text-sm">
                  <input type="checkbox" name="isActive" defaultChecked={program.isActive} />
                  Aktiver öffentlicher Link
                </label>
              </div>
              <textarea name="notes" defaultValue={program.notes ?? ""} className="area" placeholder="Notiz" />
              <div className="flex flex-wrap gap-2">
                <button type="submit" className="h-10 rounded-xl bg-primary px-4 text-sm font-medium text-primary-foreground">
                  Programm speichern
                </button>
              </div>
              <p className="text-xs text-muted-foreground">{networks.find((network) => network.id === program.network)?.describe().termsNote}</p>
            </form>
          ))}
          {tool.programs.map((program) => (
            <form key={`${program.id}-delete`} action={deleteAffiliateAction}>
              <input type="hidden" name="toolId" value={tool.id} />
              <input type="hidden" name="programId" value={program.id} />
              <button type="submit" className="text-sm text-red-800 underline">
                Programm {program.network} löschen
              </button>
            </form>
          ))}
        </div>
        <form action={saveAffiliateAction} className="mt-6 grid gap-3 border-t border-border pt-6">
          <h3 className="font-medium">Programm hinzufügen</h3>
          <input type="hidden" name="toolId" value={tool.id} />
          <select name="programPresence" className="field" defaultValue="unknown">
            {programPresenceOptions.map((item) => (
              <option key={item.value} value={item.value}>
                Partnerprogramm: {item.label}
              </option>
            ))}
          </select>
          <input name="programInfoUrl" type="url" placeholder="Programmseite, nur intern" className="field" />
          <input name="affiliateUrl" placeholder="Eigener Affiliate-Link, falls schon vorhanden" className="field" />
          <div className="grid gap-3 sm:grid-cols-2">
            <select name="network" className="field" defaultValue="manual">
              {networks.map((network) => (
                <option key={network.id} value={network.id}>
                  {network.label}
                </option>
              ))}
            </select>
            <select name="status" className="field" defaultValue="none_found">
              {affiliateStatusOptions.map((item) => (
                <option key={item.value} value={item.value}>
                  {item.label}
                </option>
              ))}
            </select>
          </div>
          <input name="partnerProgramId" placeholder="Programm-ID" className="field" />
          <input name="priority" type="number" defaultValue={0} className="field" />
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" name="isActive" />
            Als aktiven Link setzen
          </label>
          <textarea name="notes" className="area" placeholder="Notiz" />
          <button type="submit" className="h-11 rounded-xl border border-border text-sm font-semibold">
            Programm anlegen
          </button>
        </form>
      </section>

      <section className="flex flex-wrap gap-3">
        {(["draft", "published", "archived"] as const).map((status) => (
          <form key={status} action={statusAction}>
            <input type="hidden" name="id" value={tool.id} />
            <input type="hidden" name="status" value={status} />
            <button type="submit" className="h-10 rounded-full border border-border bg-card px-4 text-sm">
              {publishLabels[status]}
            </button>
          </form>
        ))}
        <form action={deleteToolAction}>
          <input type="hidden" name="id" value={tool.id} />
          <button type="submit" className="h-10 rounded-full px-4 text-sm text-red-800">
            Löschen
          </button>
        </form>
      </section>
    </div>
  );
}
