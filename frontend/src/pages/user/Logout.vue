<template>
  <div class="container">
    <h1>{{ t("sider.menu.user.logout") }}</h1>
    <p>Logging out...</p>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { onMounted } from "vue";

const { t } = useI18n();
const router = useRouter();

onMounted(() => {
  // Simulate logout process
  setTimeout(() => {
    // Clear tokens here if needed
    // localStorage.removeItem('token');
    router.push("/");
  }, 1000);
});
</script>
