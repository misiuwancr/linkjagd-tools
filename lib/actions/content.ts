"use server";

import { redirect } from "next/navigation";
import { eq } from "drizzle-orm";
import { newsPosts } from "@/db/schema";
import { getDb } from "@/db/client";
import { requireUser } from "@/lib/auth/session";
import { saveNewsRecord } from "@/lib/tools/mutations";
import { setSetting } from "@/lib/tools/repository";
import { revalidatePath } from "next/cache";

export async function saveNewsAction(formData: FormData) {
  await requireUser("editor");
  const result = await saveNewsRecord(await getDb(), {
    id: String(formData.get("id") || ""),
    title: formData.get("title"),
    slug: formData.get("slug") || "",
    excerpt: formData.get("excerpt"),
    body: formData.get("body") || "",
    sourceName: formData.get("sourceName") || "",
    coverImageUrl: formData.get("coverImageUrl") || "",
    seoTitle: formData.get("seoTitle") || "",
    seoDescription: formData.get("seoDescription") || "",
    status: formData.get("status") === "published" ? "published" : "draft",
    editorial: {
      topic: String(formData.get("topic") || "entdecken"),
      toolSlugs: String(formData.get("toolSlugs") || "").split(/[\s,]+/).filter(Boolean),
      relatedSlugs: String(formData.get("relatedSlugs") || "").split(/[\s,]+/).filter(Boolean),
    },
  });
  if (!result.ok) redirect(`/admin/blog?fehler=${encodeURIComponent(result.error)}`);
  revalidatePath("/blog", "layout");
  revalidatePath("/tools", "layout");
  revalidatePath("/");
  revalidatePath("/sitemap.xml");
  redirect("/admin/blog?gespeichert=1");
}

export async function deleteNewsAction(formData: FormData) {
  await requireUser("editor");
  const id = String(formData.get("id") || "");
  if (id) await (await getDb()).delete(newsPosts).where(eq(newsPosts.id, id));
  redirect("/admin/blog");
}

export async function saveSocialProofAction(formData: FormData) {
  await requireUser("editor");
  await setSetting(await getDb(), "social_proof", String(formData.get("socialProof") || "").trim().slice(0, 240));
  redirect("/admin/einstellungen?gespeichert=1");
}
