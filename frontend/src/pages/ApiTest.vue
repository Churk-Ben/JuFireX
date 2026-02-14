<template>
  <ScrollContainer class="container">
    <div class="row g-2">
      <div class="col-8 offset-2">
        <!-- Generic Request Section -->
        <n-card title="Generic Request" class="my-2">
          <template #header-extra>
            <n-button @click="checkMe">检查</n-button>
          </template>
          <n-space vertical>
            <n-space>
              <n-select
                v-model:value="generic.method"
                :options="methods"
                style="width: 100px"
              />
              <n-input
                v-model:value="generic.url"
                placeholder="/api/..."
                style="width: 300px"
              />
              <n-button-group>
                <n-button type="primary" @click="sendGeneric">Send</n-button>
              </n-button-group>
            </n-space>
            <n-input
              v-if="['POST', 'PUT', 'PATCH'].includes(generic.method)"
              v-model:value="generic.body"
              type="textarea"
              placeholder="JSON Body"
              :rows="3"
            />
          </n-space>
        </n-card>

        <!-- Response Console -->
        <n-card title="Response Console" class="my-2">
          <n-space vertical>
            <div v-if="lastResponse.status">
              <n-tag
                :type="
                  lastResponse.status >= 200 && lastResponse.status < 300
                    ? 'success'
                    : 'error'
                "
              >
                {{ lastResponse.status }} {{ lastResponse.statusText }}
              </n-tag>
            </div>
            <n-scrollbar style="height: 40vh">
              <n-code
                v-if="lastResponse.data"
                show-line-numbers
                language="json"
                :code="JSON.stringify(lastResponse.data, null, 2)"
              />
            </n-scrollbar>
          </n-space>
        </n-card>
      </div>
    </div>
  </ScrollContainer>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import {
  NCard,
  NSpace,
  NInput,
  NButton,
  NScrollbar,
  NSelect,
  NTag,
  NCode,
  NButtonGroup,
} from "naive-ui";

import { ScrollContainer } from "@/components/scroll-container";

// State
const currentUser = ref<any>(null);
const lastResponse = reactive({
  status: 0,
  statusText: "",
  data: null as any,
});

const loginForm = reactive({ identifier: "", password: "" });
const generic = reactive({
  method: "GET",
  url: "/api/",
  body: "{}",
});

const methods = ["GET", "POST", "PUT", "DELETE"].map((m) => ({
  label: m,
  value: m,
}));

// Helper
async function request(url: string, options: RequestInit = {}) {
  try {
    const res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });

    lastResponse.status = res.status;
    lastResponse.statusText = res.statusText;

    const contentType = res.headers.get("content-type");
    if (contentType && contentType.indexOf("application/json") !== -1) {
      lastResponse.data = await res.json();
    } else {
      lastResponse.data = await res.text();
    }

    return res;
  } catch (err: any) {
    lastResponse.status = 0;
    lastResponse.statusText = "Network Error";
    lastResponse.data = err.message;
    throw err;
  }
}

// Actions
async function login() {
  const res = await request("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(loginForm),
  });
  if (res.ok) {
    currentUser.value = lastResponse.data.user;
  }
}

async function logout() {
  await request("/api/auth/logout", { method: "POST" });
  currentUser.value = null;
}

async function checkMe() {
  const res = await request("/api/auth/me");
  if (res.ok) {
    currentUser.value = lastResponse.data;
  } else {
    currentUser.value = null;
  }
}

async function sendGeneric() {
  const options: RequestInit = {
    method: generic.method,
  };
  if (["POST", "PUT", "PATCH"].includes(generic.method)) {
    try {
      // Validate JSON
      JSON.parse(generic.body);
      options.body = generic.body;
    } catch (e) {
      alert("Invalid JSON in body");
      return;
    }
  }
  await request(generic.url, options);
}
</script>
