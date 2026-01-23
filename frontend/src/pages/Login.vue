<template>
  <div class="login-container">
    <n-card class="login-card">
      <template #header>
        <div class="text-center">
          <h2>{{ t("sider.menu.user.login") }}</h2>
        </div>
      </template>
      <n-form ref="formRef" :model="formModel" :rules="rules">
        <n-form-item path="identifier" label="Email / UUID">
          <n-input
            v-model:value="formModel.identifier"
            placeholder="Email or UUID"
            @keydown.enter="handleLogin"
          />
        </n-form-item>
        <n-form-item path="password" :label="t('login.password')">
          <n-input
            v-model:value="formModel.password"
            type="password"
            show-password-on="click"
            @keydown.enter="handleLogin"
          />
        </n-form-item>
        <div class="actions">
          <n-button
            type="primary"
            block
            :loading="userStore.loading"
            @click="handleLogin"
          >
            {{ t("sider.menu.user.login") }}
          </n-button>
          <div class="mt-3 text-center">
            <router-link to="/register">Register new account</router-link>
          </div>
        </div>
      </n-form>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useMessage, NCard, NForm, NFormItem, NInput, NButton } from "naive-ui";
import { useUserStore } from "@/stores/user";

const { t } = useI18n();
const router = useRouter();
const message = useMessage();
const userStore = useUserStore();

const formRef = ref(null);
const formModel = reactive({
  identifier: "",
  password: "",
});

const rules = {
  identifier: {
    required: true,
    message: "Please input Email or UUID",
    trigger: "blur",
  },
  password: {
    required: true,
    message: t("login.validation.passwordRequired"),
    trigger: "blur",
  },
};

async function handleLogin() {
  if (!formModel.identifier || !formModel.password) return;

  try {
    await userStore.login(formModel);
    message.success(t("login.success"));
    router.push("/");
  } catch (e: any) {
    message.error(e.message || "Login failed");
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.text-center {
  text-align: center;
}

.actions {
  margin-top: 24px;
}
</style>
