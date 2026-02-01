const modules = import.meta.glob("./manifests/*.json", { eager: true });

export const themes: Record<string, any> = {};

for (const path in modules) {
  // path is like "./manifests/default.json"
  const fileName = path.split("/").pop()?.replace(".json", "");
  if (fileName) {
    themes[fileName] = (modules[path] as any).default;
  }
}
