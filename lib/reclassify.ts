import { createClient, type Client, type InValue } from "@libsql/client";
import { resolveAppDatabase } from "@/db/resolve";
import { buildSearchText } from "@/lib/tools/repository";
import { chooseCategory, DIRECTORY_CATEGORIES, EDITORIAL_TOP } from "@/lib/taxonomy";

const FLAG = "directory_taxonomy";
const FLAG_VALUE = "v1";
const CHUNK = 80;

type Statement = { sql: string; args: InValue[] };

async function applyWithClient(client: Client) {
  const now = Date.now();
  const setup: Statement[] = [];
  for (const [index, [name, slug, description]] of DIRECTORY_CATEGORIES.entries()) {
    setup.push({
      sql: `insert into categories (id, name, slug, description, sort_order, created_at, updated_at)
            values (?, ?, ?, ?, ?, ?, ?)
            on conflict(slug) do update set name = excluded.name, description = excluded.description, sort_order = excluded.sort_order, updated_at = excluded.updated_at`,
      args: [slug, name, slug, description, index + 1, now, now],
    });
  }
  await client.batch(setup, "write");

  const [toolResult, linkResult, tagResult] = await Promise.all([
    client.execute("select id, slug, name, short_description_de, long_description_de, publish_status, is_example from tools"),
    client.execute(
      `select tc.tool_id as tool_id, c.slug as slug
       from tool_categories tc inner join categories c on c.id = tc.category_id`,
    ),
    client.execute(
      `select tt.tool_id as tool_id, tags.name as name
       from tool_tags tt inner join tags on tags.id = tt.tag_id`,
    ),
  ]);

  const oldByTool = new Map<string, string[]>();
  for (const row of linkResult.rows) {
    const id = String(row.tool_id);
    const list = oldByTool.get(id) ?? [];
    list.push(String(row.slug));
    oldByTool.set(id, list);
  }
  const tagsByTool = new Map<string, string[]>();
  for (const row of tagResult.rows) {
    const id = String(row.tool_id);
    const list = tagsByTool.get(id) ?? [];
    list.push(String(row.name));
    tagsByTool.set(id, list);
  }

  const categoryName = new Map(DIRECTORY_CATEGORIES.map((item) => [item[1], item[0]]));
  const writes: Statement[] = [];
  const review: Array<{ slug: string; name: string; from: string[]; to: string; reason: string }> = [];
  const counts = new Map<string, number>();

  for (const row of toolResult.rows) {
    const id = String(row.id);
    const name = String(row.name);
    const short = String(row.short_description_de ?? "");
    const long = String(row.long_description_de ?? "");
    const choice = chooseCategory(oldByTool.get(id) ?? [], `${name} ${short} ${long}`);
    writes.push({ sql: "delete from tool_categories where tool_id = ?", args: [id] });
    writes.push({ sql: "insert into tool_categories (tool_id, category_id) values (?, ?)", args: [id, choice.slug] });
    writes.push({
      sql: "update tools set search_text = ? where id = ?",
      args: [
        buildSearchText({
          name,
          shortDescriptionDe: short,
          longDescriptionDe: long,
          categories: [categoryName.get(choice.slug) ?? choice.slug],
          tags: tagsByTool.get(id) ?? [],
        }),
        id,
      ],
    });
    if (String(row.publish_status) === "published" && Number(row.is_example) === 0) {
      counts.set(choice.slug, (counts.get(choice.slug) ?? 0) + 1);
    }
    if (choice.review) review.push({ slug: String(row.slug), name, from: oldByTool.get(id) ?? [], to: choice.slug, reason: choice.reason });
  }

  writes.push({ sql: "update tools set editorial_rank = null", args: [] });
  for (const item of EDITORIAL_TOP) {
    writes.push({
      sql: "update tools set editorial_rank = ? where slug = ? and publish_status = 'published' and is_example = 0",
      args: [item.rank, item.slug],
    });
  }
  const keep = DIRECTORY_CATEGORIES.map((item) => item[1]);
  writes.push({
    sql: `delete from categories where slug not in (${keep.map(() => "?").join(", ")})`,
    args: keep,
  });
  writes.push({
    sql: `insert into site_settings (key, value) values (?, ?)
          on conflict(key) do update set value = excluded.value`,
    args: [FLAG, FLAG_VALUE],
  });

  for (let offset = 0; offset < writes.length; offset += CHUNK) {
    await client.batch(writes.slice(offset, offset + CHUNK), "write");
  }

  return {
    counts: Object.fromEntries([...counts.entries()].sort((a, b) => b[1] - a[1])),
    review,
    ranked: EDITORIAL_TOP.map((item) => `${item.rank}. ${item.name}`),
  };
}

export async function ensureDirectoryTaxonomy(options: { force?: boolean } = {}) {
  const target = resolveAppDatabase();
  const client = createClient({ url: target.url, authToken: target.authToken });
  if (!options.force) {
    const flag = await client.execute({ sql: "select value from site_settings where key = ?", args: [FLAG] });
    if (String(flag.rows[0]?.value ?? "") === FLAG_VALUE) return null;
  }
  return applyWithClient(client);
}
