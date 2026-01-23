<template>
  <div class="container">
    <h1>{{ t("sider.menu.user.profile") }}</h1>
    <p>User Profile Page</p>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
const { t } = useI18n();
</script>
