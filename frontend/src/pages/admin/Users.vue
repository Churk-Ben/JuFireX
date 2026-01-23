<template>
  <div class="container">
    <h1>{{ t("sider.menu.admin.users") }}</h1>
    <p>Admin Users Management Page</p>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
const { t } = useI18n();
</script>
