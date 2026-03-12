<!-- @author: Churk -->
<!-- @status: 完工 -->
<!-- @description: Navigations 导航页 -->

<template>
  <ScrollContainer>
    <n-space vertical size="large">
      <n-h1>{{ $t("page.navigations.title") }}</n-h1>

      <n-spin :show="loading">
        <n-result
          v-if="Object.keys(groupedNavs).length === 0 && !loading"
          status="404"
          style="margin-top: 25vh"
          :title="$t('page.navigations.noResult.title')"
          :description="$t('page.navigations.noResult.description')"
        />

        <n-space v-else vertical size="large">
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
                  style="cursor: pointer"
                >
                  <template #header>
                    <n-space :wrap="false" :size="10">
                      <FontAwesomeIcon
                        :icon="navigationService.getIcon(nav.icon)"
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
                    style="height: 4em"
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
  </ScrollContainer>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import {
  NGrid,
  NGridItem,
  NCard,
  NSpin,
  NSpace,
  NH1,
  NH3,
  NEllipsis,
  NResult,
} from "naive-ui";
import type { Navigation } from "@/types/models";
import { navigationService } from "@/services/navigation";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { ScrollContainer } from "@/components/scroll-container";

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
    navigations.value = await navigationService.getAll(false);
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

function openLink(url: string) {
  window.open(url, "_blank");
}

onMounted(() => {
  fetchNavigations();
});
</script>
