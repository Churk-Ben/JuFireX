<template>
  <div class="container">
    <div class="row g-2">
      <div class="col-6">
        <!-- Authentication Section -->
        <n-card title="Authentication" class="my-2">
          <n-space vertical>
            <n-space>
              <n-input
                v-model:value="loginForm.identifier"
                placeholder="Email / UUID"
              />
              <n-input
                v-model:value="loginForm.password"
                placeholder="Password"
                type="password"
              />
              <n-button-group>
                <n-button @click="login">登录</n-button>
                <n-button @click="logout">注销</n-button>
                <n-button @click="checkMe">检查</n-button>
              </n-button-group>
            </n-space>
            <div v-if="currentUser">
              Current User: <strong>{{ currentUser.username }}</strong> (Role:
              {{ currentUser.role }})
            </div>
          </n-space>
        </n-card>

        <!-- Navigation API Section -->
        <n-card title="Navigation API" class="my-2">
          <n-tabs type="line">
            <n-tab-pane name="list" tab="List Categories">
              <n-button-group>
                <n-button @click="getNavCategories">Fetch Categories</n-button>
              </n-button-group>
            </n-tab-pane>
            <n-tab-pane name="create" tab="Create Category">
              <n-space vertical>
                <n-input
                  v-model:value="navForm.name"
                  placeholder="Category Name"
                />
                <n-input
                  v-model:value="navForm.icon"
                  placeholder="Icon Class (e.g. fas fa-home)"
                />
                <n-input-number
                  v-model:value="navForm.order"
                  placeholder="Order"
                />
                <n-button-group>
                  <n-button type="primary" @click="createNavCategory"
                    >Create</n-button
                  >
                </n-button-group>
              </n-space>
            </n-tab-pane>
          </n-tabs>
        </n-card>

        <!-- Projects API Section -->
        <n-card title="Projects API" class="my-2">
          <n-space>
            <n-button-group>
              <n-button @click="getProjects">List Projects</n-button>
              <n-button @click="getFeaturedProjects">List Featured</n-button>
            </n-button-group>
          </n-space>
        </n-card>
      </div>

      <div class="col-6">
        <!-- Generic Request Section -->
        <n-card title="Generic Request" class="my-2">
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
            <pre v-if="lastResponse.data">{{
              JSON.stringify(lastResponse.data, null, 2)
            }}</pre>
            <div v-else>No response yet</div>
          </n-space>
        </n-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import {
  NCard,
  NSpace,
  NInput,
  NButton,
  NTabs,
  NTabPane,
  NInputNumber,
  NSelect,
  NTag,
  NButtonGroup,
} from "naive-ui";

// State
const currentUser = ref<any>(null);
const lastResponse = reactive({
  status: 0,
  statusText: "",
  data: null as any,
});

const loginForm = reactive({ identifier: "", password: "" });
const navForm = reactive({ name: "", icon: "fas fa-link", order: 0 });
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

async function getNavCategories() {
  await request("/api/nav/categories");
}

async function createNavCategory() {
  await request("/api/nav/categories", {
    method: "POST",
    body: JSON.stringify(navForm),
  });
}

async function getProjects() {
  await request("/api/projects");
}

async function getFeaturedProjects() {
  await request("/api/projects/featured");
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

<style scoped>
.container {
  max-width: 80vw;
  margin: 0 auto;
}
</style>
