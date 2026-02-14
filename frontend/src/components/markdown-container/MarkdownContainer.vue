<!-- @author: Churk -->
<!-- @status: 完成 -->
<!-- @description: 通用Markdown容器组件，用于展示Markdown内容 -->

<template>
  <n-card class="markdown-container">
    <MarkdownRender :content="content" />
  </n-card>
</template>

<script setup lang="ts">
import { NCard } from "naive-ui";
import MarkdownRender from "./MarkdownRender";

defineProps({
  content: {
    type: String,
    default: "",
  },
});
</script>

<style scoped>
.markdown-container {
  padding: 0 32px 16px;
}
</style>
