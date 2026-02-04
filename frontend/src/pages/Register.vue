<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6 col-xl-4 offset-md-3 offset-xl-4">
        <n-card class="register-card">
          <template #header>
            <div class="text-center">
              <n-h1>{{ $t("page.register.title") }}</n-h1>
            </div>
          </template>
          <n-form ref="formRef" :model="formModel" :rules="rules">
            <n-form-item
              path="username"
              :label="$t('page.register.username.label')"
            >
              <n-input
                v-model:value="formModel.username"
                :placeholder="$t('page.register.username.placeholder')"
              />
            </n-form-item>
            <n-form-item path="email" :label="$t('page.register.email.label')">
              <n-input
                v-model:value="formModel.email"
                :placeholder="$t('page.register.email.placeholder')"
              />
            </n-form-item>
            <n-form-item
              path="password"
              :label="$t('page.register.password.label')"
            >
              <n-input
                v-model:value="formModel.password"
                type="password"
                show-password-on="click"
                :placeholder="$t('page.register.password.placeholder')"
              />
            </n-form-item>
            <n-form-item
              path="confirmPassword"
              :label="$t('page.register.confirmPassword.label')"
            >
              <n-input
                v-model:value="formModel.confirmPassword"
                type="password"
                show-password-on="click"
                :placeholder="$t('page.register.confirmPassword.placeholder')"
              />
            </n-form-item>
            <div class="mt-4">
              <n-button
                type="primary"
                block
                :loading="loading"
                @click="handleRegister"
              >
                {{ $t("page.register.register") }}
              </n-button>
              <div class="mt-3 text-center">
                <router-link to="/login" custom #="{ navigate, href }">
                  <n-button
                    tag="a"
                    text
                    :href="href"
                    type="primary"
                    @click="navigate"
                  >
                    {{ $t("page.register.login") }}
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
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NButton,
  FormItemRule,
  NH1,
} from "naive-ui";
import { authService } from "@/services/auth";
import { notification } from "@/utils/notification";

const router = useRouter();
const { t } = useI18n();

const loading = ref(false);
const formModel = reactive({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const rules = {
  username: {
    required: true,
    message: t("page.register.username.validation"),
    trigger: "blur",
  },
  email: {
    required: true,
    message: t("page.register.email.validation"),
    trigger: "blur",
  },
  password: {
    required: true,
    message: t("page.register.password.validation"),
    trigger: "blur",
  },
  confirmPassword: [
    {
      required: true,
      message: t(
        "page.register.confirmPassword.validation.confirmPasswordRequired",
      ),
      trigger: "blur",
    },
    {
      validator: (rule: FormItemRule, value: string) => {
        return value === formModel.password;
      },
      message: t(
        "page.register.confirmPassword.validation.passwordsDoNotMatch",
      ),
      trigger: ["blur", "password-input"],
    },
  ],
};

async function handleRegister() {
  if (!formModel.username || !formModel.email || !formModel.password) {
    notification.warning({
      content: t("page.register.notification.emptyFields"),
      duration: 2000,
    });
    return;
  }
  if (formModel.password !== formModel.confirmPassword) {
    notification.warning({
      content: t("page.register.notification.passwordsDoNotMatch"),
      duration: 2000,
    });
    return;
  }

  loading.value = true;
  try {
    const { username, email, password } = formModel;
    await authService.register({ username, email, password });
    router.push("/login");
  } catch (e: any) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}
</style>
