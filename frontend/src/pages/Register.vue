<template>
  <div class="register-container">
    <n-card class="register-card">
      <template #header>
        <div class="text-center">
          <h2>Register</h2>
        </div>
      </template>
      <n-form ref="formRef" :model="formModel" :rules="rules">
        <n-form-item path="username" label="Username">
          <n-input
            v-model:value="formModel.username"
            placeholder="Username"
          />
        </n-form-item>
        <n-form-item path="email" label="Email">
          <n-input
            v-model:value="formModel.email"
            placeholder="Email"
          />
        </n-form-item>
        <n-form-item path="password" label="Password">
          <n-input
            v-model:value="formModel.password"
            type="password"
            show-password-on="click"
          />
        </n-form-item>
        <n-form-item path="confirmPassword" label="Confirm Password">
          <n-input
            v-model:value="formModel.confirmPassword"
            type="password"
            show-password-on="click"
          />
        </n-form-item>
        <div class="actions">
          <n-button
            type="primary"
            block
            :loading="loading"
            @click="handleRegister"
          >
            Register
          </n-button>
          <div class="mt-3 text-center">
            <router-link to="/login">Already have an account? Login</router-link>
          </div>
        </div>
      </n-form>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useMessage, NCard, NForm, NFormItem, NInput, NButton, FormItemRule } from "naive-ui";
import { authService } from "@/services/auth";

const router = useRouter();
const message = useMessage();

const formRef = ref(null);
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
    message: "Please input username",
    trigger: "blur",
  },
  email: {
    required: true,
    message: "Please input email",
    trigger: "blur",
  },
  password: {
    required: true,
    message: "Please input password",
    trigger: "blur",
  },
  confirmPassword: [
    {
      required: true,
      message: "Please confirm your password",
      trigger: "blur",
    },
    {
      validator: (rule: FormItemRule, value: string) => {
        return value === formModel.password;
      },
      message: "Passwords do not match",
      trigger: ["blur", "password-input"],
    },
  ],
};

async function handleRegister() {
  if (!formModel.username || !formModel.email || !formModel.password) return;
  if (formModel.password !== formModel.confirmPassword) {
    message.error("Passwords do not match");
    return;
  }

  loading.value = true;
  try {
    const { username, email, password } = formModel;
    await authService.register({ username, email, password });
    router.push("/login");
  } catch (e: any) {
    // Error is handled by request interceptor
    console.error(e);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.register-card {
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
