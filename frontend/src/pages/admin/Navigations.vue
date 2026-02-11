<template>
  <div class="page-container">
    <CommonTable
      ref="tableRef"
      :searchTitle="$t('page.admin.navigations.search.title')"
      :tableTitle="$t('page.admin.navigations.table.title')"
      :columns="columns"
      :data="navigations"
      :loading="loading"
      :row-key="(row) => row.uuid"
      :scroll-x="1500"
      @search="fetchNavigations"
      @reset="onReset"
      @reload="fetchNavigations"
    >
      <template #toolbar>
        <n-button type="primary" @click="openModal()">
          {{ $t("page.admin.navigations.table.toolbar.add") }}
        </n-button>
      </template>

      <template #search>
        <n-form
          ref="searchFormRef"
          :model="searchForm"
          inline
          label-placement="left"
        >
          <n-form-item
            :label="$t('page.admin.navigations.search.items.title')"
            path="title"
          >
            <n-input v-model:value="searchForm.title" clearable />
          </n-form-item>
          <n-form-item
            :label="$t('page.admin.navigations.search.items.category')"
            path="category"
          >
            <n-input v-model:value="searchForm.category" clearable />
          </n-form-item>
          <n-form-item
            :label="$t('page.admin.navigations.search.items.public')"
            path="is_public"
          >
            <n-select
              v-model:value="searchForm.is_public"
              :options="publicOptions"
              clearable
              class="selector"
            />
          </n-form-item>
          <n-form-item
            :label="$t('page.admin.navigations.search.items.owner')"
            path="owner_uuid"
          >
            <n-input v-model:value="searchForm.owner_uuid" clearable />
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

<script setup lang="tsx">
import { ref, reactive, onMounted, h, computed } from "vue";
import { useI18n } from "vue-i18n";

import type { Navigation } from "@/types/models";
import type { CreateNavigationDto } from "@/types/api";
import { navigationService } from "@/services/navigation";
import { notification } from "@/utils/notification";
import { CommonTable } from "@/components/common-table";
import { CommonTag } from "@/components/common-tag";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

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
  NTime,
  NEllipsis,
} from "naive-ui";

const { t } = useI18n();

const loading = ref(false);
const navigations = ref<Navigation[]>([]);

// 表格信息
const columns = computed<DataTableColumns<Navigation>>(() => [
  {
    title: "Icon",
    key: "icon",
    width: 60,
    render: (row: Navigation) => (
      <FontAwesomeIcon icon={navigationService.getIcon(row.icon)} />
    ),
  },
  { title: "Title", key: "title", width: 150 },
  {
    title: "Description",
    key: "description",
    width: 200,
    render: (row: Navigation) => (
      <NEllipsis style="max-width: 200px">
        {{ default: () => row.description || "-" }}
      </NEllipsis>
    ),
  },
  {
    title: "URL",
    key: "url",
    width: 200,
    render: (row: Navigation) => (
      <a
        href={row.url}
        target="_blank"
        style="text-decoration: none; color: inherit;"
      >
        {row.url}
      </a>
    ),
  },
  {
    title: "Category",
    key: "category",
    width: 120,
    render: (row: Navigation) => (
      <NTag type="info" size="small">
        {{ default: () => row.category || "-" }}
      </NTag>
    ),
  },
  {
    title: "Public",
    key: "is_public",
    width: 80,
    render: (row: Navigation) => (
      <CommonTag preset="nav_status" size="small" navigation={row} />
    ),
  },
  {
    title: "Owner",
    key: "owner_uuid",
    width: 150,
    render: (row: Navigation) => {
      return row.owner_uuid ? (
        <CommonTag preset="user" size="small" user_uuid={row.owner_uuid} />
      ) : (
        <CommonTag type="primary" size="small" text="System" round />
      );
    },
  },
  {
    title: "Created At",
    key: "created_at",
    width: 200,
    render: (row: Navigation) => {
      return row.created_at ? <NTime time={new Date(row.created_at)} /> : "-";
    },
  },
  {
    title: "Updated At",
    key: "updated_at",
    width: 200,
    render: (row: Navigation) => {
      return row.updated_at ? <NTime time={new Date(row.updated_at)} /> : "-";
    },
  },
  {
    title: "Actions",
    key: "actions",
    align: "center",
    width: 150,
    fixed: "right",
    render: (row: Navigation) => (
      <div style="display: flex; justify-content: center; gap: 8px;">
        <NButton size="small" onClick={() => openModal(row)}>
          Edit
        </NButton>
        <NButton size="small" type="error" onClick={() => handleDelete(row)}>
          Delete
        </NButton>
      </div>
    ),
  },
]);

// 筛选表单
const searchForm = reactive({
  title: "",
  category: "",
  is_public: null as string | null,
  owner_uuid: "",
});

const publicOptions = [
  { label: "Public", value: "true" },
  { label: "Private", value: "false" },
];

const onReset = () => {
  searchForm.title = "";
  searchForm.category = "";
  searchForm.is_public = null;
  searchForm.owner_uuid = "";
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

    if (searchForm.owner_uuid) {
      filtered = filtered.filter((n) => n.owner_uuid === searchForm.owner_uuid);
    }

    navigations.value = filtered;
  } catch (e) {
    console.error(e);
    notification.error({
      content: String(e),
      duration: 4000,
      keepAliveOnHover: true,
    });
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

.selector {
  width: 200px;
}
</style>
