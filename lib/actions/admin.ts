"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { getDb } from "@/db/client";
import { assertUser } from "@/lib/auth/session";
import {
  createEditor,
  removeAffiliate,
  removeCategory,
  removeTool,
  saveAffiliateRecord,
  saveCategoryRecord,
  saveNewsRecord,
  saveToolRecord,
  setToolStatus,
} from "@/lib/tools/mutations";
import { getToolById } from "@/lib/tools/repository";
import { parseStringList } from "@/lib/utils";
import { saveImageUpload } from "@/lib/uploads";
import { licenseTypes, pricingModels, publishStatuses } from "@/db/schema";

export type ActionState = { error?: string };

function revalidatePublic(slug?: string) {
  for (const path of ["/", "/tools", "/top-20", "/neu", "/kategorien", "/blog"]) {
    revalidatePath(path);
  }
  if (slug) revalidatePath(`/tools/${slug}`);
}

function lines(value: FormDataEntryValue | null) {
  return String(value || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

function checked(formData: FormData, key: string) {
  const value = formData.get(key);
  return value === "on" || value === "true" || value === "1";
}

async function filesFrom(formData: FormData, currentScreenshots: string[]) {
  const logoFile = formData.get("logo");
  const logo = logoFile instanceof File && logoFile.size > 0 ? await saveImageUpload(logoFile) : null;
  const shots = formData.getAll("screenshots");
  const screenshots: string[] = [];
  for (const shot of shots) {
    if (shot instanceof File && shot.size > 0) {
      const saved = await saveImageUpload(shot);
      if (saved) screenshots.push(saved);
    }
  }
  return {
    logo,
    screenshots,
    removeLogo: checked(formData, "removeLogo"),
    removeScreenshots: formData.getAll("removeScreenshots").map(String).filter((item) => currentScreenshots.includes(item)),
  };
}

export async function saveToolAction(_prev: ActionState, formData: FormData): Promise<ActionState> {
  const auth = await assertUser("editor");
  if (!auth.ok) return { error: auth.error };
  const database = await getDb();
  const id = String(formData.get("id") || "");
  const current = id ? await getToolById(database, id) : null;
  if (id && !current) return { error: "Tool nicht gefunden." };
  const rankRaw = String(formData.get("editorialRank") || "").trim();
  const rank = rankRaw ? Number(rankRaw) : null;
  let uploads;
  try {
    uploads = await filesFrom(formData, current ? parseStringList(current.screenshots) : []);
  } catch (error) {
    return { error: error instanceof Error ? error.message : "Das Bild konnte nicht gespeichert werden." };
  }
  const pricing = String(formData.get("pricingModel") || "");
  const license = String(formData.get("licenseType") || "");
  const status = String(formData.get("publishStatus") || "");
  const ratingRaw = String(formData.get("editorRating") || "").trim();
  const result = await saveToolRecord(
    database,
    {
      name: formData.get("name"),
      slug: formData.get("slug") || "",
      originalUrl: formData.get("originalUrl"),
      shortDescriptionDe: formData.get("shortDescriptionDe"),
      longDescriptionDe: formData.get("longDescriptionDe") || "",
      featuresDe: lines(formData.get("featuresDe")),
      pricingModel: pricingModels.includes(pricing as (typeof pricingModels)[number]) ? pricing : "freemium",
      licenseType: licenseTypes.includes(license as (typeof licenseTypes)[number]) ? license : "unknown",
      useCasesDe: lines(formData.get("useCasesDe")),
      beginnerFriendly: checked(formData, "beginnerFriendly"),
      germanUi: ["ja", "nein", "unklar"].includes(String(formData.get("germanUi"))) ? String(formData.get("germanUi")) : "unklar",
      noSignup: ["ja", "nein", "unklar"].includes(String(formData.get("noSignup"))) ? String(formData.get("noSignup")) : "unklar",
      ossProjectUrl: String(formData.get("ossProjectUrl") || ""),
      ossRepoUrl: String(formData.get("ossRepoUrl") || ""),
      ossLicense: String(formData.get("ossLicense") || ""),
      ossOperatingSystems: String(formData.get("ossOperatingSystems") || "")
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean),
      ossInstallNotes: String(formData.get("ossInstallNotes") || ""),
      tiktokUrl: String(formData.get("tiktokUrl") || ""),
      instagramReelUrl: String(formData.get("instagramReelUrl") || ""),
      youtubeShortUrl: String(formData.get("youtubeShortUrl") || ""),
      editorRating: ratingRaw ? Number(ratingRaw) : null,
      publishStatus: publishStatuses.includes(status as (typeof publishStatuses)[number]) ? status : "draft",
      featured: checked(formData, "featured"),
      editorialRank: rank,
      isExample: checked(formData, "isExample"),
      categoryIds: formData.getAll("categoryIds").map(String),
      tags: String(formData.get("tags") || "")
        .split(",")
        .map((tag) => tag.trim())
        .filter(Boolean),
      internalNotes: formData.get("internalNotes") || "",
      discoverySource: formData.get("discoverySource") || current?.discoverySource || "manual",
    },
    current ? { id: current.id, logo: current.logo, screenshots: parseStringList(current.screenshots) } : undefined,
    uploads,
  );
  if (!result.ok) return { error: result.error };
  revalidatePublic(result.slug);
  revalidatePath("/admin");
  revalidatePath("/admin/tools");
  revalidatePath("/admin/moderation");
  redirect(`/admin/tools/${result.id}?gespeichert=1`);
}

export async function deleteToolAction(formData: FormData) {
  const auth = await assertUser("editor");
  if (!auth.ok) redirect(`/admin/tools?fehler=${encodeURIComponent(auth.error)}`);
  const database = await getDb();
  const id = String(formData.get("id") || "");
  const tool = await getToolById(database, id);
  if (tool) {
    await removeTool(database, id);
    revalidatePublic(tool.slug);
  }
  redirect("/admin/tools?gespeichert=1");
}

export async function statusAction(formData: FormData) {
  const auth = await assertUser("editor");
  if (!auth.ok) redirect(`/admin/tools?fehler=${encodeURIComponent(auth.error)}`);
  const status = String(formData.get("status") || "");
  if (!publishStatuses.includes(status as (typeof publishStatuses)[number])) {
    redirect("/admin/tools?fehler=Unbekannter%20Status");
  }
  const database = await getDb();
  const id = String(formData.get("id") || "");
  const tool = await getToolById(database, id);
  if (!tool) redirect("/admin/tools");
  await setToolStatus(database, id, status as "draft" | "published" | "archived");
  revalidatePublic(tool.slug);
  redirect(`/admin/tools/${id}?gespeichert=1`);
}

export async function saveAffiliateAction(formData: FormData) {
  const auth = await assertUser("editor");
  if (!auth.ok) redirect(`/admin?fehler=${encodeURIComponent(auth.error)}`);
  const database = await getDb();
  const toolId = String(formData.get("toolId") || "");
  const programId = String(formData.get("programId") || "") || undefined;
  const result = await saveAffiliateRecord(
    database,
    toolId,
    {
      affiliateUrl: formData.get("affiliateUrl") || "",
      programInfoUrl: formData.get("programInfoUrl") || "",
      programPresence: formData.get("programPresence") || "unknown",
      network: formData.get("network"),
      partnerProgramId: formData.get("partnerProgramId") || "",
      status: formData.get("status"),
      priority: Number(formData.get("priority") || 0),
      isActive: checked(formData, "isActive"),
      notes: formData.get("notes") || "",
    },
    programId,
  );
  const tool = await getToolById(database, toolId);
  if (tool) revalidatePublic(tool.slug);
  if (!result.ok) redirect(`/admin/tools/${toolId}?fehler=${encodeURIComponent(result.error)}`);
  redirect(`/admin/tools/${toolId}?gespeichert=1`);
}

export async function deleteAffiliateAction(formData: FormData) {
  const auth = await assertUser("editor");
  if (!auth.ok) redirect("/admin/login");
  const database = await getDb();
  const toolId = String(formData.get("toolId") || "");
  await removeAffiliate(database, String(formData.get("programId") || ""));
  const tool = await getToolById(database, toolId);
  if (tool) revalidatePublic(tool.slug);
  redirect(`/admin/tools/${toolId}?gespeichert=1`);
}

export async function saveCategoryAction(formData: FormData) {
  const auth = await assertUser("editor");
  if (!auth.ok) redirect(`/admin/kategorien?fehler=${encodeURIComponent(auth.error)}`);
  const database = await getDb();
  const result = await saveCategoryRecord(
    database,
    {
      name: formData.get("name"),
      slug: formData.get("slug") || "",
      description: formData.get("description") || "",
      sortOrder: Number(formData.get("sortOrder") || 0),
    },
    String(formData.get("id") || "") || undefined,
  );
  revalidatePublic();
  if (!result.ok) redirect(`/admin/kategorien?fehler=${encodeURIComponent(result.error)}`);
  redirect("/admin/kategorien?gespeichert=1");
}

export async function deleteCategoryAction(formData: FormData) {
  const auth = await assertUser("editor");
  if (!auth.ok) redirect("/admin/kategorien");
  const database = await getDb();
  await removeCategory(database, String(formData.get("id") || ""));
  revalidatePublic();
  redirect("/admin/kategorien?gespeichert=1");
}

export async function saveNewsAction(formData: FormData) {
  const auth = await assertUser("editor");
  if (!auth.ok) redirect(`/admin?fehler=${encodeURIComponent(auth.error)}`);
  const database = await getDb();
  const result = await saveNewsRecord(database, {
    title: formData.get("title"),
    excerpt: formData.get("excerpt"),
    body: formData.get("body") || "",
    sourceName: formData.get("sourceName") || "",
    status: formData.get("status"),
  });
  revalidatePath("/blog");
  revalidatePath("/");
  if (!result.ok) redirect(`/admin?fehler=${encodeURIComponent(result.error)}#meldungen`);
  redirect("/admin?gespeichert=1#meldungen");
}

export async function createEditorAction(formData: FormData) {
  const auth = await assertUser("admin");
  if (!auth.ok) redirect(`/admin?fehler=${encodeURIComponent(auth.error)}`);
  const database = await getDb();
  const result = await createEditor(
    database,
    String(formData.get("email") || ""),
    String(formData.get("password") || ""),
  );
  if (!result.ok) redirect(`/admin?fehler=${encodeURIComponent(result.error)}`);
  redirect("/admin?gespeichert=1");
}
