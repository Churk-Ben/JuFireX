const modules = import.meta.glob("./manifests/*.json", { eager: true });

export const themeOverrides: Record<string, any> = {};

for (const path in modules) {
  const fileName = path.split("/").pop()?.replace(".json", "");
  if (fileName) {
    themeOverrides[fileName] = (modules[path] as any).default;
  }
}
