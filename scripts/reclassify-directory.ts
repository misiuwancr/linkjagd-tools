import "dotenv/config";
import fs from "fs";
import path from "path";
import { ensureDirectoryTaxonomy } from "@/lib/reclassify";

async function main() {
  const result = await ensureDirectoryTaxonomy({ force: true });
  if (!result) return;
  fs.writeFileSync(path.join(process.cwd(), "data", "category-review.json"), JSON.stringify(result.review, null, 2));
  console.log(JSON.stringify({ counts: result.counts, review: result.review.length, ranked: result.ranked }, null, 2));
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
