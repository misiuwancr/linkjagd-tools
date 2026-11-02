type Group = { agents: string[]; rules: { allow: boolean; pattern: string }[] };

/** Evaluate the applicable robots group, not restrictions addressed to unrelated bots. */
export function robotsAllows(text: string, url: string, agent = "LinkjagdReview") {
  const groups: Group[] = [];
  let group: Group = { agents: [], rules: [] };
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.split("#", 1)[0].trim();
    const colon = line.indexOf(":");
    if (colon < 0) continue;
    const key = line.slice(0, colon).trim().toLowerCase();
    const value = line.slice(colon + 1).trim();
    if (key === "user-agent") {
      if (group.rules.length) { groups.push(group); group = { agents: [], rules: [] }; }
      group.agents.push(value.toLowerCase());
    } else if ((key === "allow" || key === "disallow") && group.agents.length && value) {
      group.rules.push({ allow: key === "allow", pattern: value });
    }
  }
  groups.push(group);
  const token = agent.toLowerCase();
  const score = (g: Group) => Math.max(-1, ...g.agents.map(a => a === "*" ? 0 : a && token.includes(a) ? a.length : -1));
  const best = Math.max(-1, ...groups.map(score));
  if (best < 0) return true;
  const parsed = new URL(url);
  const path = parsed.pathname + parsed.search;
  let matchedLength = -1;
  let allowed = true;
  for (const rule of groups.filter(g => score(g) === best).flatMap(g => g.rules)) {
    const end = rule.pattern.endsWith("$");
    const pattern = end ? rule.pattern.slice(0, -1) : rule.pattern;
    const escape = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const expression = "^" + pattern.split("*").map(escape).join(".*") + (end ? "$" : "");
    if (!new RegExp(expression).test(path)) continue;
    const specificity = pattern.replaceAll("*", "").length;
    if (specificity > matchedLength || (specificity === matchedLength && rule.allow)) {
      matchedLength = specificity;
      allowed = rule.allow;
    }
  }
  return allowed;
}
