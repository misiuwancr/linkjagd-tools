import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function slugify(input: string) {
  return input
    .trim()
    .toLowerCase()
    .replace(/ä/g, "ae")
    .replace(/ö/g, "oe")
    .replace(/ü/g, "ue")
    .replace(/ß/g, "ss")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

export function normalizeSearch(input: string) {
  return slugify(input).replace(/-/g, " ").replace(/[%_\\]/g, " ").trim().slice(0, 120);
}

export function domainFromUrl(raw: string) {
  const url = new URL(raw);
  return url.hostname.replace(/^www\./, "").toLowerCase();
}

export function parseStringList(value: string | null | undefined) {
  if (!value) return [];
  try {
    const parsed = JSON.parse(value) as unknown;
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((item): item is string => typeof item === "string" && item.trim().length > 0);
  } catch {
    return [];
  }
}

export function utcDay(date = new Date()) {
  return date.toISOString().slice(0, 10);
}

export function isSafeLocalImage(path: string) {
  return /^\/(?:uploads|examples)\/[a-zA-Z0-9._-]+$/.test(path);
}
