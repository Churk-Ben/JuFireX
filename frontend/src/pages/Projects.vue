<template>
  <div class="page-container">
    <n-space vertical size="large">
      <n-h1>{{ t("sider.menu.projects") }}</n-h1>

      <n-spin :show="loading">
        <n-result
          v-if="projects.length === 0 && !loading"
          status="404"
          title="No Projects Found"
          description="There are no projects to display."
        />

        <n-grid
          v-else
          x-gap="20"
          y-gap="20"
          cols="1 m:2 l:3"
          responsive="screen"
        >
          <n-grid-item v-for="project in projects" :key="project.uuid">
            <n-card hoverable class="project-card">
              <template #header>
                <n-space align="center" :wrap="false" :size="10">
                  <n-avatar
                    v-if="project.icon"
                    :src="project.icon"
                    fallback-src="/favicon.ico"
                    size="small"
                    color="transparent"
                    class="project-icon"
                  />
                  <n-ellipsis style="max-width: 100%">
                    {{ project.title }}
                  </n-ellipsis>
                </n-space>
              </template>
              <template #header-extra>
                <n-space
                  size="small"
                  v-if="project.tags && project.tags.length"
                >
                  <n-tag
                    v-for="tag in project.tags.slice(0, 2)"
                    :key="tag"
                    size="small"
                    type="info"
                    :bordered="false"
                  >
                    {{ tag }}
                  </n-tag>
                </n-space>
              </template>

              <n-ellipsis :line-clamp="3" :tooltip="false" class="description">
                {{ project.description }}
              </n-ellipsis>

              <template #action>
                <n-space justify="end">
                  <n-button
                    v-if="project.url"
                    size="small"
                    secondary
                    type="primary"
                    @click="openLink(project.url)"
                  >
                    Visit
                  </n-button>
                  <n-button v-else size="small" disabled> Details </n-button>
                </n-space>
              </template>
            </n-card>
          </n-grid-item>
        </n-grid>
      </n-spin>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import {
  NGrid,
  NGridItem,
  NCard,
  NSpin,
  NAvatar,
  NTag,
  NButton,
  NSpace,
  NH1,
  NEllipsis,
  NResult,
} from "naive-ui";
import { projectService, type Project } from "@/services/project";

const { t } = useI18n();
const loading = ref(false);
const projects = ref<Project[]>([]);

async function fetchProjects() {
  loading.value = true;
  try {
    projects.value = await projectService.getAll(false); // public only
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
  fetchProjects();
});
</script>

<style scoped>
.page-container {
  padding: 24px;
}
.project-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.project-icon {
  background-color: transparent;
}
.description {
  height: 66px; /* Approximate height for 3 lines */
  color: var(--n-text-color-3);
}
/* Ensure the card content expands to fill height so action bar is at bottom if needed */
:deep(.n-card__content) {
  flex-grow: 1;
}
</style>
