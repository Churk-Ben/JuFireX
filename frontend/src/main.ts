import { createApp } from "vue";
import { createPinia } from "pinia";
import { createI18n } from "vue-i18n";
import { messages } from "@/locales/.index";
import router from "@/router";
import "bootstrap/dist/css/bootstrap.min.css";
import "@/styles/root.css";
import "bootstrap";
import App from "../app.vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";

library.add(fas, fab);

function resolveInitialLocale(): string {
  const saved = localStorage.getItem("locale");
  if (saved) return saved;
  const nav = (navigator.language || "zh-CN").toLowerCase();
  if (nav.startsWith("zh")) return "zh-CN";
  return "en";
}

const i18n = createI18n({
  legacy: false,
  locale: resolveInitialLocale(),
  fallbackLocale: "en",
  messages,
});

const app = createApp(App)
  .use(createPinia())
  .use(router)
  .use(i18n)
  .component("fa", FontAwesomeIcon);
app.mount("#app");
