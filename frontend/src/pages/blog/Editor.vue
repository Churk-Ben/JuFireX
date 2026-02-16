<template>
  <div class="editor-container">
    <MdEditor
      v-model="content"
      :theme="theme"
      :language="language"
      class="editor"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { MdEditor } from "md-editor-v3";
import "md-editor-v3/lib/style.css";
import { useI18n } from "vue-i18n";
import { useThemeStore } from "@/stores/theme";

import { blogService } from "@/services/blog";

const route = useRoute();
const { locale } = useI18n();
const themeStore = useThemeStore();

const content = ref("");

const theme = computed(() => {
  return themeStore.themeMode === "dark" ? "dark" : "light";
});

const language = computed(() => {
  // md-editor-v3 supports 'zh-CN', 'en-US'
  // Our app uses 'zh-CN', 'en', 'jp'
  switch (locale.value) {
    case "zh-CN":
      return "zh-CN";
    case "en":
      return "en-US";
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
</style>
