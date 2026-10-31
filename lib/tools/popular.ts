export const WEEKLY_POPULAR_MIN_CLICKS = 3;

export function weeklyPopularVisible(totalClicks: number) {
  return totalClicks >= WEEKLY_POPULAR_MIN_CLICKS;
}
