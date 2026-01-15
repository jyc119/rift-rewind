export type RankTier =
  | "IRON"
  | "BRONZE"
  | "SILVER"
  | "GOLD"
  | "PLATINUM"
  | "EMERALD"
  | "DIAMOND"
  | "MASTER"
  | "GRANDMASTER"
  | "CHALLENGER";

export function rankToMedalUrl(tier?: string | null, division?: string | null) {
  if (!tier) return null;

  const t = tier.toLowerCase();          // "gold"
  const d = division?.toLowerCase();     // "i", "ii", "iii", "iv"
  // If your source uses "I/II/III/IV", you might normalize here.

  // Example: if your assets are like gold_1.png, gold_2.png...
  // Map I->1, II->2, III->3, IV->4
  const divMap: Record<string, number> = { "i": 1, "ii": 2, "iii": 3, "iv": 4 };
  const n = d ? divMap[d] : undefined;

  // If you don’t have division-specific icons, ignore `n` and use `${t}.png`
  return n
    ? `https://opgg-static.akamaized.net/images/medals/${t}_${n}.png`
    : `https://opgg-static.akamaized.net/images/medals/${t}.png`;
}

export function formatRankLabel(tier?: string | null, division?: string | null, lp?: number | null) {
  if (!tier) return "Unranked";
  const div = division ? division.toUpperCase() : "";
  const lpText = typeof lp === "number" ? ` • ${lp} LP` : "";
  return `${tier.charAt(0)}${tier.slice(1).toLowerCase()} ${div}${lpText}`.trim();
}
