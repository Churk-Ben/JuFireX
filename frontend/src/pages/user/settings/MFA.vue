<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6 offset-md-3">
        <n-card>
          <template #header>
            <div class="text-center">
              <n-h1>{{ $t("page.user.settings.account_security.2fa.title") }}</n-h1>
            </div>
          </template>

          <div v-if="loading" class="text-center">
            <n-spin size="large" />
          </div>

          <div v-else>
            <!-- 已经开启的情况 -->
            <div v-if="isEnabled && !showRecoveryCodes" class="status-view">
              <n-result
                status="success"
                :title="$t('page.user.settings.account_security.2fa.status_enabled')"
                :description="$t('page.user.settings.account_security.2fa.status_enabled_desc')"
              >
                <template #footer>
                  <n-space vertical>
                    <n-button
                      type="warning"
                      secondary
                      @click="
                        notification.info({
                          content: $t('page.user.settings.account_security.2fa.reset_not_supported'),
                        })
                      "
                    >
                      {{ $t("page.user.settings.account_security.2fa.reset_recovery_codes") }}
                    </n-button>
                    <n-button type="error" secondary @click="showDisableConfirm = true">
                      {{ $t("page.user.settings.account_security.2fa.disable") }}
                    </n-button>
                  </n-space>

                  <div v-if="showDisableConfirm">
                    <n-divider />
                    <n-input-group style="justify-content: center">
                      <n-input
                        v-model:value="verificationCode"
                        :placeholder="$t('page.user.settings.account_security.2fa.input_code_placeholder')"
                        :maxlength="6"
                        style="max-width: 200px"
                        @keyup.enter="handleDisable"
                      />
                      <n-button
                        secondary
                        @click="
                          showDisableConfirm = false;
                          verificationCode = '';
                        "
                      >
                        {{ $t("page.user.settings.account_security.2fa.cancel") }}
                      </n-button>
                      <n-button
                        type="error"
                        secondary
                        :loading="submitting"
                        @click="handleDisable"
                        :disabled="verificationCode.length !== 6"
                      >
                        {{ $t("page.user.settings.account_security.2fa.confirm_disable") }}
                      </n-button>
                    </n-input-group>
                  </div>
                </template>
              </n-result>
            </div>

            <!-- 刚刚开启成功，展示恢复代码 -->
            <div v-else-if="showRecoveryCodes" class="recovery-view">
              <n-result
                status="success"
                :title="$t('page.user.settings.account_security.2fa.setup_success_title')"
                :description="$t('page.user.settings.account_security.2fa.setup_success_desc')"
              >
                <template #default>
                  <n-alert type="warning" :show-icon="false" style="margin-top: 24px; text-align: left">
                    <p>
                      <strong>{{ $t("page.user.settings.account_security.2fa.recovery_codes_tip_1") }}</strong>
                    </p>
                    <p>{{ $t("page.user.settings.account_security.2fa.recovery_codes_tip_2") }}</p>
                    <div class="recovery-codes-grid">
                      <div v-for="(code, index) in recoveryCodes" :key="index" class="recovery-code-item">
                        {{ code }}
                      </div>
                    </div>
                  </n-alert>
                </template>
                <template #footer>
                  <n-button type="primary" @click="finishSetup">
                    {{ $t("page.user.settings.account_security.2fa.finish") }}
                  </n-button>
                </template>
              </n-result>
            </div>

            <!-- 未开启的情况，显示设置界面 -->
            <div v-else class="setup-view">
              <n-space vertical size="small">
                <n-form-item class="desc">
                  {{ $t("page.user.settings.account_security.2fa.scan_tip") }}
                </n-form-item>

                <div class="qr-code-container">
                  <n-qr-code
                    type="svg"
                    error-correction-level="Q"
                    :value="totpUri"
                    :size="200"
                    :padding="0"
                    :style="{ background: 'transparent' }"
                  />
                </div>

                <n-form-item>
                  <n-space vertical style="width: 100%">
                    <div class="desc">{{ $t("page.user.settings.account_security.2fa.manual_input_tip") }}</div>
                    <n-input v-model:value="secret" type="password" show-password-on="click" readonly />
                  </n-space>
                </n-form-item>

                <n-form-item>
                  <n-space vertical style="width: 100%">
                    <n-input-group>
                      <n-input
                        v-model:value="verificationCode"
                        :placeholder="$t('page.user.settings.account_security.2fa.scan_input_placeholder')"
                        :maxlength="6"
                        @keyup.enter="handleEnable"
                      />
                      <n-button
                        type="primary"
                        secondary
                        :loading="submitting"
                        :disabled="verificationCode.length !== 6"
                        @click="handleEnable"
                      >
                        {{ $t("page.user.settings.account_security.2fa.verify_and_enable") }}
                      </n-button>
                    </n-input-group>
                  </n-space>
                </n-form-item>
              </n-space>
            </div>
          </div>
        </n-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useI18n } from "vue-i18n";
import {
  NSpin,
  NResult,
  NButton,
  NCard,
  NH1,
  NAlert,
  NInput,
  NQrCode,
  NDivider,
  NInputGroup,
  NForm,
  NFormItem,
  NSpace,
  NFlex,
} from "naive-ui";
import { authService } from "@/services/auth";
import { notification } from "@/utils/notification";

const { t } = useI18n();

const loading = ref(true);
const submitting = ref(false);
const isEnabled = ref(false);

const showDisableConfirm = ref(false);
const showResetInfo = ref(false);

// Setup state
const totpUri = ref("");
const verificationCode = ref("");
const recoveryCodes = ref<string[]>([]);
const showRecoveryCodes = ref(false);

const secret = computed(() => {
  if (!totpUri.value) return "";
  try {
    const url = new URL(totpUri.value);
    return url.searchParams.get("secret") || "";
  } catch (e) {
    return t("page.user.settings.account_security.2fa.parse_failed");
  }
});

const checkStatus = async () => {
  loading.value = true;
  try {
    const res = await authService.check2fa();
    // @ts-ignore: res structure check
    if (res && res.is_enabled !== undefined) {
      // @ts-ignore
      isEnabled.value = res.is_enabled;
    } else {
      // @ts-ignore
      isEnabled.value = !!res?.data?.is_enabled;
    }

    if (!isEnabled.value) {
      await startSetup();
    }
  } catch (error) {
    notification.error({ content: t("page.user.settings.account_security.2fa.fetch_status_failed") });
    console.error(error);
  } finally {
    loading.value = false;
  }
};

const startSetup = async () => {
  submitting.value = true;
  try {
    const res = await authService.setup2fa();
    // @ts-ignore: 兼容可能包装在 data 里的情况
    const data = res?.data || res;
    if (data && data.uri) {
      totpUri.value = data.uri;
      if (data.recovery_codes) {
        recoveryCodes.value = data.recovery_codes;
      }
    } else {
      notification.error({ content: t("page.user.settings.account_security.2fa.fetch_secret_failed") });
    }
  } catch (error) {
    notification.error({ content: t("page.user.settings.account_security.2fa.fetch_secret_failed") });
    console.error(error);
  } finally {
    submitting.value = false;
  }
};

const handleEnable = async () => {
  if (verificationCode.value.length !== 6) return;

  submitting.value = true;
  try {
    await authService.enable2fa(verificationCode.value);
    notification.success({ content: t("page.user.settings.account_security.2fa.enable_success") });
    verificationCode.value = "";
    totpUri.value = "";

    // 开启成功后展示恢复代码
    showRecoveryCodes.value = true;
  } catch (error) {
    console.error(error);
  } finally {
    submitting.value = false;
  }
};

const finishSetup = () => {
  showRecoveryCodes.value = false;
  isEnabled.value = true;
};

const handleDisable = async () => {
  if (verificationCode.value.length !== 6) return;

  submitting.value = true;
  try {
    await authService.disable2fa(verificationCode.value);
    notification.success({ content: t("page.user.settings.account_security.2fa.disable_success") });
    isEnabled.value = false;
    showDisableConfirm.value = false;
    showResetInfo.value = false;
    verificationCode.value = "";

    // 关闭后自动重新获取新的密钥准备开启
    await startSetup();
  } catch (error) {
    console.error(error);
  } finally {
    submitting.value = false;
  }
};

onMounted(() => {
  checkStatus();
});
</script>

<style scoped>
.container {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.divider-title {
  font-size: small;
  font-weight: 300;
  opacity: 0.85;
}

.desc {
  margin-top: 0.5em;
  font-size: small;
  font-weight: 300;
  opacity: 0.85;
}

.status-view,
.recovery-view,
.setup-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.recovery-codes-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 16px;
}

.qr-code-container {
  background-color: #c2c2ca27;
  padding: 12px;
  border-radius: 8px;
}
</style>
