import { describe, expect, it } from "vitest";
import { previousRanks, rankMovement } from "@/lib/editorial-ranking";
describe("redaktionelle Rangänderungen", () => {
  it("zeigt ohne belegten vorherigen Rang immer einen Strich", () => {
    for (const previous of [undefined, null, "2", 0, -1, 1.5]) expect(rankMovement(1, previous)).toBe("unchanged");
    expect(previousRanks("")).toEqual({});
    expect(previousRanks('{"a":2,"b":"3","c":-1}')).toEqual({ a: 2 });
  });
  it("zeigt nur echte numerische Änderungen", () => {
    expect(rankMovement(1, 2)).toBe("up");
    expect(rankMovement(3, 2)).toBe("down");
    expect(rankMovement(2, 2)).toBe("unchanged");
    expect(rankMovement(null, 2)).toBe("unchanged");
  });
});
