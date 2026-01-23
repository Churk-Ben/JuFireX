<template>
  <div class="container">
    <div class="row g-3">
      <div class="col-12">
        <h1>{{ t("navigations.title") }}</h1>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
const { t } = useI18n();
</script>