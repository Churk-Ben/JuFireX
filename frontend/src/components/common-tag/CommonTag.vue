<template>
  <!-- 用户标签/徽章 -->
  <template v-if="$props.preset === 'user'">
    <n-tag
      round
      bordered
      :type="getTypeByUserRole(user)"
      :size="size"
      :strong="strong"
    >
      <template #avatar>
        <n-avatar :src="userService.getAvatarUrl(user?.uuid)" />
      </template>
      {{ user?.username || "Unknown" }}
    </n-tag>
  </template>

  <!-- 角色标签/徽章 -->
  <template v-else-if="$props.preset === 'role'">
    <n-tag
      round
      bordered
      :type="getTypeByUserRole(user)"
      :size="size"
      :strong="strong"
    >
      {{ user?.role_name || "Unknown" }}
    </n-tag>
  </template>

  <!-- 用户状态标签 -->
  <template v-else-if="$props.preset === 'user_status'">
    <n-tag
      round
      bordered
      :type="getTypeByUserStatus(user)"
      :size="size"
      :strong="strong"
    >
      {{
        user?.is_active
          ? $t("page.admin.users.table.columns.status.active")
          : $t("page.admin.users.table.columns.status.inactive")
      }}
    </n-tag>
  </template>

  <!-- 导航项公开状态标签 -->
  <template v-else-if="$props.preset === 'nav_status'">
    <n-tag
      round
      bordered
      :type="getTypeByNavStatus(navigation)"
      :size="size"
      :strong="strong"
    >
      {{
        navigation?.is_public
          ? $t("page.admin.navigations.table.columns.status.public")
          : $t("page.admin.navigations.table.columns.status.private")
      }}
    </n-tag>
  </template>

  <template v-else>
    <n-tag :type="type" :size="size" :strong="strong">
      {{ text }}
    </n-tag>
  </template>
</template>

<script setup lang="ts">
import { type PropType } from "vue";

import { NTag, NAvatar } from "naive-ui";

import type { User, Navigation } from "@/types/models";
import { userService } from "@/services/user";

defineOptions({
  name: "CommonTag",
});

const props = defineProps({
  preset: {
    type: String,
    default: undefined,
  },
  size: {
    type: String as PropType<"medium" | "small" | "tiny" | "large" | undefined>,
    default: "medium",
  },
  strong: {
    type: Boolean,
    default: false,
  },
  type: {
    type: String as PropType<
      "primary" | "success" | "warning" | "error" | "default" | undefined
    >,
    default: "primary",
  },
  text: {
    type: String,
    default: "",
  },
  user: {
    type: Object as PropType<User>,
    default: null,
  },
  navigation: {
    type: Object as PropType<Navigation>,
    default: null,
  },
});

const getTypeByUserRole = (user: User | null) => {
  if (!user) return "default";
  switch (user.role) {
    case 3: // SuperAdmin
      return "error";
    case 2: // Admin
      return "warning";
    case 1: // Member
      return "info";
    case 0: // Guest or Unkown
    default:
      return "default";
  }
};

const getTypeByUserStatus = (user: User | null) => {
  if (!user) return "default";
  return user.is_active ? "success" : "error";
};

const getTypeByNavStatus = (navigation: Navigation | null) => {
  if (!navigation) return "default";
  return navigation.is_public ? "success" : "error";
};
</script>
