<!-- @author: Churk -->
<!-- @status: 待修缮, 我要在这个页面疯狂藏彩蛋 :P -->
<!-- @description: Logout 注销页 -->

<template>
  <ScrollContainer>
    <n-space vertical size="large">
      <n-h1>{{ $t("page.user.logout.title") }}</n-h1>

      <n-result
        status="warning"
        style="margin-top: 25vh"
        :title="$t('page.user.logout.result.title')"
        :description="$t('page.user.logout.result.description')"
      >
        <template #footer>
          <n-button @click="onLogout">
            {{ $t("page.user.logout.result.confirm") }}
          </n-button>
        </template>
      </n-result>
    </n-space>
  </ScrollContainer>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { NH1, NSpace, NButton, NResult } from "naive-ui";
import { ScrollContainer } from "@/components/scroll-container";

const router = useRouter();
const userStore = useUserStore();

async function onLogout() {
  await userStore.logout();
  router.push("/");
}

onMounted(() => {
  // 等待一秒后再执行注销操作
  // setTimeout(() => {
  //   onLogout();
  // }, 1000);
});
</script>
