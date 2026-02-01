import { defineStore } from "pinia";
import { ref } from "vue";

export const useThemeStore = defineStore("theme", () => {
  const currentTheme = ref<string>("native");

  function setTheme(theme: string) {
    currentTheme.value = theme;
  }

  return {
    currentTheme,
    setTheme,
  };
});
