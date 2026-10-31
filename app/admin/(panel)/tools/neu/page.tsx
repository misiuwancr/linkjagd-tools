import { getDb } from "@/db/client";
import { ToolForm, type ToolFormInitial } from "@/components/admin/tool-form";
import { listCategories } from "@/lib/tools/repository";

export const dynamic = "force-dynamic";

const initial: ToolFormInitial = {
  name: "",
  slug: "",
  originalUrl: "",
  shortDescriptionDe: "",
  longDescriptionDe: "",
  featuresDe: "",
  pricingModel: "freemium",
  publishStatus: "draft",
  featured: false,
  editorialRank: "",
  isExample: false,
  categoryIds: [],
  tags: "",
  internalNotes: "",
  discoverySource: "manual",
  logo: null,
  screenshots: [],
};

export default async function NewToolPage() {
  const categories = await listCategories(await getDb());
  return (
    <div className="max-w-3xl">
      <h1 className="text-3xl font-bold tracking-tight">Neues Tool</h1>
      <p className="mt-2 text-sm text-muted-foreground">Startet als Entwurf, wenn du den Status nicht änderst.</p>
      <div className="mt-6 rounded-3xl border border-border bg-card p-5">
        <ToolForm initial={initial} categories={categories} />
      </div>
    </div>
  );
}
