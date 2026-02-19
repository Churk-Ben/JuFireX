<!-- @author: Churk -->
<!-- @status: 完成 -->
<!-- @description: 通用Markdown容器组件，用于展示Markdown内容 -->

<template>
  <n-card class="markdown-container">
    <MdPreview :modelValue="content" :theme="theme" :language="language" />
  </n-card>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { MdPreview } from "md-editor-v3";
import "md-editor-v3/lib/preview.css";
import { useThemeStore } from "@/stores/theme";
import { useI18n } from "vue-i18n";
import { NCard } from "naive-ui";

const props = defineProps({
  content: {
    type: String,
    default: "",
  },
});

const themeStore = useThemeStore();
const { locale } = useI18n();

const theme = computed(() => {
  return themeStore.themeMode === "dark" ? "dark" : "light";
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
</script>

<style scoped>
.markdown-container {
  padding: 0 32px 16px;
}
</style>
