import "dotenv/config";
import { getDb } from "./client";
import { seed } from "./seed";

async function main() {
  await getDb();
  await seed();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
