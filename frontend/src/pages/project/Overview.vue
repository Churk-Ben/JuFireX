<template>
  <div class="page-container">
    <n-spin :show="loading">
      <div v-if="project" class="content-wrapper">
        <n-button text @click="router.push('/projects')" class="back-button">
          <template #icon>
            <n-icon>
              <font-awesome-icon :icon="faArrowLeft" />
            </n-icon>
          </template>
          Back to Projects
        </n-button>

        <n-space justify="space-between" align="center">
          <n-h1 class="project-title">{{ project.title }}</n-h1>
          <n-space>
            <n-button
              v-if="project.url"
              tag="a"
              :href="project.url"
              target="_blank"
              secondary
              type="primary"
            >
              Visit Site
            </n-button>
            <n-button secondary @click="viewFiles"> Browse Files </n-button>
          </n-space>
        </n-space>

        <n-space
          v-if="project.tags && project.tags.length"
          class="tags-container"
          style="margin-bottom: 16px"
        >
          <n-tag
            v-for="tag in project.tags"
            :key="tag"
            round
            :bordered="false"
            type="info"
          >
            {{ tag }}
          </n-tag>
        </n-space>

        <n-p v-if="project.description" class="description">
          {{ project.description }}
        </n-p>

        <n-divider />

        <n-card title="README" :bordered="false" content-style="padding: 0">
          <div class="markdown-body" v-html="renderedReadme"></div>
        </n-card>
      </div>

      <n-result
        v-else-if="!loading"
        status="404"
        title="Project not found"
        description="The project you are looking for does not exist."
        style="margin-top: 48px"
      >
        <template #footer>
          <n-button @click="router.push('/projects')">Go Back</n-button>
        </template>
      </n-result>
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  NSpin,
  NCard,
  NTag,
  NButton,
  NResult,
  NSpace,
  NH1,
  NP,
  NDivider,
  NIcon,
} from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import { projectService } from "@/services/project";
import type { Project } from "@/types/models";
import { marked } from "marked";

const route = useRoute();
const router = useRouter();
const loading = ref(false);
const project = ref<Project | null>(null);

const renderedReadme = computed(() => {
  if (!project.value?.readme) return "No README available.";
  return marked.parse(project.value.readme);
});

async function fetchDetail() {
  const uuid = route.params.uuid as string;
  if (!uuid) return;

  loading.value = true;
  try {
    project.value = await projectService.getDetail(uuid);
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

function viewFiles() {
  router.push(`/project/${project.value?.uuid}/files`);
}

onMounted(() => {
  fetchDetail();
});
</script>

<style scoped>
.page-container {
  padding: 24px;
}

.content-wrapper {
  max-width: 900px;
  margin: 0 auto;
}

.back-button {
  margin-bottom: 16px;
}

.project-title {
  margin-bottom: 8px;
}

.description {
  font-size: 16px;
  color: var(--n-text-color-2);
}

.markdown-body {
  line-height: 1.6;
  font-size: 16px;
  color: var(--n-text-color);
}
</style>
