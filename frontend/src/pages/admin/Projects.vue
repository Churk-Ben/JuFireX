<template>
  <div class="page-container">
    <n-space vertical size="large">
      <n-space justify="space-between" align="center">
        <n-h1 style="margin: 0">{{ t("sider.menu.admin.projects") }}</n-h1>
        <n-button type="primary" @click="openModal()"> Add Project </n-button>
      </n-space>

      <n-card>
        <n-data-table
          :columns="columns"
          :data="projects"
          :loading="loading"
          :pagination="pagination"
        />
      </n-card>

      <n-modal
        v-model:show="showModal"
        preset="card"
        :title="modalTitle"
        style="width: 700px"
      >
        <n-form
          ref="formRef"
          :model="formModel"
          :rules="rules"
          label-placement="left"
          label-width="100"
        >
          <n-form-item label="Title" path="title">
            <n-input
              v-model:value="formModel.title"
              placeholder="Project Title"
            />
          </n-form-item>
          <n-form-item label="Description" path="description">
            <n-input
              v-model:value="formModel.description"
              type="textarea"
              placeholder="Short description"
            />
          </n-form-item>
          <n-form-item label="Content" path="content">
            <n-input
              v-model:value="formModel.content"
              type="textarea"
              placeholder="Detailed content (Markdown)"
              :rows="5"
            />
          </n-form-item>
          <n-form-item label="URL" path="url">
            <n-input
              v-model:value="formModel.url"
              placeholder="Project Link / Demo"
            />
          </n-form-item>
          <n-form-item label="Icon" path="icon">
            <n-input v-model:value="formModel.icon" placeholder="Icon URL" />
          </n-form-item>
          <n-form-item label="Tags" path="tags">
            <n-dynamic-tags v-model:value="formModel.tags" />
          </n-form-item>
          <n-form-item label="Public" path="is_public">
            <n-switch v-model:value="formModel.is_public" />
          </n-form-item>
          <n-form-item label="Order" path="order">
            <n-input-number v-model:value="formModel.order" />
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
  NInputNumber,
  NTag,
  NSpace,
  NDynamicTags,
  NH1,
} from "naive-ui";
import { projectService } from "@/services/project";
import type { Project } from "@/types/models";
import type { CreateProjectDto } from "@/types/api";

const { t } = useI18n();

const loading = ref(false);
const projects = ref<Project[]>([]);
const pagination = { pageSize: 10 };

const showModal = ref(false);
const submitting = ref(false);
const formRef = ref(null);
const isEditing = ref(false);
const currentUuid = ref("");

const formModel = reactive<CreateProjectDto>({
  title: "",
  description: "",
  content: "",
  url: "",
  icon: "",
  tags: [],
  is_public: true,
  order: 0,
});

const rules = {
  title: { required: true, message: "Title is required", trigger: "blur" },
};

const columns = [
  { title: "Title", key: "title" },
  {
    title: "Tags",
    key: "tags",
    render: (row: Project) => {
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
    render: (row: Project) => (row.is_public ? "Yes" : "No"),
  },
  { title: "Order", key: "order" },
  {
    title: "Actions",
    key: "actions",
    render(row: Project) {
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

const modalTitle = ref("Add Project");

async function fetchProjects() {
  loading.value = true;
  try {
    projects.value = await projectService.getAll(true);
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

function openModal(proj?: Project) {
  if (proj) {
    isEditing.value = true;
    currentUuid.value = proj.uuid;
    modalTitle.value = "Edit Project";
    Object.assign(formModel, {
      title: proj.title,
      description: proj.description,
      content: proj.readme || "",
      url: proj.url,
      icon: proj.icon,
      tags: [...proj.tags],
      is_public: proj.is_public,
      order: proj.order,
    });
  } else {
    isEditing.value = false;
    currentUuid.value = "";
    modalTitle.value = "Add Project";
    Object.assign(formModel, {
      title: "",
      description: "",
      content: "",
      url: "",
      icon: "",
      tags: [],
      is_public: true,
      order: 0,
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
          await projectService.update(currentUuid.value, formModel);
        } else {
          await projectService.create(formModel);
        }
        showModal.value = false;
        fetchProjects();
      } catch (e) {
        console.error(e);
      } finally {
        submitting.value = false;
      }
    }
  });
}

async function handleDelete(proj: Project) {
  if (window.confirm(`Are you sure you want to delete "${proj.title}"?`)) {
    try {
      await projectService.delete(proj.uuid);
      fetchProjects();
    } catch (e) {
      console.error(e);
    }
  }
}

onMounted(() => {
  fetchProjects();
});
</script>

<style scoped>
.page-container {
  padding: 24px;
}
</style>
