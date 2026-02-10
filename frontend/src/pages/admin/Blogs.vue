<template>
  <div class="page-container">
    <CommonTable
      ref="tableRef"
      :searchTitle="$t('page.admin.blogs.title')"
      :tableTitle="$t('page.admin.blogs.title')"
      :columns="columns"
      :data="blogs"
      :loading="loading"
      :row-key="(row) => row.uuid"
      @search="fetchBlogs"
      @reset="onReset"
      @reload="fetchBlogs"
    >
      <template #toolbar>
        <n-button type="primary" @click="openModal()">Add Blog</n-button>
      </template>

      <template #search>
        <n-form
          ref="searchFormRef"
          :model="searchForm"
          inline
          label-placement="left"
        >
          <n-form-item label="Title" path="title">
            <n-input
              v-model:value="searchForm.title"
              clearable
              placeholder="Title"
            />
          </n-form-item>
          <n-form-item label="Author" path="author">
            <n-input
              v-model:value="searchForm.author"
              clearable
              placeholder="Author"
            />
          </n-form-item>
          <n-form-item label="Tags" path="tags">
            <n-input
              v-model:value="searchForm.tags"
              clearable
              placeholder="Tags"
            />
          </n-form-item>
          <n-form-item label="Public" path="is_public">
            <n-select
              v-model:value="searchForm.is_public"
              :options="publicOptions"
              clearable
              style="width: 120px"
              placeholder="Select"
            />
          </n-form-item>
        </n-form>
      </template>
    </CommonTable>

    <n-modal
      v-model:show="showModal"
      preset="card"
      :title="modalTitle"
      style="width: 800px"
    >
      <n-form
        ref="formRef"
        :model="formModel"
        :rules="rules"
        label-placement="left"
        label-width="100"
      >
        <n-form-item label="Title" path="title">
          <n-input v-model:value="formModel.title" placeholder="Blog Title" />
        </n-form-item>
        <n-form-item label="Summary" path="summary">
          <n-input
            v-model:value="formModel.summary"
            type="textarea"
            placeholder="Short summary"
          />
        </n-form-item>
        <n-form-item label="Content" path="content">
          <n-input
            v-model:value="formModel.content"
            type="textarea"
            placeholder="Markdown Content"
            :rows="10"
          />
        </n-form-item>
        <n-form-item label="Cover Image" path="cover_image">
          <n-input
            v-model:value="formModel.cover_image"
            placeholder="Image URL"
          />
        </n-form-item>
        <n-form-item label="Tags" path="tags">
          <n-dynamic-tags v-model:value="formModel.tags" />
        </n-form-item>
        <n-form-item label="Public" path="is_public">
          <n-switch v-model:value="formModel.is_public" />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showModal = false">Cancel</n-button>
          <n-button type="primary" :loading="submitting" @click="handleSubmit"
            >Save</n-button
          >
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, h } from "vue";
import { useI18n } from "vue-i18n";
import {
  NButton,
  NModal,
  NForm,
  NFormItem,
  NInput,
  NSwitch,
  NTag,
  NSpace,
  NDynamicTags,
  NSelect,
  NImage,
  NTime,
  NEllipsis,
} from "naive-ui";
import { CommonTable } from "@/components/common-table";
import { blogService } from "@/services/blog";
import type { Blog } from "@/types/models";
import type { CreateBlogDto } from "@/types/api";

const { t } = useI18n();

const loading = ref(false);
const blogs = ref<Blog[]>([]);

// Search Form
const searchFormRef = ref(null);
const searchForm = reactive({
  title: "",
  author: "",
  tags: "",
  is_public: null as string | null,
});

const publicOptions = [
  { label: "Public", value: "true" },
  { label: "Private", value: "false" },
];

const onReset = () => {
  searchForm.title = "";
  searchForm.author = "";
  searchForm.tags = "";
  searchForm.is_public = null;
  fetchBlogs();
};

const showModal = ref(false);
const submitting = ref(false);
const formRef = ref(null);
const isEditing = ref(false);
const currentUuid = ref("");

const formModel = reactive<CreateBlogDto>({
  title: "",
  summary: "",
  content: "",
  cover_image: "",
  tags: [],
  is_public: true,
});

const rules = {
  title: { required: true, message: "Title is required", trigger: "blur" },
};

const columns = [
  {
    title: "Cover",
    key: "cover_image",
    width: 80,
    render: (row: Blog) =>
      row.cover_image
        ? h(NImage, { src: row.cover_image, width: 50, height: 35 })
        : "-",
  },
  { title: "Title", key: "title", width: 200 },
  {
    title: "Summary",
    key: "summary",
    width: 200,
    render: (row: Blog) =>
      h(
        NEllipsis,
        { style: "max-width: 200px" },
        { default: () => row.summary || "-" },
      ),
  },
  { title: "Author", key: "author_name", width: 120 },
  {
    title: "Tags",
    key: "tags",
    width: 200,
    render: (row: Blog) => {
      return row.tags.map((tag) =>
        h(
          NTag,
          { style: { marginRight: "6px" }, size: "small" },
          { default: () => tag },
        ),
      );
    },
  },
  {
    title: "Public",
    key: "is_public",
    width: 80,
    render: (row: Blog) => (row.is_public ? "Yes" : "No"),
  },
  { title: "Views", key: "views", width: 80 },
  {
    title: "Date",
    key: "created_at",
    width: 150,
    render: (row: Blog) =>
      row.created_at ? h(NTime, { time: new Date(row.created_at) }) : "-",
  },
  {
    title: "Actions",
    key: "actions",
    fixed: "right" as const,
    width: 150,
    render(row: Blog) {
      return h(
        NSpace,
        {},
        {
          default: () => [
            h(
              NButton,
              { size: "small", onClick: () => openModal(row) },
              { default: () => "Edit" },
            ),
            h(
              NButton,
              {
                size: "small",
                type: "error",
                onClick: () => handleDelete(row),
              },
              { default: () => "Delete" },
            ),
          ],
        },
      );
    },
  },
];

const modalTitle = ref("Add Blog");

async function fetchBlogs() {
  loading.value = true;
  try {
    const allBlogs = await blogService.getAll(true);
    let filtered = allBlogs;

    if (searchForm.title) {
      filtered = filtered.filter((b) =>
        b.title.toLowerCase().includes(searchForm.title.toLowerCase()),
      );
    }
    if (searchForm.author) {
      filtered = filtered.filter((b) =>
        (b.author_name || "")
          .toLowerCase()
          .includes(searchForm.author.toLowerCase()),
      );
    }
    if (searchForm.tags) {
      filtered = filtered.filter((b) =>
        b.tags.some((t) =>
          t.toLowerCase().includes(searchForm.tags.toLowerCase()),
        ),
      );
    }
    if (searchForm.is_public) {
      filtered = filtered.filter(
        (b) => String(b.is_public) === searchForm.is_public,
      );
    }

    blogs.value = filtered;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

function openModal(blog?: Blog) {
  if (blog) {
    isEditing.value = true;
    currentUuid.value = blog.uuid;
    modalTitle.value = "Edit Blog";
    Object.assign(formModel, {
      title: blog.title,
      summary: blog.summary,
      content: blog.content,
      cover_image: blog.cover_image,
      tags: [...blog.tags],
      is_public: blog.is_public,
    });
  } else {
    isEditing.value = false;
    currentUuid.value = "";
    modalTitle.value = "Add Blog";
    Object.assign(formModel, {
      title: "",
      summary: "",
      content: "",
      cover_image: "",
      tags: [],
      is_public: true,
    });
  }
  showModal.value = true;
}

async function handleSubmit() {
  // @ts-ignore
  formRef.value?.validate(async (errors) => {
    if (!errors) {
      submitting.value = true;
      try {
        if (isEditing.value) {
          await blogService.update(currentUuid.value, formModel);
        } else {
          await blogService.create(formModel);
        }
        showModal.value = false;
        fetchBlogs();
      } catch (e) {
        console.error(e);
      } finally {
        submitting.value = false;
      }
    }
  });
}

async function handleDelete(blog: Blog) {
  if (window.confirm(`Are you sure you want to delete "${blog.title}"?`)) {
    try {
      await blogService.delete(blog.uuid);
      fetchBlogs();
    } catch (e) {
      console.error(e);
    }
  }
}

onMounted(() => {
  fetchBlogs();
});
</script>

<style scoped>
.page-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
