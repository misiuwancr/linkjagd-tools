export async function register() {
  if (process.env.NEXT_RUNTIME === "nodejs") {
    const { getDb } = await import("./db/client");
    const { ensureAdmin } = await import("./db/seed");
    const database = await getDb();
    await ensureAdmin(database);
    const { ensureDirectoryTaxonomy } = await import("./lib/reclassify");
    await ensureDirectoryTaxonomy();
  }
}
