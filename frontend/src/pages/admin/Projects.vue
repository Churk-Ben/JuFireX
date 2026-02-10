<template>
  <div class="page-container">
    <CommonTable
      ref="tableRef"
      :searchTitle="$t('page.admin.users.search.title')"
      :tableTitle="$t('page.admin.users.table.title')"
      :columns="columns"
      :data="projects"
      :loading="loading"
      :row-key="(row) => row.uuid"
      @search="fetchProjects"
      @reset="onReset"
      @reload="fetchProjects"
    >
      <template #toolbar>
        <n-button type="primary" @click="openModal()"> Add Project </n-button>
      </template>
      <template #search>
        <n-form ref="formRef" :model="form" inline label-placement="left">
          <n-form-item label="Title" path="title">
            <n-input
              v-model:value="form.title"
              clearable
              placeholder="Title"
            />
          </n-form-item>
          <n-form-item label="Tags" path="tags">
            <n-input
              v-model:value="form.tags"
              clearable
              placeholder="Tags"
            />
          </n-form-item>
          <n-form-item label="Public" path="is_public">
            <n-select
              v-model:value="form.is_public"
              :options="publicOptions"
              clearable
              style="width: 120px"
              placeholder="Select"
            />
          </n-form-item>
        </n-form>
      </template>
    </CommonTable>

    <!-- 项目弹窗 -->
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
        <n-form-item label="README" path="readme">
          <n-input
            v-model:value="formModel.readme"
            type="textarea"
            placeholder="README content (Markdown)"
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
  NInputNumber,
  NTag,
  NSpace,
  NDynamicTags,
  NSelect,
  NTime,
  NAvatar,
} from "naive-ui";
import { projectService } from "@/services/project";
import type { Project } from "@/types/models";
import type { CreateProjectDto } from "@/types/api";
import { CommonTable } from "@/components/common-table";

const { t } = useI18n();

const loading = ref(false);
const projects = ref<Project[]>([]);

const showModal = ref(false);
const submitting = ref(false);
const formRef = ref(null);
const isEditing = ref(false);
const currentUuid = ref("");

// 筛选表单
const form = reactive({
  title: "",
  tags: "",
  is_public: null as string | null,
});

const publicOptions = [
  { label: "Public", value: "true" },
  { label: "Private", value: "false" },
];

const onReset = () => {
  form.title = "";
  form.tags = "";
  form.is_public = null;
  fetchProjects();
};

// 弹窗模型
const formModel = reactive<CreateProjectDto>({
  title: "",
  description: "",
  readme: "",
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
  {
    title: "Icon",
    key: "icon",
    width: 60,
    render: (row: Project) =>
      row.icon
        ? h(NAvatar, { src: row.icon, size: "small" })
        : h(NAvatar, { size: "small" }, { default: () => row.title[0] }),
  },
  { title: "Title", key: "title" },
  {
    title: "URL",
    key: "url",
    render: (row: Project) =>
      row.url
        ? h(
            "a",
            { href: row.url, target: "_blank", style: "text-decoration: none" },
            "Link"
          )
        : "-",
  },
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
  { title: "Views", key: "views" },
  { title: "Stars", key: "stars" },
  {
    title: "Public",
    key: "is_public",
    render: (row: Project) => (row.is_public ? "Yes" : "No"),
  },
  { title: "Order", key: "order" },
  {
    title: "Created At",
    key: "created_at",
    render: (row: Project) =>
      row.created_at ? h(NTime, { time: new Date(row.created_at) }) : "-",
  },
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
    const allProjects = await projectService.getAll(true);
    let filtered = allProjects;

    if (form.title) {
      filtered = filtered.filter((p) =>
        p.title.toLowerCase().includes(form.title.toLowerCase())
      );
    }
    if (form.tags) {
      filtered = filtered.filter((p) =>
        p.tags.some((t) => t.toLowerCase().includes(form.tags.toLowerCase()))
      );
    }
    if (form.is_public) {
      filtered = filtered.filter(
        (p) => String(p.is_public) === form.is_public
      );
    }

    projects.value = filtered;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

async function openModal(proj?: Project) {
  if (proj) {
    isEditing.value = true;
    currentUuid.value = proj.uuid;
    modalTitle.value = "Edit Project";

    // 先用列表数据填充基本信息
    Object.assign(formModel, {
      title: proj.title,
      description: proj.description,
      readme: proj.readme || "",
      url: proj.url,
      icon: proj.icon,
      tags: [...proj.tags],
      is_public: proj.is_public,
      order: proj.order,
    });

    showModal.value = true;

    // 异步获取完整详情（主要是为了获取 readme）
    try {
      const fullProj = await projectService.getDetail(proj.uuid);
      if (fullProj) {
        Object.assign(formModel, {
          title: fullProj.title,
          description: fullProj.description,
          readme: fullProj.readme || "",
          url: fullProj.url,
          icon: fullProj.icon,
          tags: [...fullProj.tags],
          is_public: fullProj.is_public,
          order: fullProj.order,
        });
      }
    } catch (e) {
      console.error("Failed to fetch project details", e);
    }
  } else {
    isEditing.value = false;
    currentUuid.value = "";
    modalTitle.value = "Add Project";
    Object.assign(formModel, {
      title: "",
      description: "",
      readme: "",
      url: "",
      icon: "",
      tags: [],
      is_public: true,
      order: 0,
    });
    showModal.value = true;
  }
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
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
