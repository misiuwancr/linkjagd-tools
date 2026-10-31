import { getDb } from "@/db/client";
import { deleteCategoryAction, saveCategoryAction } from "@/lib/actions/admin";
import { Flash } from "@/components/admin/shell";
import { listCategories } from "@/lib/tools/repository";

export const dynamic = "force-dynamic";

export default async function AdminCategoriesPage({
  searchParams,
}: {
  searchParams: { gespeichert?: string; fehler?: string };
}) {
  const categories = await listCategories(await getDb());
  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight">Kategorien</h1>
      <Flash gespeichert={searchParams.gespeichert} fehler={searchParams.fehler} />
      <form action={saveCategoryAction} className="mt-4 grid gap-3 rounded-3xl border border-border bg-card p-5 sm:grid-cols-2">
        <input name="name" required placeholder="Name" className="field" />
        <input name="slug" placeholder="Kurzname, optional" className="field" />
        <input name="description" placeholder="Beschreibung" className="field sm:col-span-2" />
        <input name="sortOrder" type="number" defaultValue={categories.length + 1} className="field" />
        <button type="submit" className="h-11 rounded-xl bg-primary text-sm font-semibold text-primary-foreground">
          Kategorie anlegen
        </button>
      </form>
      <div className="mt-6 grid gap-4">
        {categories.map((category) => (
          <form key={category.id} action={saveCategoryAction} className="grid gap-3 rounded-2xl border border-border bg-card p-4">
            <input type="hidden" name="id" value={category.id} />
            <div className="grid gap-3 sm:grid-cols-2">
              <input name="name" defaultValue={category.name} className="field" />
              <input name="slug" defaultValue={category.slug} className="field" />
            </div>
            <input name="description" defaultValue={category.description ?? ""} className="field" />
            <input name="sortOrder" type="number" defaultValue={category.sortOrder} className="field" />
            <div className="flex items-center justify-between gap-3">
              <p className="text-xs text-muted-foreground">{category.toolCount} veröffentlicht</p>
              <button type="submit" className="h-10 rounded-xl bg-primary px-4 text-sm font-medium text-primary-foreground">
                Speichern
              </button>
            </div>
          </form>
        ))}
        {categories.map((category) => (
          <form key={`${category.id}-delete`} action={deleteCategoryAction}>
            <input type="hidden" name="id" value={category.id} />
            <button type="submit" className="text-sm text-red-800 underline">
              {category.name} löschen
            </button>
          </form>
        ))}
      </div>
    </div>
  );
}
