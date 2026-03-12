<!-- @author: Churk -->
<!-- @status: 完工 -->
<!-- @description: ApiTest 测试页 -->

<template>
  <ScrollContainer>
    <n-space vertical size="large">
      <n-h1>{{ $t("page.apiTest.title") }}</n-h1>

      <div class="container">
        <div class="row g-3">
          <!-- Generic Request Section -->
          <div class="col-4">
            <n-card
              :title="$t('page.apiTest.genericRequest.title')"
              class="my-2 h-100"
            >
              <template #header-extra>
                <n-space size="small">
                  <n-button @click="checkMe">
                    {{ $t("page.apiTest.genericRequest.check") }}
                  </n-button>
                  <n-button type="primary" @click="sendGeneric">
                    {{ $t("page.apiTest.genericRequest.send") }}
                  </n-button>
                </n-space>
              </template>
              <n-space vertical size="large">
                <n-space>
                  <n-input-group>
                    <n-select
                      v-model:value="generic.method"
                      :options="methods"
                      style="width: 100px"
                    />
                    <n-input
                      v-model:value="generic.url"
                      placeholder="/api/"
                      style="width: 300px"
                    />
                  </n-input-group>
                </n-space>
                <n-input
                  v-model:value="generic.body"
                  type="textarea"
                  placeholder="JSON Body"
                  :disabled="!['POST', 'PUT', 'PATCH'].includes(generic.method)"
                  :autosize="{ minRows: 5, maxRows: 25 }"
                />
              </n-space>
            </n-card>
          </div>

          <!-- Response Console -->
          <div class="col-8">
            <n-card
              :title="$t('page.apiTest.responseConsole')"
              class="my-2 h-100"
            >
              <template #header-extra>
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
              </template>
              <n-space vertical>
                <n-config-provider :hljs="hljs">
                  <!-- 操这里这个高度真给我调崩溃了`^´# -->
                  <ScrollContainer style="height: calc(75vh - 36px)">
                    <n-code
                      v-if="lastResponse.data"
                      show-line-numbers
                      language="json"
                      :code="JSON.stringify(lastResponse.data, null, 2)"
                    />
                  </ScrollContainer>
                </n-config-provider>
              </n-space>
            </n-card>
          </div>
        </div>
      </div>
    </n-space>
  </ScrollContainer>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import {
  NH1,
  NCard,
  NSpace,
  NInput,
  NButton,
  NInputGroup,
  NSelect,
  NTag,
  NCode,
  NConfigProvider,
} from "naive-ui";

import { ScrollContainer } from "@/components/scroll-container";
import { notification } from "@/utils/notification";
import hljs from "highlight.js";

// State
const currentUser = ref<any>(null);
const lastResponse = reactive({
  status: 0,
  statusText: "",
  data: null as any,
});

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
      // 验证 JSON
      JSON.parse(generic.body);
      options.body = generic.body;
    } catch (e) {
      notification.error({
        content: "请求体JSON不合法",
        duration: 3000,
      });
      return;
    }
  }
  await request(generic.url, options);
}
</script>
