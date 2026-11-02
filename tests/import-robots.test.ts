import { expect, it } from "vitest";
import { robotsAllows } from "@/lib/import/robots";

it("beachtet nur passende Bot-Gruppen und die spezifischste Regel", () => {
  const robots = "User-agent: OtherBot\nDisallow: /\nUser-agent: *\nDisallow: /private\nAllow: /private/open\n";
  expect(robotsAllows(robots, "https://example.test/product")).toBe(true);
  expect(robotsAllows(robots, "https://example.test/private/data")).toBe(false);
  expect(robotsAllows(robots, "https://example.test/private/open/info")).toBe(true);
  expect(robotsAllows(robots, "https://example.test/product", "OtherBot")).toBe(false);
});

it("kombiniert gleich spezifische Gruppen und berücksichtigt Wildcards, Endanker und Allow-Gleichstand", () => {
  const robots = "User-agent: *\nDisallow: /\nUser-agent: LinkjagdReview\nDisallow: /*?download=1$\nDisallow: /same\nUser-agent: LinkjagdReview\nAllow: /same\n";
  expect(robotsAllows(robots, "https://example.test/product")).toBe(true);
  expect(robotsAllows(robots, "https://example.test/file?download=1")).toBe(false);
  expect(robotsAllows(robots, "https://example.test/file?download=12")).toBe(true);
  expect(robotsAllows(robots, "https://example.test/same")).toBe(true);
});
