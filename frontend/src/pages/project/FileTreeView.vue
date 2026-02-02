<template>
  <div class="page-container">
    <n-spin :show="loading">
      <div class="header">
        <n-button text @click="goBack" class="back-button">
          <template #icon>
            <n-icon>
              <font-awesome-icon :icon="faArrowLeft" />
            </n-icon>
          </template>
          Back to Project
        </n-button>
        <n-h2 v-if="project" style="margin: 0 0 0 16px"
          >{{ project.title }} Files</n-h2
        >
      </div>

      <!-- Breadcrumbs -->
      <n-breadcrumb class="breadcrumbs">
        <n-breadcrumb-item @click="navigateTo('')">
          <span class="breadcrumb-link">Root</span>
        </n-breadcrumb-item>
        <n-breadcrumb-item
          v-for="(part, index) in pathParts"
          :key="index"
          @click="navigateToPart(index)"
        >
          <span class="breadcrumb-link">{{ part }}</span>
        </n-breadcrumb-item>
      </n-breadcrumb>

      <!-- File Content View -->
      <div v-if="currentFileContent !== null" class="file-content-view">
        <div class="file-header">
          <n-text strong>{{ currentFileName }}</n-text>
          <n-button size="small" @click="closeFile">Close File</n-button>
        </div>
        <n-card class="code-card">
          <pre><code>{{ currentFileContent }}</code></pre>
        </n-card>
      </div>

      <!-- File List View -->
      <div v-else class="file-list">
        <n-list hoverable clickable>
          <n-list-item v-if="currentPath" @click="navigateUp">
            <template #prefix>
              <n-icon><font-awesome-icon :icon="faFolder" /></n-icon>
            </template>
            ..
          </n-list-item>
          <n-list-item
            v-for="file in files"
            :key="file.name"
            @click="handleItemClick(file)"
          >
            <template #prefix>
              <n-icon>
                <font-awesome-icon
                  :icon="file.type === 'directory' ? faFolder : faFile"
                />
              </n-icon>
            </template>
            <n-space justify="space-between" style="width: 100%">
              <n-text>{{ file.name }}</n-text>
              <n-text depth="3" v-if="file.type === 'file'">{{
                formatSize(file.size)
              }}</n-text>
            </n-space>
          </n-list-item>
          <n-list-item v-if="files.length === 0">
            <n-text depth="3">Empty directory</n-text>
          </n-list-item>
        </n-list>
      </div>
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  NSpin,
  NButton,
  NIcon,
  NBreadcrumb,
  NBreadcrumbItem,
  NList,
  NListItem,
  NText,
  NSpace,
  NCard,
  NH2,
} from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faArrowLeft,
  faFolder,
  faFile,
} from "@fortawesome/free-solid-svg-icons";
import { projectService } from "@/services/project";
import type { Project, ProjectFile } from "@/types/models";

const route = useRoute();
const router = useRouter();
const loading = ref(false);
const project = ref<Project | null>(null);
const files = ref<ProjectFile[]>([]);
const currentPath = ref("");
const currentFileContent = ref<string | null>(null);
const currentFileName = ref("");

const uuid = route.params.uuid as string;

const pathParts = computed(() => {
  return currentPath.value ? currentPath.value.split("/") : [];
});

async function fetchProject() {
  try {
    project.value = await projectService.getDetail(uuid);
  } catch (e) {
    console.error(e);
  }
}

async function fetchFiles(path: string) {
  loading.value = true;
  try {
    files.value = await projectService.getFileTree(uuid, path);
    currentPath.value = path;
    currentFileContent.value = null; // Ensure we are in list mode
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

async function fetchFileContent(path: string, name: string) {
  loading.value = true;
  try {
    const content = await projectService.getFileContent(uuid, path);
    currentFileContent.value = content;
    currentFileName.value = name;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

function handleItemClick(file: ProjectFile) {
  if (file.type === "directory") {
    fetchFiles(file.path);
  } else {
    fetchFileContent(file.path, file.name);
  }
}

function navigateTo(path: string) {
  fetchFiles(path);
}

function navigateToPart(index: number) {
  const newPath = pathParts.value.slice(0, index + 1).join("/");
  fetchFiles(newPath);
}

function navigateUp() {
  if (!currentPath.value) return;
  const parts = currentPath.value.split("/");
  parts.pop();
  fetchFiles(parts.join("/"));
}

function closeFile() {
  currentFileContent.value = null;
}

function goBack() {
  router.push(`/project/${uuid}`);
}

function formatSize(bytes: number) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

onMounted(() => {
  if (uuid) {
    fetchProject();
    fetchFiles("");
  }
});
</script>

<style scoped>
.page-container {
  padding: 24px;
  max-width: 900px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.breadcrumbs {
  margin-bottom: 16px;
  font-size: 16px;
}

.breadcrumb-link {
  cursor: pointer;
}

.breadcrumb-link:hover {
  text-decoration: underline;
  color: var(--n-primary-color);
}

.file-list {
  background: white;
  border-radius: 8px;
  border: 1px solid #efeff5;
}

.file-content-view {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.file-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.code-card {
  overflow-x: auto;
}

pre {
  margin: 0;
  font-family: v-mono, SFMono-Regular, Menlo, Consolas, Courier, monospace;
  font-size: 14px;
}
</style>
