<template>
  <div class="container">
    <div class="row justify-content-center">
      <h1>{{ t("sider.menu.user.logout") }}</h1>
      <p>Logging out...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { onMounted } from "vue";
import { useUserStore } from "@/stores/user";

const { t } = useI18n();
const router = useRouter();
const userStore = useUserStore();

async function onLogout() {
  await userStore.logout();
  router.push("/");
}

onMounted(() => {
  // 等待一秒后再执行注销操作
  setTimeout(() => {
    onLogout();
  }, 1000);
});
</script>
