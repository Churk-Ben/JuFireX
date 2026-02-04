<template>
  <div class="container">
    <div class="row">
      <div class="col-4 offset-4">
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
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { NCard, NForm, NFormItem, NInput, NButton, NH1 } from "naive-ui";
import { useUserStore } from "@/stores/user";

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
    message: t("page.login.validation.identifierRequired"),
    trigger: "blur",
  },
  password: {
    required: true,
    message: t("page.login.validation.passwordRequired"),
    trigger: "blur",
  },
};

async function handleLogin() {
  try {
    await userStore.login(formModel);
    router.push("/");
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
