<template>
  <ScrollContainer>
    <n-space vertical size="large">
      <n-h1>{{ t("sider.menu.blogs") }}</n-h1>

      <n-spin :show="loading">
        <n-result
          v-if="blogs.length === 0 && !loading"
          status="404"
          title="No Articles Found"
          description="There are no blog posts to display."
        />

        <div v-else class="blog-list-container">
          <n-space vertical size="large">
            <n-card
              v-for="blog in blogs"
              :key="blog.uuid"
              hoverable
              @click="openDetail(blog.uuid)"
              class="blog-card"
            >
              <template #cover v-if="blog.cover_image">
                <img :src="blog.cover_image" class="blog-cover" />
              </template>
              <template #header>
                <n-ellipsis :tooltip="false">{{ blog.title }}</n-ellipsis>
              </template>
              <template #header-extra>
                <n-text depth="3" class="date-text">
                  {{ new Date(blog.created_at).toLocaleDateString() }}
                </n-text>
              </template>

              <n-ellipsis :line-clamp="3" class="summary" :tooltip="false">
                {{ blog.summary }}
              </n-ellipsis>

              <template #footer v-if="blog.tags && blog.tags.length">
                <n-space size="small">
                  <n-tag
                    v-for="tag in blog.tags"
                    :key="tag"
                    size="small"
                    type="info"
                    round
                    :bordered="false"
                  >
                    {{ tag }}
                  </n-tag>
                </n-space>
              </template>
            </n-card>
          </n-space>
        </div>
      </n-spin>
    </n-space>
  </ScrollContainer>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { ScrollContainer } from "@/components/scroll-container";
import {
  NCard,
  NSpin,
  NTag,
  NSpace,
  NH1,
  NResult,
  NEllipsis,
  NText,
} from "naive-ui";
import { blogService } from "@/services/blog";
import type { Blog } from "@/types/models";

const { t } = useI18n();
const router = useRouter();
const loading = ref(false);
const blogs = ref<Blog[]>([]);

async function fetchBlogs() {
  loading.value = true;
  try {
    blogs.value = await blogService.getAll(false); // public only
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

function openDetail(uuid: string) {
  router.push(`/blog/${uuid}`);
}

onMounted(() => {
  fetchBlogs();
});
</script>

<style scoped>
.blog-list-container {
  max-width: 800px;
  margin: 0 auto;
}
.blog-card {
  cursor: pointer;
}
.blog-cover {
  height: 200px;
  object-fit: cover;
  width: 100%;
  display: block;
}
.summary {
  color: var(--n-text-color-3);
}
.date-text {
  font-size: 12px;
}
</style>
