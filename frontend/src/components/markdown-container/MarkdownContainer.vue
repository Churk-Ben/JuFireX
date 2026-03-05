<!-- @author: Churk -->
<!-- @status: 待完成 -->
<!-- @description: 通用Markdown容器组件，用于展示Markdown内容 -->

<template>
  <div ref="containerRef" class="markdown-wrapper">
    <n-card class="markdown-container">
      <div v-if="loading || !isVisible" class="loading-container">
        <n-skeleton text :repeat="2" />
        <n-skeleton text style="width: 60%" />
        <div style="margin-top: 20px">
          <n-skeleton height="100vh" width="100%" />
        </div>
      </div>
      <MdPreview
        v-else
        :modelValue="processedContent"
        :theme="theme"
        :style="editorStyle"
        :preview-theme="previewTheme"
      />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted, watch, nextTick } from "vue";
import { MdPreview, config } from "md-editor-v3";
import { useThemeStore } from "@/stores/theme";
import { NCard, NSkeleton } from "naive-ui";

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
});

const themeStore = useThemeStore();
const containerRef = ref<HTMLElement | null>(null);
const isVisible = ref(false);
const loading = ref(false);
const processedContent = ref("");
const blobUrls = ref<string[]>([]);
let observer: IntersectionObserver | null = null;
let isUnmounted = false;

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

// 将base64转换为Blob URL以优化性能
const processContent = async (text: string) => {
  if (!text) {
    processedContent.value = "";
    return;
  }

  // 如果已经卸载，不再处理
  if (isUnmounted) return;

  loading.value = true;

  // 给UI渲染 loading 状态的机会
  await new Promise((resolve) => setTimeout(resolve, 10));

  if (isUnmounted) return;

  try {
    // 简单的替换策略，查找Markdown图片语法中的Base64
    // 匹配 ![...](data:image/...)
    const regex = /!\[([^\]]*?)\]\((data:image\/[^;]+;base64,[^)]+)\)/g;

    let newText = text;
    let match;
    const matches: {
      index: number;
      length: number;
      alt: string;
      data: string;
    }[] = [];

    regex.lastIndex = 0;

    while ((match = regex.exec(text)) !== null) {
      matches.push({
        index: match.index,
        length: match[0].length,
        alt: match[1],
        data: match[2],
      });
    }

    if (matches.length === 0) {
      processedContent.value = text;
      loading.value = false;
      return;
    }

    // 创建 Blob URL
    for (let i = matches.length - 1; i >= 0; i--) {
      if (isUnmounted) break; // 检查是否卸载

      const m = matches[i];
      try {
        const res = await fetch(m.data);
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        blobUrls.value.push(url);

        const before = newText.substring(0, m.index);
        const after = newText.substring(m.index + m.length);
        newText = before + `![${m.alt}](${url})` + after;
      } catch (e) {
        console.error("Failed to convert base64 to blob", e);
      }
    }

    if (!isUnmounted) {
      processedContent.value = newText;
    }
  } catch (err) {
    console.error("Error processing markdown content", err);
    if (!isUnmounted) {
      processedContent.value = text;
    }
  } finally {
    if (!isUnmounted) {
      loading.value = false;
    }
  }
};

const cleanupBlobUrls = () => {
  blobUrls.value.forEach((url) => URL.revokeObjectURL(url));
  blobUrls.value = [];
};

// 监听内容变化
watch(
  () => props.content,
  (newVal) => {
    cleanupBlobUrls();
    if (isVisible.value) {
      processContent(newVal);
    } else {
      processedContent.value = "";
    }
  }
);

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          isVisible.value = true;
          if (processedContent.value === "" && props.content) {
            processContent(props.content);
          }
          if (observer) observer.disconnect();
        }
      });
    },
    {
      rootMargin: "200px", // 增加预加载距离
      threshold: 0.01,
    }
  );

  if (containerRef.value) {
    observer.observe(containerRef.value);
  }
});

onUnmounted(() => {
  isUnmounted = true;
  if (observer) {
    observer.disconnect();
  }
  cleanupBlobUrls();
});
</script>

<style scoped>
.markdown-container {
  padding: 0 32px 16px;
}
</style>
