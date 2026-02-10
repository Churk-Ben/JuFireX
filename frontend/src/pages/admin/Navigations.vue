<template>
  <div class="page-container">
    <CommonTable
      ref="tableRef"
      :searchTitle="$t('page.admin.navigations.title')"
      :tableTitle="$t('page.admin.navigations.title')"
      :columns="columns"
      :data="navigations"
      :loading="loading"
      :row-key="(row) => row.uuid"
      @search="fetchNavigations"
      @reset="onReset"
      @reload="fetchNavigations"
    >
      <template #toolbar>
        <n-button type="primary" @click="openModal()">
          Add Navigation
        </n-button>
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
          <n-form-item label="Category" path="category">
            <n-input
              v-model:value="searchForm.category"
              clearable
              placeholder="Category"
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

    <!-- 模态框 -->
    <n-modal
      v-model:show="showModal"
      preset="card"
      :title="modalTitle"
      style="width: 600px"
    >
      <n-form
        ref="formRef"
        :model="formModel"
        :rules="rules"
        label-placement="left"
        label-width="100"
      >
        <n-form-item label="Title" path="title">
          <n-input v-model:value="formModel.title" placeholder="Title" />
        </n-form-item>
        <n-form-item label="URL" path="url">
          <n-input v-model:value="formModel.url" placeholder="https://..." />
        </n-form-item>
        <n-form-item label="Icon" path="icon">
          <n-input
            v-model:value="formModel.icon"
            placeholder="Icon URL or Class"
          />
        </n-form-item>
        <n-form-item label="Category" path="category">
          <n-input v-model:value="formModel.category" placeholder="Category" />
        </n-form-item>
        <n-form-item label="Description" path="description">
          <n-input
            v-model:value="formModel.description"
            type="textarea"
            placeholder="Description"
          />
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

import type { Navigation } from "@/types/models";
import type { CreateNavigationDto } from "@/types/api";
import { navigationService } from "@/services/navigation";
import { CommonTable } from "@/components/common-table";

import type { DataTableColumns } from "naive-ui";
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
  NSelect,
  NAvatar,
  NTime,
  NEllipsis,
} from "naive-ui";

const { t } = useI18n();

const loading = ref(false);
const navigations = ref<Navigation[]>([]);

// 表格信息
const columns: DataTableColumns<Navigation> = [
  {
    title: "Icon",
    key: "icon",
    width: 60,
    render: (row: Navigation) =>
      row.icon
        ? h(NAvatar, { src: row.icon, size: "small" })
        : h(NAvatar, { size: "small" }, { default: () => row.title[0] }),
  },
  { title: "Title", key: "title", width: 150 },
  {
    title: "Description",
    key: "description",
    width: 200,
    render: (row: Navigation) =>
      h(
        NEllipsis,
        { style: "max-width: 200px" },
        { default: () => row.description || "-" },
      ),
  },
  {
    title: "URL",
    key: "url",
    width: 200,
    render: (row: Navigation) =>
      h(
        "a",
        {
          href: row.url,
          target: "_blank",
          style: "text-decoration: none; color: inherit;",
        },
        row.url,
      ),
  },
  {
    title: "Category",
    key: "category",
    width: 120,
    render: (row: Navigation) =>
      h(NTag, { type: "info" }, { default: () => row.category }),
  },
  {
    title: "Public",
    key: "is_public",
    width: 80,
    render: (row: Navigation) => (row.is_public ? "Yes" : "No"),
  },
  { title: "Order", key: "order", width: 80 },
  {
    title: "Created At",
    key: "created_at",
    width: 150,
    render: (row: Navigation) =>
      row.created_at ? h(NTime, { time: new Date(row.created_at) }) : "-",
  },
  {
    title: "Actions",
    key: "actions",
    fixed: "right" as const,
    width: 150,
    render(row: Navigation) {
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

// 筛选表单
const searchForm = reactive({
  title: "",
  category: "",
  is_public: null as string | null,
});

const publicOptions = [
  { label: "Public", value: "true" },
  { label: "Private", value: "false" },
];

const onReset = () => {
  searchForm.title = "";
  searchForm.category = "";
  searchForm.is_public = null;
  fetchNavigations();
};

// 数据加载函数
const fetchNavigations = async () => {
  loading.value = true;
  try {
    const allNavs = await navigationService.getAll(true);
    let filtered = allNavs;

    if (searchForm.title) {
      filtered = filtered.filter((n) =>
        n.title.toLowerCase().includes(searchForm.title.toLowerCase()),
      );
    }

    if (searchForm.category) {
      filtered = filtered.filter((n) =>
        n.category!.toLowerCase().includes(searchForm.category.toLowerCase()),
      );
    }

    if (searchForm.is_public) {
      filtered = filtered.filter(
        (n) => String(n.is_public) === searchForm.is_public,
      );
    }

    navigations.value = filtered;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

// 模态框
const modalTitle = ref("Add Navigation");
const showModal = ref(false);
const submitting = ref(false);
const formRef = ref(null);
const isEditing = ref(false);
const currentUuid = ref("");

const formModel = reactive<CreateNavigationDto>({
  title: "",
  url: "",
  icon: "",
  description: "",
  category: "default",
  is_public: true,
  order: 0,
});

const rules = {
  title: { required: true, message: "Title is required", trigger: "blur" },
  url: { required: true, message: "URL is required", trigger: "blur" },
};

async function openModal(nav?: Navigation) {
  if (nav) {
    isEditing.value = true;
    currentUuid.value = nav.uuid;
    modalTitle.value = "Edit Navigation";
    Object.assign(formModel, {
      title: nav.title,
      url: nav.url,
      icon: nav.icon,
      description: nav.description,
      category: nav.category,
      is_public: nav.is_public,
      order: nav.order,
    });
  } else {
    isEditing.value = false;
    currentUuid.value = "";
    modalTitle.value = "Add Navigation";
    Object.assign(formModel, {
      title: "",
      url: "",
      icon: "",
      description: "",
      category: "default",
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
          await navigationService.update(currentUuid.value, formModel);
        } else {
          await navigationService.create(formModel);
        }
        showModal.value = false;
        fetchNavigations();
      } catch (e) {
        console.error(e);
      } finally {
        submitting.value = false;
      }
    }
  });
}

async function handleDelete(nav: Navigation) {
  if (window.confirm(`Are you sure you want to delete "${nav.title}"?`)) {
    try {
      await navigationService.delete(nav.uuid);
      fetchNavigations();
    } catch (e) {
      console.error(e);
    }
  }
}

onMounted(() => {
  fetchNavigations();
});
</script>

<style scoped>
.page-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
