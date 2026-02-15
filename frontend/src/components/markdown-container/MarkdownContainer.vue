<!-- @author: Churk -->
<!-- @status: 完成 -->
<!-- @description: 通用Markdown容器组件，用于展示Markdown内容 -->

<template>
  <n-config-provider :hljs="hljs" :katex="katex">
    <n-card class="markdown-container">
      <MarkdownRender :content="content" :assets-base-url="assetsBaseUrl" />
    </n-card>
  </n-config-provider>
</template>

<script setup lang="ts">
import { NCard, NConfigProvider } from "naive-ui";
import MarkdownRender from "./MarkdownRender";

import katex from "katex";
import "katex/dist/katex.min.css";
import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.min.css";

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
