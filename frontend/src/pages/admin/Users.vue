<template>
  <div class="page-container">
    <CommonTable
      ref="tableRef"
      :searchTitle="$t('page.admin.users.search.title')"
      :tableTitle="$t('page.admin.users.table.title')"
      :columns="columns"
      :data="users"
      :loading="loading"
      :row-key="(row) => row.uuid"
      :scroll-x="1500"
      @search="fetchUsers"
      @reset="onReset"
      @reload="fetchUsers"
    >
      <!-- TODO -->
      <template #toolbar>
        <n-button
          type="primary"
          @click="
            () => {
              notification.info({
                content: 'Add User',
                duration: 1000,
              });
            }
          "
        >
          {{ $t("page.admin.users.table.toolbar.add") }}
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
            :label="$t('page.admin.users.search.items.username')"
            path="username"
          >
            <n-input v-model:value="searchForm.username" clearable />
          </n-form-item>
          <n-form-item
            :label="$t('page.admin.users.search.items.email')"
            path="email"
          >
            <n-input v-model:value="searchForm.email" clearable />
          </n-form-item>
          <n-form-item
            :label="$t('page.admin.users.search.items.role')"
            path="role"
          >
            <n-select
              v-model:value="searchForm.role"
              :options="roleOptions"
              clearable
              class="selector"
            />
          </n-form-item>
          <n-form-item
            :label="$t('page.admin.users.search.items.status')"
            path="status"
          >
            <n-select
              v-model:value="searchForm.status"
              :options="statusOptions"
              clearable
              class="selector"
            />
          </n-form-item>
        </n-form>
      </template>
    </CommonTable>

    <!-- TODO: 模态框 -->
  </div>
</template>

<script setup lang="tsx">
import { ref, reactive, h, onMounted, computed } from "vue";
import { useI18n } from "vue-i18n";

import type { User } from "@/types/models";
import { userService } from "@/services/user";
import { notification } from "@/utils/notification";
import { CommonTable } from "@/components/common-table";
import { CommonTag } from "@/components/common-tag";

import type { DataTableColumns } from "naive-ui";
import { NForm, NFormItem, NInput, NSelect, NTime, NButton } from "naive-ui";

const { t } = useI18n();

const loading = ref(false);
const users = ref<User[]>([]);

// 表格信息
const columns = computed<DataTableColumns<User>>(() => [
  {
    title: t("page.admin.users.table.columns.user"),
    key: "user",
    width: 150,
    render: (row: User) => <CommonTag preset="user" size="medium" user={row} />,
  },
  {
    title: t("page.admin.users.table.columns.email"),
    key: "email",
    width: 200,
  },
  {
    title: t("page.admin.users.table.columns.uuid"),
    key: "uuid",
    width: 300,
  },
  {
    title: t("page.admin.users.table.columns.role"),
    key: "role",
    width: 100,
    render: (row: User) => <CommonTag preset="role" size="small" user={row} />,
  },
  {
    title: t("page.admin.users.table.columns.status.title"),
    key: "is_active",
    width: 100,
    render: (row: User) => (
      <CommonTag preset="user_status" size="small" user={row} />
    ),
  },
  {
    title: t("page.admin.users.table.columns.createdAt"),
    key: "created_at",
    width: 150,
    render: (row: User) => {
      return row.created_at ? <NTime time={new Date(row.created_at)} /> : "-";
    },
  },
  {
    title: t("page.admin.users.table.columns.actions.title"),
    key: "actions",
    align: "center",
    width: 150,
    fixed: "right",
    render: (row: User) => (
      <div style="display: flex; justify-content: center; gap: 8px;">
        <NButton
          type="primary"
          size="small"
          onClick={() => {
            isEditing.value = true;
            currentUuid.value = row.uuid;
            modalTitle.value = t("page.admin.users.table.columns.actions.edit");
            showModal.value = true;
          }}
        >
          {t("page.admin.users.table.columns.actions.edit")}
        </NButton>
        <NButton
          type="error"
          size="small"
          onClick={() => {
            notification.warning({
              content: "Delete action not implemented",
              duration: 2000,
            });
          }}
        >
          {t("page.admin.users.table.columns.actions.delete")}
        </NButton>
      </div>
    ),
  },
]);

// 筛选表单
const searchForm = reactive({
  username: "",
  email: "",
  role: null as string | null,
  status: null as string | null,
});

const roleOptions = [
  { label: "超级管理员", value: "3" },
  { label: "管理员", value: "2" },
  { label: "成员", value: "1" },
  { label: "游客", value: "0" },
];

const statusOptions = [
  { label: "激活", value: "true" },
  { label: "禁用", value: "false" },
];

const onReset = () => {
  searchForm.username = "";
  searchForm.email = "";
  searchForm.role = null;
  searchForm.status = null;
  fetchUsers();
};

// 数据加载函数
const fetchUsers = async () => {
  loading.value = true;
  try {
    const allUsers = await userService.getAll();
    let filtered = allUsers;

    // 内存过滤
    if (searchForm.username) {
      filtered = filtered.filter((u) =>
        u.username.includes(searchForm.username),
      );
    }
    if (searchForm.email) {
      filtered = filtered.filter((u) => u.email.includes(searchForm.email));
    }
    if (searchForm.role) {
      filtered = filtered.filter((u) => String(u.role) === searchForm.role);
    }
    if (searchForm.status) {
      filtered = filtered.filter(
        (u) => String(u.is_active) === searchForm.status,
      );
    }

    users.value = filtered;
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
const modalTitle = ref("Add User");
const showModal = ref(false);
const submitting = ref(false);
const formRef = ref(null);
const isEditing = ref(false);
const currentUuid = ref("");

onMounted(() => {
  fetchUsers();
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
