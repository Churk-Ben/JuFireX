<template>
  <div class="page-container">
    <n-space vertical size="large">
      <n-space justify="space-between" align="center">
        <n-h1 style="margin: 0">{{ t("sider.menu.admin.blogs") }}</n-h1>
        <n-button type="primary" @click="openModal()">Add Blog</n-button>
      </n-space>

      <n-card>
        <n-data-table
          :columns="columns"
          :data="blogs"
          :loading="loading"
          :pagination="pagination"
        />
      </n-card>

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
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, h } from "vue";
import { useI18n } from "vue-i18n";
import {
  NCard,
  NButton,
  NDataTable,
  NModal,
  NForm,
  NFormItem,
  NInput,
  NSwitch,
  useMessage,
  NTag,
  NSpace,
  NDynamicTags,
  NH1,
} from "naive-ui";
import { blogService, type Blog, type CreateBlogDto } from "@/services/blog";

const { t } = useI18n();
const message = useMessage();

const loading = ref(false);
const blogs = ref<Blog[]>([]);
const pagination = { pageSize: 10 };

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
  { title: "Title", key: "title" },
  {
    title: "Tags",
    key: "tags",
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
    render: (row: Blog) => (row.is_public ? "Yes" : "No"),
  },
  { title: "Views", key: "views" },
  {
    title: "Date",
    key: "created_at",
    render: (row: Blog) => new Date(row.created_at).toLocaleDateString(),
  },
  {
    title: "Actions",
    key: "actions",
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
    blogs.value = await blogService.getAll(true);
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
          message.success("Updated successfully");
        } else {
          await blogService.create(formModel);
          message.success("Created successfully");
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
      message.success("Deleted successfully");
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
  padding: 24px;
}
</style>
