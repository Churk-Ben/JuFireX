<template>
  <div class="page-container">
    <div class="row h-100">
      <!-- 左边栏 -->
      <div class="col-md-3 h-100">
        <n-card
          embedded
          title="项目文件"
          class="h-100 flex-card"
          header-class="pb-0"
        >
          <ScrollContainer>
            <n-spin :show="loadingTree">
              <n-tree
                block-line
                show-line
                :data="treeData"
                :on-load="handleLoad"
                key-field="path"
                label-field="name"
                children-field="children"
                @update:selected-keys="handleNodeClick"
                selectable
                expand-on-click
                :node-props="nodeProps"
              />
            </n-spin>
          </ScrollContainer>
          <template #header-extra>
            <n-button type="default" @click="router.back()"> 返回 </n-button>
          </template>
        </n-card>
      </div>

      <!-- 右边栏 -->
      <div class="col-md-9 h-100">
        <n-card embedded class="h-100 flex-card" header-class="pb-2">
          <template #header>
            <n-breadcrumb>
              <n-breadcrumb-item @click="navigateToRoot">
                Root
              </n-breadcrumb-item>
              <n-breadcrumb-item
                v-for="(part, index) in breadcrumbPaths"
                :key="index"
              >
                {{ part }}
              </n-breadcrumb-item>
            </n-breadcrumb>
          </template>

          <ScrollContainer>
            <div v-if="currentFileContent !== null">
              <n-code
                :code="currentFileContent"
                :language="detectedLanguage"
                word-wrap
              />
            </div>
            <div v-else class="h-100 text-center">
              <n-empty />
            </div>
          </ScrollContainer>
        </n-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, h } from "vue";
import { useRoute } from "vue-router";
import {
  NCard,
  NButton,
  NTree,
  NBreadcrumb,
  NBreadcrumbItem,
  NCode,
  NIcon,
  NSpin,
  NEmpty,
  type TreeOption,
} from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faFolder,
  faFileAlt,
  faFileImage,
  faFileCode,
} from "@fortawesome/free-solid-svg-icons";
import {
  faPython,
  faJs,
  faHtml5,
  faCss3,
  faMarkdown,
} from "@fortawesome/free-brands-svg-icons";
import { projectService } from "@/services/project";
import type { ProjectFile } from "@/types/models";
import ScrollContainer from "@/components/scroll-container/ScrollContainer.vue";
import router from "@/router";

const route = useRoute();
const projectUuid = route.params.uuid as string;

const treeData = ref<TreeOption[]>([]);
const loadingTree = ref(false);
const currentFileContent = ref<string | null>(null);
const currentFilePath = ref<string>("");

// Language detection map
const getLanguage = (filename: string) => {
  const ext = filename.split(".").pop()?.toLowerCase();
  switch (ext) {
    case "py":
      return "python";
    case "js":
      return "javascript";
    case "ts":
      return "typescript";
    case "vue":
      return "html";
    case "html":
      return "html";
    case "css":
      return "css";
    case "json":
      return "json";
    case "md":
      return "markdown";
    case "sql":
      return "sql";
    default:
      return "text";
  }
};

const detectedLanguage = computed(() => getLanguage(currentFilePath.value));

const breadcrumbPaths = computed(() => {
  if (!currentFilePath.value) return [];
  return currentFilePath.value.split("/");
});

// Icon helper
const getIcon = (file: ProjectFile) => {
  if (file.type === "directory") return faFolder;

  const ext = file.name.split(".").pop()?.toLowerCase();
  switch (ext) {
    case "py":
      return faPython;
    case "js":
    case "ts":
      return faJs;
    case "html":
    case "vue":
      return faHtml5;
    case "css":
      return faCss3;
    case "md":
      return faMarkdown;
    case "png":
    case "jpg":
    case "jpeg":
    case "gif":
      return faFileImage;
    case "json":
    case "xml":
    case "sql":
      return faFileCode;
    default:
      return faFileAlt;
  }
};

// Transform API response to TreeOption
const mapFilesToOptions = (files: ProjectFile[]): TreeOption[] => {
  return files.map((file) => ({
    path: file.path,
    name: file.name,
    isLeaf: file.type === "file",
    prefix: () =>
      h(NIcon, null, {
        default: () => h(FontAwesomeIcon, { icon: getIcon(file) }),
      }),
  }));
};

const loadRoot = async () => {
  loadingTree.value = true;
  try {
    const files = await projectService.getFileTree(projectUuid, "");
    treeData.value = mapFilesToOptions(files);
  } catch (error) {
    console.error("Failed to load project files", error);
  } finally {
    loadingTree.value = false;
  }
};

const handleLoad = async (node: TreeOption) => {
  try {
    const path = node.path as string;
    const files = await projectService.getFileTree(projectUuid, path);
    node.children = mapFilesToOptions(files);
    return Promise.resolve();
  } catch (error) {
    console.error("Failed to load directory", error);
    return Promise.reject();
  }
};

const handleNodeClick = async (
  keys: Array<string | number>,
  options: Array<TreeOption | null>,
) => {
  if (keys.length === 0 || !options[0]) return;

  const node = options[0];
  if (node.isLeaf) {
    const path = node.path as string;
    currentFilePath.value = path;
    try {
      const content = await projectService.getFileContent(projectUuid, path);
      currentFileContent.value = content;
    } catch (error) {
      console.error("Failed to load file content", error);
    }
  }
};

const navigateToRoot = () => {
  currentFilePath.value = "";
  currentFileContent.value = null;
};

// Node props for styling if needed
const nodeProps = ({ option }: { option: TreeOption }) => {
  return {
    // Prevent default click behavior for directories if we only want expansion
    // But NTree 'expand-on-click' handles this.
    // We can add custom classes here.
  };
};

onMounted(() => {
  loadRoot();
});
</script>

<style scoped>
.page-container {
  height: calc(100vh - 48px);
}

:deep(.flex-card) {
  display: flex;
  flex-direction: column;
}

:deep(.flex-card > .n-card-header) {
  flex-shrink: 0;
}

:deep(.flex-card > .n-card__content) {
  flex: 1;
  min-height: 0;
  padding: 0 !important;
}
</style>
