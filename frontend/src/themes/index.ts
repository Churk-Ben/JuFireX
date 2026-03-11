import type { GlobalThemeOverrides } from "naive-ui";

const modules = import.meta.glob("./manifests/*.json", { eager: true });

export const themes: Record<string, GlobalThemeOverrides> = {};
export const themeOptions: { label: string; value: string }[] = [];

for (const path in modules) {
  // "./manifests/*.json"
  const fileName = path.split("/").pop()?.replace(".json", "");
  if (fileName) {
    themes[fileName] = (modules[path] as any).default;
    themeOptions.push({ label: fileName, value: fileName });
  }
}
