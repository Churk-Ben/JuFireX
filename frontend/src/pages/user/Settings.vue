<template>
  <div class="container">
    <h1>{{ t("sider.menu.user.settings") }}</h1>
    <p>User Settings Page</p>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
const { t } = useI18n();
</script>
