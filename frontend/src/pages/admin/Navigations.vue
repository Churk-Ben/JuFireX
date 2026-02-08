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
        </n-form>
      </template>
    </CommonTable>

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
} from "naive-ui";
import { CommonTable } from "@/components/common-table";
import { navigationService } from "@/services/navigation";
import type { Navigation } from "@/types/models";
import type { CreateNavigationDto } from "@/types/api";

const { t } = useI18n();

const loading = ref(false);
const navigations = ref<Navigation[]>([]);

// Search Form
const searchFormRef = ref(null);
const searchForm = reactive({
  title: "",
  category: "",
});

const onReset = () => {
  searchForm.title = "";
  searchForm.category = "";
  fetchNavigations();
};

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

const columns = [
  { title: "Title", key: "title" },
  {
    title: "URL",
    key: "url",
    render: (row: Navigation) =>
      h("a", { href: row.url, target: "_blank" }, row.url),
  },
  {
    title: "Category",
    key: "category",
    render: (row: Navigation) =>
      h(NTag, { type: "info" }, { default: () => row.category }),
  },
  {
    title: "Public",
    key: "is_public",
    render: (row: Navigation) => (row.is_public ? "Yes" : "No"),
  },
  { title: "Order", key: "order" },
  {
    title: "Actions",
    key: "actions",
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

const modalTitle = ref("Add Navigation");

async function fetchNavigations() {
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

    navigations.value = filtered;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

function openModal(nav?: Navigation) {
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
