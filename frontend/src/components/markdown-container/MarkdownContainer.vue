<!-- @author: Churk -->
<!-- @status: 待完成 -->
<!-- @description: 通用Markdown容器组件，用于展示Markdown内容 -->

<template>
  <n-card class="markdown-container">
    <MdPreview :modelValue="content" :theme="theme" :style="editorStyle" :preview-theme="previewTheme" />
  </n-card>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { MdPreview, config } from "md-editor-v3";
import { useThemeStore } from "@/stores/theme";
import { NCard } from "naive-ui";

import "md-editor-v3/lib/preview.css";
// @ts-ignore
import markdownItImageLazysizes from "markdown-it-image-lazysizes";
import "lazysizes";

config({
  markdownItConfig(md) {
    md.use(markdownItImageLazysizes);
  },
});

const props = defineProps({
  content: {
    type: String,
    default: "",
  },
  blogId: {
    type: String,
    default: "",
  },
});

const themeStore = useThemeStore();
const previewTheme = computed(() => {
  return "github";
});

const editorStyle = computed(() => {
  return {
    "--md-bk-color": "rgba(0, 0, 0, 0)",
  };
});

const theme = computed(() => {
  return themeStore.themeMode === "dark" ? "dark" : "light";
});
</script>

<style scoped>
.markdown-container {
  padding: 0 32px 16px;
}
</style>
