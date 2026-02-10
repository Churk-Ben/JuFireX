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
      @search="fetchUsers"
      @reset="onReset"
      @reload="fetchUsers"
    >
      <template #search>
        <n-form ref="formRef" :model="form" inline label-placement="left">
          <n-form-item label="用户名" path="username">
            <n-input
              v-model:value="form.username"
              clearable
              placeholder="请输入用户名"
            />
          </n-form-item>
          <n-form-item label="邮箱" path="email">
            <n-input
              v-model:value="form.email"
              clearable
              placeholder="请输入邮箱"
            />
          </n-form-item>
          <n-form-item label="角色" path="role">
            <n-select
              v-model:value="form.role"
              :options="roleOptions"
              clearable
              style="width: 120px"
              placeholder="请选择"
            />
          </n-form-item>
          <n-form-item label="状态" path="status">
            <n-select
              v-model:value="form.status"
              :options="statusOptions"
              clearable
              style="width: 120px"
              placeholder="请选择"
            />
          </n-form-item>
        </n-form>
      </template>
    </CommonTable>

    <!-- TODO: 弹窗组件 -->
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, h, onMounted } from "vue";
import { NForm, NFormItem, NInput, NSelect, NTag, NTime } from "naive-ui";
import { CommonTable } from "@/components/common-table";
import { userService } from "@/services/user";
import type { User } from "@/types/models";
import type { DataTableColumns } from "naive-ui";
import { notification } from "@/utils/notification";

const loading = ref(false);
const users = ref<User[]>([]);

// 筛选表单
const form = reactive({
  username: "",
  email: "",
  role: null as string | null,
  status: null as string | null, // 'true' | 'false'
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
  form.username = "";
  form.email = "";
  form.role = null;
  form.status = null;
  fetchUsers();
};

// 数据加载函数
const fetchUsers = async () => {
  loading.value = true;
  try {
    const allUsers = await userService.getAll();
    let filtered = allUsers;

    // 简单的内存过滤
    if (form.username) {
      filtered = filtered.filter((u) => u.username.includes(form.username));
    }
    if (form.email) {
      filtered = filtered.filter((u) => u.email.includes(form.email));
    }
    if (form.role) {
      filtered = filtered.filter((u) => String(u.role) === form.role);
    }
    if (form.status) {
      filtered = filtered.filter((u) => String(u.is_active) === form.status);
    }

    users.value = filtered;
  } catch (e) {
    console.error(e);
    notification.error({ content: "加载失败", title: "错误" });
  } finally {
    loading.value = false;
  }
};

const columns: DataTableColumns<User> = [
  { title: "Username", key: "username" },
  { title: "Email", key: "email" },
  {
    title: "Role",
    key: "role",
    render: (row: User) => {
      return h(
        NTag,
        {
          type: row.role >= 2 ? "error" : "success", // 2=Admin, 3=SuperAdmin
          size: "small",
        },
        { default: () => row.role_name || row.role },
      );
    },
  },
  {
    title: "Status",
    key: "is_active",
    render: (row: User) => (row.is_active ? "Active" : "Inactive"),
  },
  {
    title: "Created At",
    key: "created_at",
    render: (row: User) => {
      return row.created_at
        ? h(NTime, { time: new Date(row.created_at) })
        : "-";
    },
  },
  {
    title: "操作",
    key: "actions",
    align: "center",
    width: 150,
  },
];

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
</style>
