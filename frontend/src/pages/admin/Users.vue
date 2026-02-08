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
        <NForm ref="formRef" :model="form" inline label-placement="left">
          <NFormItem label="用户名" path="username">
            <NInput
              v-model:value="form.username"
              clearable
              placeholder="请输入用户名"
            />
          </NFormItem>
          <NFormItem label="角色" path="role">
            <NSelect
              v-model:value="form.role"
              :options="roleOptions"
              clearable
              style="width: 120px"
              placeholder="请选择"
            />
          </NFormItem>
        </NForm>
      </template>
    </CommonTable>

    <!-- 弹窗组件复用 -->
  </div>
</template>

<script setup lang="tsx">
import { ref, reactive, h, onMounted } from "vue";
import {
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NButton,
  NTag,
  NPopconfirm,
  NTime,
} from "naive-ui";
import CommonTable from "@/components/common-table/CommonTable.vue";
import { userService } from "@/services/user";
import type { User } from "@/types/models";
import type { DataTableColumns } from "naive-ui";
import { notification } from "@/utils/notification";

// 表单数据
const form = reactive({
  username: "",
  role: null as string | null,
});

const roleOptions = [
  { label: "超级管理员", value: "3" },
  { label: "管理员", value: "2" },
  { label: "成员", value: "1" },
  { label: "游客", value: "0" },
];

const tableRef = ref();
const loading = ref(false);
const users = ref<User[]>([]);

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
    if (form.role) {
      filtered = filtered.filter((u) => String(u.role) === form.role);
    }

    users.value = filtered;
  } catch (e) {
    console.error(e);
    notification.error({ content: "加载失败", title: "错误" });
  } finally {
    loading.value = false;
  }
};

const onReset = () => {
  form.username = "";
  form.role = null;
  fetchUsers();
};

const handleDelete = async (uuid: string) => {
  try {
    notification.success({ content: "删除成功", title: "成功" });
    tableRef.value?.reload();
  } catch (e) {
    notification.error({ content: "删除失败", title: "错误" });
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
    render: (row: User) => (
      <div class="d-flex gap-1">
        <NButton
          size="small"
          secondary
          type="primary"
          onClick={() =>
            notification.info({ content: "编辑 " + row.uuid, title: "提示" })
          }
        >
          编辑
        </NButton>
        <NPopconfirm
          onPositiveClick={() => handleDelete(row.uuid)}
          v-slots={{
            trigger: () => (
              <NButton size="small" secondary type="error">
                删除
              </NButton>
            ),
            default: () => "确认删除吗？",
          }}
        />
      </div>
    ),
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
