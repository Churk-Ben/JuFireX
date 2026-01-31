<template>
  <div class="page-container">
    <n-space vertical size="large">
      <n-h1>{{ t("sider.menu.navigations") }}</n-h1>

      <n-spin :show="loading">
        <n-result
          v-if="Object.keys(groupedNavs).length === 0 && !loading"
          status="404"
          title="No Navigations Found"
          description="There are no navigation items to display."
        />

        <n-space vertical size="large" v-else>
          <div v-for="(navs, category) in groupedNavs" :key="category">
            <n-h3 prefix="bar" align-text>{{ category }}</n-h3>
            <n-grid
              x-gap="16"
              y-gap="16"
              cols="1 s:2 m:3 l:4 xl:5"
              responsive="screen"
            >
              <n-grid-item v-for="nav in navs" :key="nav.uuid">
                <n-card
                  hoverable
                  @click="openLink(nav.url)"
                  class="cursor-pointer"
                >
                  <template #header>
                    <n-space align="center" :wrap="false" :size="10">
                      <FontAwesomeIcon
                        :icon="getIcon(nav.icon)"
                        class="text-xl"
                      />
                      <n-ellipsis style="max-width: 100%">
                        {{ nav.title }}
                      </n-ellipsis>
                    </n-space>
                  </template>
                  <n-ellipsis
                    :line-clamp="2"
                    :tooltip="false"
                    class="description"
                  >
                    {{ nav.description || nav.url }}
                  </n-ellipsis>
                </n-card>
              </n-grid-item>
            </n-grid>
          </div>
        </n-space>
      </n-spin>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useI18n } from "vue-i18n";
import {
  NGrid,
  NGridItem,
  NCard,
  NSpin,
  NAvatar,
  NSpace,
  NH1,
  NH3,
  NEllipsis,
  NResult,
} from "naive-ui";
import { navigationService, type Navigation } from "@/services/navigation";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

const { t } = useI18n();
const loading = ref(false);
const navigations = ref<Navigation[]>([]);

const groupedNavs = computed(() => {
  const groups: Record<string, Navigation[]> = {};
  navigations.value.forEach((nav) => {
    const cat = nav.category || "Uncategorized";
    if (!groups[cat]) {
      groups[cat] = [];
    }
    groups[cat].push(nav);
  });
  return groups;
});

async function fetchNavigations() {
  loading.value = true;
  try {
    navigations.value = await navigationService.getAll(false); // public only
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

function getIcon(iconClass: string | undefined): any {
  if (!iconClass) return ["fas", "link"];

  // format: "fas:link" or "fab:github"
  if (iconClass.includes(":")) {
    const parts = iconClass.split(":");
    if (parts.length === 2) {
      return [parts[0], parts[1]];
    }
  }

  return iconClass;
}

function openLink(url: string) {
  window.open(url, "_blank");
}

onMounted(() => {
  fetchNavigations();
});
</script>

<style scoped>
.page-container {
  padding: 24px;
}
.cursor-pointer {
  cursor: pointer;
}
.nav-icon {
  background-color: transparent;
}
.description {
  height: 44px; /* Approximate height for 2 lines */
  color: var(--n-text-color-3);
}
</style>
