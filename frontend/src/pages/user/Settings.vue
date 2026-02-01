<template>
  <div class="container p-4">
    <h1>{{ t("sider.userMenu.user.settings") }}</h1>

    <n-form>
      <n-form-item :label="t('settings.theme')">
        <n-select
          v-model:value="themeStore.currentTheme"
          :options="themeOptions"
        />
      </n-form-item>
    </n-form>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { NForm, NFormItem, NSelect } from "naive-ui";
import { useThemeStore } from "@/stores/theme";
import { themes } from "@/themes";

const { t } = useI18n();
const themeStore = useThemeStore();

const themeOptions = computed(() => {
  return Object.keys(themes).map((key) => ({
    label: key,
    value: key,
  }));
});
</script>
