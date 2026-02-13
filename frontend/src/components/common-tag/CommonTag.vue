<!-- @author: Churk -->
<!-- @status: 阶段性完工 -->
<!-- @description: 通用标签组件，用于展示用户标签、角色标签、用户状态标签、导航项公开状态标签等 -->

<template>
  <!-- 用户标签/徽章 -->
  <template v-if="$props.preset === 'user'">
    <n-tag
      round
      bordered
      class="my-1"
      :type="getTypeByUserRole(currentUser)"
      :size="size"
      :strong="strong"
    >
      <template #avatar>
        <n-avatar :src="userService.getAvatarUrl(currentUser?.uuid!)" />
      </template>
      {{ currentUser?.username || "Unknown" }}
    </n-tag>
  </template>

  <!-- 角色标签/徽章 -->
  <template v-else-if="$props.preset === 'role'">
    <n-tag
      round
      bordered
      :type="getTypeByUserRole(currentUser)"
      :size="size"
      :strong="strong"
    >
      {{ currentUser?.role_name || "Unknown" }}
    </n-tag>
  </template>

  <!-- 用户状态标签 -->
  <template v-else-if="$props.preset === 'user_status'">
    <n-tag
      round
      bordered
      :type="getTypeByUserStatus(currentUser)"
      :size="size"
      :strong="strong"
    >
      {{
        currentUser?.is_active
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
    <n-tag :type="type" :size="size" :strong="strong" :round="round">
      {{ text }}
    </n-tag>
  </template>
</template>

<script setup lang="ts">
import { type PropType, ref, watch } from "vue";

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
  round: {
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
  user_uuid: {
    type: String,
    default: "",
  },
  navigation: {
    type: Object as PropType<Navigation>,
    default: null,
  },
});

const currentUser = ref<User | null>(null);

watch(
  () => [props.user, props.user_uuid],
  async () => {
    if (props.user) {
      currentUser.value = props.user;
    } else if (props.user_uuid) {
      try {
        currentUser.value = await userService.get(props.user_uuid, {
          silent: true,
        });
      } catch (e) {
        // Ignore error
        currentUser.value = null;
      }
    } else {
      currentUser.value = null;
    }
  },
  { immediate: true },
);

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
