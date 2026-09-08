import { ref } from "vue";

export const THEMES = [
  {
    id: "original",
    name: "原版 · 森系工作台",
    description: "保留最初的浅色页面与墨绿导航。",
  },
  {
    id: "aurora",
    name: "Aurora · 紫蓝极光",
    description: "深空底色、柔和光晕与悬浮卡片，让工作流成为视觉中心。",
  },
  {
    id: "graphite",
    name: "Graphite · 黑曜终端",
    description: "石墨黑、琥珀刻度和清晰网格，像一座安静的任务控制室。",
  },
  {
    id: "glacier",
    name: "Glacier · 冰川玻璃",
    description: "冰蓝留白、半透明层次与轻盈阴影，适合长时间阅读与整理。",
  },
] as const;

export type ThemeId = (typeof THEMES)[number]["id"];

const STORAGE_KEY = "sanjiu-workbench-theme";
export const activeTheme = ref<ThemeId>("original");
export const savedTheme = ref<ThemeId>("original");

function isThemeId(value: unknown): value is ThemeId {
  return THEMES.some((theme) => theme.id === value);
}

/** Apply immediately. Preview calls never overwrite the saved preference. */
export function applyTheme(id: ThemeId, persist = true): boolean {
  if (!isThemeId(id)) return false;
  activeTheme.value = id;
  if (typeof document !== "undefined") {
    document.documentElement.dataset.theme = id;
  }
  if (!persist) return true;

  try {
    if (typeof window === "undefined") return false;
    window.localStorage.setItem(STORAGE_KEY, id);
    savedTheme.value = id;
    return true;
  } catch {
    // Storage can be unavailable; the visual preview still works.
    return false;
  }
}

/** Call once before mounting the app. A missing/invalid choice keeps the original. */
export function initializeTheme(): void {
  let initial: ThemeId = "original";
  try {
    if (typeof window !== "undefined") {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (isThemeId(stored)) initial = stored;
    }
  } catch {
    // No storage access is equivalent to no remembered preference.
  }
  savedTheme.value = initial;
  applyTheme(initial, false);
}
