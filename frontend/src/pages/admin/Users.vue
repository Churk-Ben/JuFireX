<template>
  <div class="page-container">
    <n-space vertical size="large">
      <n-space justify="space-between" align="center">
        <n-h1 style="margin: 0">{{ t("sider.menu.admin.users") }}</n-h1>
        <!-- User creation is typically done via Registration, but admins might want to add users manually. 
             For now, we just list them. -->
        <n-button type="primary" disabled>
          Add User (Not Implemented)
        </n-button>
      </n-space>

      <n-card>
        <n-data-table
          :columns="columns"
          :data="users"
          :loading="loading"
          :pagination="pagination"
        />
      </n-card>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from "vue";
import { useI18n } from "vue-i18n";
import {
  NCard,
  NButton,
  NDataTable,
  NSpace,
  NH1,
  NTag,
  NTime,
  NScrollbar,
} from "naive-ui";
import { userService } from "@/services/user";
import type { User } from "@/types/models";

const { t } = useI18n();

const loading = ref(false);
const users = ref<User[]>([]);
const pagination = { pageSize: 10 };

const columns = [
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
      // @ts-ignore - NTime needs string or number, assuming created_at is ISO string
      return row.created_at
        ? h(NTime, { time: new Date(row.created_at) })
        : "-";
    },
  },
];

async function fetchUsers() {
  loading.value = true;
  try {
    users.value = await userService.getAll();
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
.page-container {
  padding: 24px;
}
</style>
