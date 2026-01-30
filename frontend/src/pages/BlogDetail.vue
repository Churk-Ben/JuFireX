<template>
  <div class="page-container">
    <n-spin :show="loading">
      <div v-if="blog" class="content-wrapper">
        <n-button text @click="router.back()" class="back-button">
          <template #icon>
            <n-icon>
              <font-awesome-icon :icon="faArrowLeft" />
            </n-icon>
          </template>
          Back to Blogs
        </n-button>

        <n-h1 class="blog-title">{{ blog.title }}</n-h1>

        <n-space align="center" size="small" class="blog-meta">
          <n-text depth="3">By {{ blog.author_name || "Admin" }}</n-text>
          <n-divider vertical />
          <n-text depth="3">{{
            new Date(blog.created_at).toLocaleDateString()
          }}</n-text>
          <n-divider vertical />
          <n-text depth="3">{{ blog.views }} views</n-text>
        </n-space>

        <div v-if="blog.cover_image" class="cover-image-container">
          <n-image
            :src="blog.cover_image"
            object-fit="cover"
            class="cover-image"
          />
        </div>

        <n-card :bordered="false" content-style="padding: 0">
          <div class="markdown-body" v-html="renderedContent"></div>
        </n-card>

        <n-space v-if="blog.tags && blog.tags.length" class="tags-container">
          <n-tag v-for="tag in blog.tags" :key="tag" round :bordered="false">
            # {{ tag }}
          </n-tag>
        </n-space>
      </div>

      <n-result
        v-else-if="!loading"
        status="404"
        title="Article not found"
        description="The article you are looking for does not exist."
        style="margin-top: 48px"
      >
        <template #footer>
          <n-button @click="router.push('/blogs')">Go Home</n-button>
        </template>
      </n-result>
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  NSpin,
  NCard,
  NTag,
  NButton,
  NResult,
  NSpace,
  NH1,
  NText,
  NDivider,
  NImage,
  NIcon,
} from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import { blogService, type Blog } from "@/services/blog";
import { marked } from "marked";

const route = useRoute();
const router = useRouter();
const loading = ref(false);
const blog = ref<Blog | null>(null);

const renderedContent = computed(() => {
  if (!blog.value?.content) return "";
  return marked.parse(blog.value.content);
});

async function fetchDetail() {
  const uuid = route.params.uuid as string;
  if (!uuid) return;

  loading.value = true;
  try {
    blog.value = await blogService.getDetail(uuid);
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchDetail();
});
</script>

<style scoped>
.page-container {
  padding: 24px;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
}

.back-button {
  margin-bottom: 16px;
}

.blog-title {
  margin-bottom: 8px;
}

.blog-meta {
  margin-bottom: 24px;
}

.cover-image-container {
  margin-bottom: 24px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.cover-image {
  width: 100%;
  max-height: 400px;
  display: block;
}

/* Ensure markdown content has good line height */
.markdown-body {
  line-height: 1.8;
  font-size: 16px;
  color: var(--n-text-color);
}

.tags-container {
  margin-top: 32px;
}
</style>
