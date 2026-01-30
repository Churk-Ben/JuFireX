<template>
  <n-config-provider
    :date-locale="naiveDateLocale"
    :inline-theme-disabled="true"
    :locale="naiveLocale"
    :theme="naiveTheme"
  >
    <div class="app">
      <n-layout has-sider style="height: 100vh">
        <n-layout-sider
          content-style="min-height: 100%; display: flex; flex-direction: column;"
          class="app-sider"
          collapse-mode="width"
          :collapsed-width="64"
          :width="240"
          :collapsed="collapsed"
          :native-scrollbar="false"
          bordered
        >
          <div
            class="sider-content d-flex flex-column justify-content-between flex-grow-1"
          >
            <section>
              <n-menu
                :collapsed="collapsed"
                :collapsed-width="64"
                :indent="16"
                :options="menuOptions"
                :root-indent="16"
                :value="menuValue"
                class="app-menu"
                @update:value="onMenu"
              />
            </section>
            <section>
              <n-menu
                :collapsed="collapsed"
                :collapsed-width="64"
                :indent="16"
                :options="ctrlOptions"
                :root-indent="16"
                :value="ctrlValue"
                class="app-ctrl"
                @update:value="onCtrl"
              />
              <n-menu
                :collapsed="collapsed"
                :collapsed-width="64"
                :indent="16"
                :options="userOptions"
                :root-indent="16"
                :value="userValue"
                class="user-menu"
                @update:value="onUser"
              />
            </section>
          </div>
        </n-layout-sider>
        <n-layout-content class="app-content" content-style="min-height: 0;">
          <n-dialog-provider>
            <n-message-provider placement="bottom-right">
              <RouterView />
            </n-message-provider>
          </n-dialog-provider>
        </n-layout-content>
      </n-layout>
    </div>
  </n-config-provider>
</template>

<script lang="ts" setup>
import { computed, h, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { RouterView, useRoute, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import {
  darkTheme,
  dateEnUS,
  dateJaJP,
  dateZhCN,
  enUS,
  jaJP,
  zhCN,
  NConfigProvider,
  NIcon,
  NLayout,
  NLayoutContent,
  NLayoutSider,
  NMenu,
  NMessageProvider,
  NDialogProvider,
} from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faFire,
  faCompass,
  faBook,
  faBug,
  faUser,
  faCrown,
  faUserGroup,
  faCog,
  faSignOutAlt,
  faSignInAlt,
  faBars,
  faMoon,
  faSun,
  faLanguage,
  faNewspaper,
} from "@fortawesome/free-solid-svg-icons";

const { locale, t } = useI18n();
const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

function renderIcon(icon: any) {
  return () =>
    h(NIcon, { size: 16 }, { default: () => h(FontAwesomeIcon, { icon }) });
}

// 应用侧边栏折叠状态
const collapsed = ref(localStorage.getItem("collapsed") === "true");

function toggleCollapsed() {
  collapsed.value = !collapsed.value;
  localStorage.setItem("collapsed", String(collapsed.value));
}

// 应用菜单选项
const menuValue = ref(route.path);
const menuOptions = computed(() => [
  {
    label: t("sider.menu.home"),
    key: "/",
    icon: renderIcon(faFire),
  },
  {
    label: t("sider.menu.navigations"),
    key: "/navigations",
    icon: renderIcon(faCompass),
  },
  {
    label: t("sider.menu.projects"),
    key: "/projects",
    icon: renderIcon(faBook),
  },
  {
    label: t("sider.menu.blogs"),
    key: "/blogs",
    icon: renderIcon(faNewspaper),
  },
  {
    label: t("sider.menu.debug"),
    key: "/test",
    icon: renderIcon(faBug),
  },
]);

function onMenu(key: string) {
  menuValue.value = key;
  router.push(key);
}

// 应用控制选项
const ctrlValue = ref<string | null>(null);
const ctrlOptions = computed(() => [
  {
    label: collapsed.value ? t("sider.ctrl.expand") : t("sider.ctrl.collapse"),
    key: "toggleCollapsed",
    icon: renderIcon(faBars),
  },
  {
    label: themeLabel.value,
    key: "toggleTheme",
    icon: renderIcon(themeMode.value === "light" ? faMoon : faSun),
  },
  {
    label: localeLabel.value,
    key: "locale",
    icon: renderIcon(faLanguage),
    children: localeOptions.map((o) => ({
      label: o.label,
      key: `locale:${o.value}`,
    })),
  },
]);

function onCtrl(key: string | null) {
  if (!key) return;
  if (key === "toggleCollapsed") {
    toggleCollapsed();
  } else if (key === "toggleTheme") {
    toggleTheme();
  } else if (key.startsWith("locale:")) {
    onLocale(key.split(":")[1]);
  }
  ctrlValue.value = null;
}

// 应用用户选项
const userValue = ref<string | null>(null);
const userOptions = computed(() => {
  if (!userStore.currentUser) {
    return [
      {
        label: t("sider.menu.user.login"),
        key: "/login",
        icon: renderIcon(faSignInAlt),
      },
    ];
  }
  return [
    {
      label: userStore.currentUser.username || t("sider.menu.user"),
      key: "/user",
      icon: renderIcon(faUser),
      children: [
        {
          label: t("sider.menu.user.profile"),
          key: "/user/profile",
          icon: renderIcon(faUser),
        },
        {
          label: t("sider.menu.user.settings"),
          key: "/user/settings",
          icon: renderIcon(faCog),
        },
        {
          label: t("sider.menu.admin"),
          key: "/admin",
          icon: renderIcon(faCrown),
          children: [
            {
              label: t("sider.menu.admin.users"),
              key: "/admin/users",
              icon: renderIcon(faUserGroup),
            },
            {
              label: t("sider.menu.admin.navigations"),
              key: "/admin/navigations",
              icon: renderIcon(faCompass),
            },
            {
              label: t("sider.menu.admin.projects"),
              key: "/admin/projects",
              icon: renderIcon(faBook),
            },
            {
              label: t("sider.menu.admin.blogs"),
              key: "/admin/blogs",
              icon: renderIcon(faNewspaper),
            },
          ],
        },
        {
          label: t("sider.menu.user.logout"),
          key: "/user/logout",
          icon: renderIcon(faSignOutAlt),
        },
      ],
    },
  ];
});

async function onLogout() {
  await userStore.logout();
  router.push("/");
}

function onUser(key: string | null) {
  if (!key) return;
  if (key === "/user/logout") {
    onLogout();
  } else {
    router.push(key);
  }
  userValue.value = null;
}

// 应用主题模式
const prefersDark = () => {
  if (localStorage.getItem("themeMode")) {
    return localStorage.getItem("themeMode") === "dark";
  }
  return (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  );
};
const themeMode = ref<"light" | "dark">(prefersDark() ? "dark" : "light");
const naiveTheme = computed(() =>
  themeMode.value === "dark" ? darkTheme : null,
);

const themeLabel = computed(() =>
  themeMode.value === "light"
    ? t("sider.ctrl.theme.dark")
    : t("sider.ctrl.theme.light"),
);

function toggleTheme() {
  themeMode.value = themeMode.value === "light" ? "dark" : "light";
  localStorage.setItem("themeMode", themeMode.value);
}

// 应用语言选项
const localeLabel = computed(() => t("sider.ctrl.locale"));
const localeOptions = [
  { label: "中文", value: "zh-CN" },
  { label: "English", value: "en" },
  { label: "日本語", value: "jp" },
];

const naiveLocale = computed(() => {
  if (locale.value === "zh-CN") return zhCN;
  if (locale.value === "en") return enUS;
  if (locale.value === "jp") return jaJP;
  return null;
});

const naiveDateLocale = computed(() => {
  if (locale.value === "zh-CN") return dateZhCN;
  if (locale.value === "en") return dateEnUS;
  if (locale.value === "jp") return dateJaJP;
  return null;
});

function onLocale(v: string) {
  locale.value = v;
  localStorage.setItem("locale", v);
  document.documentElement.lang = v;
}

// 应用初始化
onMounted(() => {
  document.documentElement.lang = locale.value;
  collapsed.value = localStorage.getItem("collapsed") === "true";
  userStore.checkAuth();
});

watch(
  () => route.path,
  (p) => {
    menuValue.value = p;
  },
);
</script>

<style scoped>
.app {
  --padding: 24px;
}

.app-content {
  padding: var(--padding);
}
</style>
