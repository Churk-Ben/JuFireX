import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";
import path from "path";

export default defineConfig({
  plugins: [vue(), vueJsx()],
  root: path.resolve(__dirname),
  build: {
    outDir: path.resolve(__dirname, "static"),
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules")) {
            const normalizedId = id.replace(/\\/g, "/");

            // Specific libraries first to prevent accidental capture by generic rules
            if (normalizedId.includes("/naive-ui/")) {
              return "naive-ui";
            }
            if (normalizedId.includes("/bootstrap/")) {
              return "bootstrap";
            }
            if (normalizedId.includes("/md-editor-v3/")) {
              return "md-editor-v3";
            }

            if (
              normalizedId.includes("/vue/") ||
              normalizedId.includes("/vue-router/") ||
              normalizedId.includes("/pinia/") ||
              normalizedId.includes("/vue-i18n/")
            ) {
              return "vue-vendor";
            }

            if (
              normalizedId.includes("/@codemirror/") ||
              normalizedId.includes("/@lezer/") ||
              normalizedId.includes("/codemirror/")
            ) {
              if (normalizedId.includes("/lang-")) {
                return "codemirror-lang";
              }
              return "codemirror";
            }
            if (normalizedId.includes("/mermaid/")) {
              return "mermaid";
            }
            if (normalizedId.includes("/highlight.js/")) {
              return "highlight.js";
            }
            if (normalizedId.includes("/katex/")) {
              return "katex";
            }
            if (
              normalizedId.includes("/marked/") ||
              normalizedId.includes("/marked-")
            ) {
              return "marked";
            }

            if (normalizedId.includes("/@fortawesome/")) {
              if (normalizedId.includes("free-solid-svg-icons")) {
                return "fontawesome-solid";
              }
              if (normalizedId.includes("free-brands-svg-icons")) {
                return "fontawesome-brands";
              }
              if (normalizedId.includes("free-regular-svg-icons")) {
                return "fontawesome-regular";
              }
              return "fontawesome-core";
            }

            if (normalizedId.includes("/dompurify/")) {
              return "dompurify";
            }
            if (normalizedId.includes("/cropperjs/")) {
              return "cropperjs";
            }

            return "vendor";
          }
        },
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
});
