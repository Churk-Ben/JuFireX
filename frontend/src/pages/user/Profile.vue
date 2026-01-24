<template>
  <div class="user-profile">
    <n-card title="My Profile">
      <div class="profile-header">
        <div class="avatar-section">
          <n-avatar round :size="128" :src="avatarUrl" class="mb-3" />
          <avatar-cropper @cropped="handleAvatarCrop">
            <n-button>Change Avatar</n-button>
          </avatar-cropper>
        </div>

        <div class="info-section">
          <n-descriptions label-placement="left" bordered :column="1">
            <n-descriptions-item label="Username">
              {{ userStore.currentUser?.username }}
            </n-descriptions-item>
            <n-descriptions-item label="Email">
              {{ userStore.currentUser?.email }}
            </n-descriptions-item>
            <n-descriptions-item label="Role">
              {{ userStore.currentUser?.role_name }}
            </n-descriptions-item>
            <n-descriptions-item label="UUID">
              {{ userStore.currentUser?.uuid }}
            </n-descriptions-item>
            <n-descriptions-item label="Joined At">
              {{ formatDate(userStore.currentUser?.created_at) }}
            </n-descriptions-item>
          </n-descriptions>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { userService } from "@/services/user";
import {
  useMessage,
  NCard,
  NAvatar,
  NButton,
  NDescriptions,
  NDescriptionsItem,
} from "naive-ui";
import AvatarCropper from "@/components/AvatarCropper.vue";

const userStore = useUserStore();
const message = useMessage();
const timestamp = ref(Date.now());

const avatarUrl = computed(() => {
  if (!userStore.currentUser?.uuid) return "";
  return (
    userService.getAvatarUrl(userStore.currentUser.uuid) +
    `?t=${timestamp.value}`
  );
});

function formatDate(dateStr?: string) {
  if (!dateStr) return "-";
  return new Date(dateStr).toLocaleString();
}

async function handleAvatarCrop(blob: Blob) {
  try {
    const file = new File([blob], "avatar.png", { type: "image/png" });
    await userService.uploadAvatar(file);
    // Success message is handled by request interceptor
    // Refresh avatar image
    timestamp.value = Date.now();
  } catch (e: any) {
    // Error message is handled by request interceptor
    console.error(e);
  }
}

onMounted(() => {
  if (!userStore.currentUser) {
    userStore.checkAuth();
  }
});
</script>

<style scoped>
.user-profile {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
}

.profile-header {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 150px;
}

.info-section {
  flex: 1;
}

.mb-3 {
  margin-bottom: 1rem;
}

@media (max-width: 600px) {
  .profile-header {
    flex-direction: column;
    align-items: center;
  }

  .info-section {
    width: 100%;
  }
}
</style>
