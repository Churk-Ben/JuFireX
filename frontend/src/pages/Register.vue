<!-- @author: Churk -->
<!-- @status: 待审查 -->
<!-- @description: Register 注册页 -->

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
          <n-form ref="formRef" :model="formModel" :rules="currentRules">
            <div v-if="currentStep === 0">
              <n-form-item
                path="username"
                :label="$t('page.register.username.label')"
              >
                <n-input
                  v-model:value="formModel.username"
                  :placeholder="$t('page.register.username.placeholder')"
                />
              </n-form-item>
              <n-form-item
                path="email"
                :label="$t('page.register.email.label')"
              >
                <n-input
                  v-model:value="formModel.email"
                  :placeholder="$t('page.register.email.placeholder')"
                />
              </n-form-item>
              <n-form-item path="code" :label="$t('page.register.code.label')">
                <n-input-group>
                  <n-input
                    v-model:value="formModel.code"
                    :placeholder="$t('page.register.code.placeholder')"
                  />
                  <n-button
                    type="primary"
                    secondary
                    :disabled="countdown > 0"
                    @click="sendCode"
                  >
                    {{
                      countdown > 0
                        ? $t("page.register.code.resend", { time: countdown })
                        : $t("page.register.code.send")
                    }}
                  </n-button>
                </n-input-group>
              </n-form-item>
              <div class="mt-4">
                <n-button
                  type="primary"
                  block
                  :loading="loading"
                  @click="handleNext"
                >
                  {{ $t("page.register.next") }}
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
            </div>

            <div v-else>
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
              <div class="mb-3">
                <n-checkbox v-model:checked="agreedToPolicy">
                  {{ $t("page.register.policy.agree") }}
                  <n-button
                    text
                    type="primary"
                    tag="a"
                    href="/blogs"
                    target="_blank"
                  >
                    {{ $t("page.register.policy.privacy") }}
                  </n-button>
                  {{ $t("page.register.policy.and") }}
                  <n-button
                    text
                    type="primary"
                    tag="a"
                    href="/blogs"
                    target="_blank"
                  >
                    {{ $t("page.register.policy.terms") }}
                  </n-button>
                </n-checkbox>
              </div>
              <div class="mt-4">
                <n-button
                  type="primary"
                  block
                  :loading="loading"
                  :disabled="!agreedToPolicy"
                  @click="handleRegister"
                >
                  {{ $t("page.register.register") }}
                </n-button>
                <div class="mt-3 text-center">
                  <n-button text type="primary" @click="currentStep = 0">
                    {{ $t("page.register.back") }}
                  </n-button>
                </div>
              </div>
            </div>
          </n-form>
        </n-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NInputGroup,
  NButton,
  NCheckbox,
  FormItemRule,
  NH1,
  FormInst,
  FormRules,
} from "naive-ui";
import { authService } from "@/services/auth";
import { notification } from "@/utils/notification";

const router = useRouter();
const { t } = useI18n();

const loading = ref(false);
const currentStep = ref(0);
const countdown = ref(0);
const agreedToPolicy = ref(false);
const formRef = ref<FormInst | null>(null);

const formModel = reactive({
  username: "",
  email: "",
  code: "",
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
  code: {
    required: true,
    message: t("page.register.code.validation"),
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
        "page.register.confirmPassword.validation.confirmPasswordRequired"
      ),
      trigger: "blur",
    },
    {
      validator: (rule: FormItemRule, value: string) => {
        return value === formModel.password;
      },
      message: t(
        "page.register.confirmPassword.validation.passwordsDoNotMatch"
      ),
      trigger: ["blur", "password-input"],
    },
  ],
};

const currentRules = computed<FormRules>(() => {
  if (currentStep.value === 0) {
    return {
      username: rules.username,
      email: rules.email,
      code: rules.code,
    } as FormRules;
  } else {
    return {
      password: rules.password,
      confirmPassword: rules.confirmPassword,
    } as FormRules;
  }
});

async function sendCode() {
  if (!formModel.email) {
    notification.warning({
      content: t("page.register.email.validation"),
      duration: 2000,
    });
    return;
  }

  try {
    await authService.sendCode(formModel.email);
    notification.success({
      content: t("page.register.code.sent"),
      duration: 2000,
    });
    countdown.value = 60;
    const timer = setInterval(() => {
      countdown.value--;
      if (countdown.value <= 0) {
        clearInterval(timer);
      }
    }, 1000);
  } catch (e: any) {
    console.error(e);
  }
}

async function handleNext() {
  if (!formRef.value) return;

  formRef.value.validate(async (errors) => {
    if (!errors) {
      loading.value = true;
      try {
        await authService.verifyCode(formModel.email, formModel.code);
        currentStep.value = 1;
      } catch (e: any) {
        console.error(e);
      } finally {
        loading.value = false;
      }
    }
  });
}

async function handleRegister() {
  if (!formRef.value) return;

  formRef.value.validate(async (errors) => {
    if (!errors) {
      loading.value = true;
      try {
        const { username, email, password, code } = formModel;
        await authService.register({ username, email, password, code });
        router.push("/login");
      } catch (e: any) {
        console.error(e);
      } finally {
        loading.value = false;
      }
    }
  });
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
