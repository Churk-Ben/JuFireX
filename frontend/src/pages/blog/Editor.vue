<template>
  <div class="editor-container">
    <n-space>
      <n-button @click="router.back()">
        <FontAwesomeIcon icon="arrow-left" />
      </n-button>
      <n-h1>{{ title }}</n-h1>
      <n-tag
        v-for="tag in tags"
        :key="tag"
        :bordered="false"
        type="info"
        size="small"
      >
        {{ tag }}
      </n-tag>
    </n-space>
    <MdEditor
      class="editor"
      v-model="content"
      autoDetectCode
      :theme="theme"
      :style="editorStyle"
      :language="language"
      :preview-theme="previewTheme"
      :code-theme="codeTheme"
      @on-save="onSave"
      @on-upload-img="onUploadImg"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { MdEditor, config } from "md-editor-v3";

import { useI18n } from "vue-i18n";
import { NButton, NSpace, NH1, NTag } from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { useThemeStore } from "@/stores/theme";
import { blogService } from "@/services/blog";

import JP_JP from "@vavt/cm-extension/dist/locale/jp-JP";
import "md-editor-v3/lib/style.css";

const route = useRoute();
const router = useRouter();
const { locale } = useI18n();
const themeStore = useThemeStore();

const content = ref("");
const title = ref("");
const tags = ref<string[]>([]);

const theme = computed(() => {
  return themeStore.themeMode === "dark" ? "dark" : "light";
});

const editorStyle = computed(() => {
  return {
    "--md-bk-color":
      themeStore.themeMode === "dark"
        ? "rgb(24, 24, 26)"
        : "rgb(255, 255, 255)",
  };
});

const previewTheme = computed(() => {
  return "github";
});

const codeTheme = computed(() => {
  return "atom";
});

const language = computed(() => {
  switch (locale.value) {
    case "zh-CN":
      return "zh-CN";
    case "en":
      return "en-US";
    case "jp":
      return "jp-JP";
    default:
      return "en-US";
  }
});

config({
  editorConfig: {
    languageUserDefined: {
      "jp-JP": JP_JP,
    },
  },
});

const onSave = async (v: string, h: Promise<string>) => {
  const uuid = route.params.uuid as string;
  if (!uuid) return;
  await blogService.update(uuid, {
    content: v,
  });
};

const onUploadImg = async (
  files: File[],
  callback: (urls: string[]) => void
) => {
  const uuid = route.params.uuid as string;
  if (!uuid) return;

  const res = await Promise.all(
    files.map(async (file) => {
      try {
        const result = await blogService.uploadAsset(uuid, file);
        // 使用 assets:// 协议
        return blogService.getAssetUrl(uuid, result.uuid);
      } catch (err) {
        console.error(err);
        return null;
      }
    })
  );

  callback(res.filter((url): url is string => url !== null));
};

onMounted(() => {
  const uuid = route.params.uuid as string;
  if (!uuid) return;
  blogService.getDetail(uuid).then((blog) => {
    content.value = blog.content || "";
    title.value = blog.title || "Blog Editor";
    tags.value = blog.tags || [];
  });
});
</script>

<style scoped>
.editor-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.editor {
  height: 100%;
  border-radius: 8px;
}
</style>
