<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6 col-xl-4 offset-md-3 offset-xl-4">
        <n-card class="login-card">
          <template #header>
            <div class="text-center">
              <n-h1>{{ $t("page.login.title") }}</n-h1>
            </div>
          </template>
          <n-form ref="formRef" :model="formModel" :rules="rules">
            <n-form-item
              path="identifier"
              :label="$t('page.login.identifier.label')"
            >
              <n-input
                v-model:value="formModel.identifier"
                @keydown.enter="handleLogin"
                :placeholder="$t('page.login.identifier.placeholder')"
              />
            </n-form-item>
            <n-form-item
              path="password"
              :label="$t('page.login.password.label')"
            >
              <n-input
                v-model:value="formModel.password"
                @keydown.enter="handleLogin"
                show-password-on="click"
                type="password"
                :placeholder="$t('page.login.password.placeholder')"
              />
            </n-form-item>
            <div class="mt-4">
              <n-button
                type="primary"
                block
                :loading="userStore.loading"
                @click="handleLogin"
              >
                {{ $t("page.login.login") }}
              </n-button>
              <div class="mt-3 text-center">
                <router-link to="/register" custom #="{ navigate, href }">
                  <n-button
                    tag="a"
                    text
                    :href="href"
                    type="primary"
                    @click="navigate"
                  >
                    {{ $t("page.login.register") }}
                  </n-button>
                </router-link>
              </div>
            </div>
          </n-form>
        </n-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { NCard, NForm, NFormItem, NInput, NButton, NH1 } from "naive-ui";
import { useUserStore } from "@/stores/user";
import { notification } from "@/utils/notification";

const { t } = useI18n();
const router = useRouter();
const userStore = useUserStore();

const formModel = reactive({
  identifier: "",
  password: "",
});

const rules = {
  identifier: {
    required: true,
    message: t("page.login.identifier.validation"),
    trigger: "blur",
  },
  password: {
    required: true,
    message: t("page.login.password.validation"),
    trigger: "blur",
  },
};

let tryCount = 0;

async function handleLogin() {
  if (!formModel.identifier || !formModel.password) {
    tryCount++;
    if (tryCount > 3 && tryCount <= 6) {
      notification.warning({
        content: t("page.login.notification.level1"),
        duration: 2000,
      });
    } else if (tryCount > 6 && tryCount <= 9) {
      notification.warning({
        content: t("page.login.notification.level2"),
        duration: 2000,
      });
    } else if (tryCount > 9 && tryCount <= 10) {
      setTimeout(() => {
        notification.error({
          content: t("page.login.notification.level3"),
          duration: 6000,
        });
      }, 800);
    }
    return;
  }

  try {
    await userStore.login(formModel);
    router.push("/user/profile");
  } catch (e: any) {
    console.error(e);
  }
}
</script>

<style scoped>
.container {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
