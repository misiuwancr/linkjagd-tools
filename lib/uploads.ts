import fs from "fs/promises";
import path from "path";

const types: Record<string, { ext: string; magic: number[] }> = {
  "image/png": { ext: "png", magic: [0x89, 0x50, 0x4e, 0x47] },
  "image/jpeg": { ext: "jpg", magic: [0xff, 0xd8, 0xff] },
  "image/webp": { ext: "webp", magic: [0x52, 0x49, 0x46, 0x46] },
};

function matches(bytes: Buffer, magic: number[]) {
  return magic.every((value, index) => bytes[index] === value);
}

export async function saveImageUpload(file: File) {
  if (!(file instanceof File) || file.size === 0) return null;
  if (file.size > 2 * 1024 * 1024) {
    throw new Error("Die Datei darf höchstens 2 MB groß sein.");
  }
  const kind = types[file.type];
  if (!kind) throw new Error("Erlaubt sind PNG, JPEG und WebP.");
  const bytes = Buffer.from(await file.arrayBuffer());
  if (!matches(bytes, kind.magic)) throw new Error("Die Datei ist kein gültiges Bild.");
  if (file.type === "image/webp" && bytes.toString("ascii", 8, 12) !== "WEBP") {
    throw new Error("Die Datei ist kein gültiges WebP.");
  }
  const filename = `${crypto.randomUUID()}.${kind.ext}`;
  const dir = path.join(process.cwd(), "public", "uploads");
  await fs.mkdir(dir, { recursive: true });
  await fs.writeFile(path.join(dir, filename), bytes);
  return `/uploads/${filename}`;
}
