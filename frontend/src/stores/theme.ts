import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { themes } from "@/themes";

export const useThemeStore = defineStore("theme", () => {
  const currentTheme = ref<string>("default");

  // 获取当前主题配置
  const currentThemeConfig = computed(() => {
    return themes[currentTheme.value] || themes["default"];
  });

  // 主题模式: light | dark
  const themeMode = ref<"light" | "dark">("light");

  // 初始化主题模式
  const initThemeMode = () => {
    const saved = localStorage.getItem("themeMode");
    if (saved === "light" || saved === "dark") {
      themeMode.value = saved;
    } else {
      const prefersDark =
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches;
      themeMode.value = prefersDark ? "dark" : "light";
    }
  };

  // 切换主题模式
  const toggleThemeMode = () => {
    themeMode.value = themeMode.value === "light" ? "dark" : "light";
    localStorage.setItem("themeMode", themeMode.value);
  };

  function setTheme(theme: string) {
    currentTheme.value = theme;
  }

  // 初始化
  initThemeMode();

  return {
    currentTheme,
    currentThemeConfig,
    themeMode,
    setTheme,
    toggleThemeMode,
  };
});
