<template>
  <div class="editor-container">
    <MdEditor
      v-model="content"
      :theme="theme"
      :language="language"
      :style="editorStyle"
      preview-theme="default"
      code-theme="atom"
      class="editor"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { MdEditor, config } from "md-editor-v3";
import "md-editor-v3/lib/style.css";
import JP_JP from "@vavt/cm-extension/dist/locale/jp-JP";
import { useI18n } from "vue-i18n";

config({
  editorConfig: {
    languageUserDefined: {
      "jp-JP": JP_JP,
    },
  },
});
import { useThemeStore } from "@/stores/theme";

import { blogService } from "@/services/blog";

const route = useRoute();
const { locale } = useI18n();
const themeStore = useThemeStore();

const content = ref("");

const theme = computed(() => {
  return themeStore.themeMode === "dark" ? "dark" : "light";
});

const editorStyle = computed(() => {
  const primaryColor =
    themeStore.currentThemeConfig?.common?.primaryColor || "#2A7BE4FF";
  return {
    "--md-color": themeStore.themeMode === "dark" ? "#e6e6e6" : "#24292e",
    "--md-bk-color": themeStore.themeMode === "dark" ? "#1a1a1a" : "#ffffff",
    // 设置主题色变量
    "--md-theme-color": primaryColor,
    // 链接颜色
    "--md-theme-link-color": primaryColor,
    // 供下方样式使用的自定义变量
    "--user-primary-color": primaryColor,
    // 覆盖悬停背景色（使用主色调的低透明度版本）
    "--md-bk-hover": `${primaryColor}1A`,
  };
});

const language = computed(() => {
  // md-editor-v3 supports 'zh-CN', 'en-US'
  // Our app uses 'zh-CN', 'en', 'jp'
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

onMounted(() => {
  const uuid = route.params.uuid as string;
  if (!uuid) return;
  blogService.getDetail(uuid).then((blog) => {
    content.value = blog.content || "";
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

/* 覆盖工具栏图标悬停颜色 */
:deep(.md-editor-toolbar-item:hover) {
  color: var(--user-primary-color);
  background-color: var(--md-bk-hover);
}

/* 覆盖菜单项激活/悬停颜色 */
:deep(.md-editor-menu-item:hover),
:deep(.md-editor-menu-item.md-editor-menu-item-active) {
  color: var(--user-primary-color);
  background-color: var(--md-bk-hover);
}

/* 覆盖链接颜色 */
:deep(.md-editor-content .md-editor-preview a),
:deep(.md-editor-preview-wrapper a) {
  color: var(--user-primary-color);
}

/* 覆盖代码块选中颜色 */
:deep(.cm-selectionBackground),
:deep(.cm-focused .cm-selectionBackground) {
  background-color: var(--user-primary-color) !important;
  opacity: 0.3;
}

/* 覆盖光标颜色 */
:deep(.cm-cursor) {
  border-left-color: var(--user-primary-color) !important;
}

/* 覆盖页脚统计信息选中颜色 */
:deep(.md-editor-footer-item:hover) {
  color: var(--user-primary-color);
}
</style>
