import type { Metadata } from "next";
import Link from "next/link";
import { getDb } from "@/db/client";
import { listCategories } from "@/lib/tools/repository";

export const revalidate = 60;

export const metadata: Metadata = {
  title: "Kategorien",
  description: "KI-Tools nach Themen geordnet: Chat, Bild, Video, Code, Arbeit und mehr.",
  alternates: { canonical: "/kategorien" },
};

export default async function CategoriesPage() {
  const categories = await listCategories(await getDb());
  return (
    <div className="page-wrap py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-copper">Themen</p>
      <h1 className="mt-3 text-4xl font-semibold tracking-tight">Kategorien</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">Die Redaktion kann Kategorien anlegen, umbenennen und löschen.</p>
      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {categories.map((category) => (
          <Link key={category.id} href={`/kategorien/${category.slug}`} className="rounded-2xl border border-border bg-white p-5 shadow-card hover:border-[#d9d0c4]">
            <h2 className="text-lg font-semibold tracking-tight">{category.name}</h2>
            <p className="mt-2 text-sm leading-6 text-muted-foreground">{category.description}</p>
            <p className="mt-4 text-sm font-medium">{category.toolCount} veröffentlicht</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
