<!-- @author: Churk -->
<!-- @status: 待完成 -->
<!-- @description: 通用Markdown容器组件，用于展示Markdown内容 -->

<template>
  <div class="markdown-container">
    <n-markdown :content="content" />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import {} from "naive-ui";

const props = defineProps({
  content: {
    type: String,
    default: "",
  },
});
</script>
