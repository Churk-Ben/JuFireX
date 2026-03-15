<template>
  <ScrollContainer>
    <n-space vertical size="large">
      <n-h1>{{ $t("page.user.settings.title") }}</n-h1>

      <div class="container">
        <div class="row">
          <div class="col-md-8 offset-md-2">
            <n-card>
              <n-tabs type="line" size="large" animated>
                <!-- 个人信息设置 -->
                <n-tab-pane
                  name="personal"
                  display-directive="show"
                  :tab="$t('page.user.settings.personal.title')"
                >
                  <n-form
                    ref="profileFormRef"
                    :model="profileForm"
                    label-placement="left"
                    label-width="200"
                    require-mark-placement="right-hanging"
                  >
                    <n-divider title-placement="left">
                      <span class="divider-title">
                        {{ $t("page.user.settings.personal.profile.title") }}
                      </span>
                    </n-divider>
                    <n-form-item :label="$t('page.user.settings.personal.profile.avatar')">
                      <n-avatar round :size="128" :src="avatarUrl" class="mb-3" />
                      <AvatarCropper @cropped="handleAvatarCrop">
                        <n-button
                          style="transform: translateX(-75%) translateY(125%)"
                          circle
                          secondary
                          bordered
                          type="primary"
                        >
                          <template #icon>
                            <FontAwesomeIcon :icon="faCamera" />
                          </template>
                        </n-button>
                      </AvatarCropper>
                    </n-form-item>
                    <n-form-item
                      :label="$t('page.user.settings.personal.profile.username')"
                      path="username"
                      required
                    >
                      <n-input
                        v-model:value="profileForm.username"
                        :placeholder="
                          $t('page.user.settings.personal.profile.username_placeholder')
                        "
                      />
                    </n-form-item>
                    <n-form-item :label="$t('page.user.settings.personal.profile.bio')" path="bio">
                      <n-input
                        v-model:value="profileForm.bio"
                        type="textarea"
                        :placeholder="$t('page.user.settings.personal.profile.bio_placeholder')"
                        :rows="4"
                        :maxlength="128"
                      />
                    </n-form-item>
                    <n-form-item style="display: flex; justify-content: flex-end">
                      <n-button type="primary" @click="handleSaveProfile">
                        {{ $t("page.user.settings.common.save") }}
                      </n-button>
                    </n-form-item>
                  </n-form>
                  <n-form
                    ref="urlFormRef"
                    :model="urlForm"
                    label-placement="left"
                    label-width="200"
                  >
                    <n-divider title-placement="left">
                      <span class="divider-title">
                        {{ $t("page.user.settings.personal.urls.title") }}
                      </span>
                    </n-divider>
                    <n-form-item path="urls">
                      <div class="desc">
                        <!-- prettier-ignore -->
                        {{ $t("page.user.settings.personal.urls.desc") }}
                      </div>
                    </n-form-item>
                    <n-form-item style="display: flex; justify-content: flex-end">
                      <n-button type="primary">
                        {{ $t("page.user.settings.common.save") }}
                      </n-button>
                    </n-form-item>
                  </n-form>
                </n-tab-pane>

                <!-- 账户与安全设置 -->
                <n-tab-pane
                  name="account_security"
                  display-directive="show"
                  :tab="$t('page.user.settings.account_security.title')"
                >
                  <n-form label-placement="left" label-width="200">
                    <n-divider title-placement="left">
                      <span class="divider-title">
                        {{ $t("page.user.settings.account_security.account.title") }}
                      </span>
                    </n-divider>
                    <n-form-item :label="$t('page.user.settings.account_security.account.email')">
                      <n-input-group>
                        <n-input readonly :value="userStore.currentUser?.email" />
                        <n-button secondary type="primary">
                          {{ $t("page.user.settings.account_security.account.email_verify") }}
                        </n-button>
                      </n-input-group>
                    </n-form-item>
                    <n-form-item
                      :label="$t('page.user.settings.account_security.account.rebuild_folder')"
                    >
                      <n-space vertical size="large" style="width: 100%">
                        <div class="desc">
                          <!-- prettier-ignore -->
                          {{ $t("page.user.settings.account_security.account.rebuild_folder_desc") }}
                        </div>
                        <n-input-group>
                          <n-input v-model:value="rebuildConfirm" placeholder="UUID" />
                          <n-button
                            secondary
                            type="warning"
                            @click="handleRebuildUserDir"
                            :disabled="!rebuildConfirm"
                          >
                            {{ $t("page.user.settings.account_security.account.rebuild") }}
                          </n-button>
                        </n-input-group>
                      </n-space>
                    </n-form-item>
                    <n-form-item
                      :label="$t('page.user.settings.account_security.account.delete_account')"
                    >
                      <n-space vertical size="large" style="width: 100%">
                        <div class="desc">
                          <!-- prettier-ignore -->
                          {{ $t("page.user.settings.account_security.account.delete_account_desc") }}
                        </div>
                        <div style="display: flex; justify-content: flex-end">
                          <n-button secondary disabled type="error">
                            {{ $t("page.user.settings.account_security.account.delete") }}
                          </n-button>
                        </div>
                      </n-space>
                    </n-form-item>
                  </n-form>
                  <n-form
                    ref="passwordFormRef"
                    :model="passwordForm"
                    :rules="passwordRules"
                    label-placement="left"
                    label-width="200"
                  >
                    <n-divider title-placement="left">
                      <span class="divider-title">
                        {{ $t("page.user.settings.account_security.security.title") }}
                      </span>
                    </n-divider>
                    <n-form-item
                      :label="$t('page.user.settings.account_security.security.password')"
                    >
                      <n-space vertical size="large" style="width: 100%">
                        <div class="desc">
                          {{ $t("page.user.settings.account_security.security.password_desc") }}
                        </div>
                        <div>
                          <n-form-item path="oldPassword">
                            <!-- prettier-ignore -->
                            <n-input
                              type="password"
                              v-model:value="passwordForm.oldPassword"
                              :placeholder="$t('page.user.settings.account_security.security.old_password_placeholder')"
                              show-password-on="click"
                            />
                          </n-form-item>
                          <n-form-item path="newPassword">
                            <!-- prettier-ignore -->
                            <n-input
                              type="password"
                              v-model:value="passwordForm.newPassword"
                              :placeholder="$t('page.user.settings.account_security.security.new_password_placeholder')"
                              show-password-on="click"
                            />
                          </n-form-item>
                          <n-form-item path="confirmPassword">
                            <!-- prettier-ignore -->
                            <n-input
                              type="password"
                              v-model:value="passwordForm.confirmPassword"
                              :placeholder="$t('page.user.settings.account_security.security.confirm_password_placeholder')"
                              show-password-on="click"
                            />
                          </n-form-item>
                          <n-form-item path="verifyCode">
                            <n-input-group>
                              <!-- prettier-ignore -->
                              <n-input
                                type="text"
                                v-model:value="passwordForm.verifyCode"
                                :placeholder="$t('page.user.settings.account_security.security.verify_code_placeholder')"
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
                        </div>
                        <div style="display: flex; justify-content: flex-end">
                          <n-space size="small">
                            <n-button tertiary disabled type="primary">
                              <!-- prettier-ignore -->
                              {{ $t("page.user.settings.account_security.security.password_forgot") }}
                            </n-button>
                            <n-button secondary type="primary" @click="handleSavePassword">
                              <!-- prettier-ignore -->
                              {{ $t("page.user.settings.account_security.security.password_update") }}
                            </n-button>
                          </n-space>
                        </div>
                      </n-space>
                    </n-form-item>
                  </n-form>
                  <n-form label-placement="left" label-width="200">
                    <n-form-item :label="$t('page.user.settings.account_security.security.2fa')">
                      <n-space vertical size="large" style="width: 100%">
                        <div class="desc">
                          {{ $t("page.user.settings.account_security.security.2fa_desc") }}
                        </div>
                        <div style="display: flex; justify-content: flex-end">
                          <n-button secondary disabled type="primary">
                            {{ $t("page.user.settings.account_security.security.2fa_enable") }}
                          </n-button>
                        </div>
                      </n-space>
                    </n-form-item>
                  </n-form>
                </n-tab-pane>

                <!-- 个性化与隐私 -->
                <n-tab-pane
                  name="preference_privacy"
                  display-directive="show"
                  :tab="$t('page.user.settings.preference_privacy.title')"
                >
                  <n-form
                    ref="preferenceFormRef"
                    :model="preferenceForm"
                    label-placement="left"
                    label-width="200"
                  >
                    <n-divider title-placement="left">
                      <span class="divider-title">
                        {{ $t("page.user.settings.preference_privacy.preference.theme_settings") }}
                      </span>
                    </n-divider>
                    <n-form-item
                      :label="$t('page.user.settings.preference_privacy.preference.theme')"
                    >
                      <n-select v-model:value="currentTheme" :options="themeOptions" />
                    </n-form-item>
                    <n-form-item
                      :label="$t('page.user.settings.preference_privacy.preference.custom_theme')"
                    >
                      <!-- prettier-ignore -->
                      <n-input
                        type="textarea"
                        :placeholder="
                          $t('page.user.settings.preference_privacy.preference.custom_theme_placeholder')
                        "
                        :autosize="{ minRows: 3 }"
                      />
                    </n-form-item>

                    <n-divider title-placement="left">
                      <span class="divider-title">
                        <!-- prettier-ignore -->
                        {{ $t("page.user.settings.preference_privacy.preference.privacy_settings") }}
                      </span>
                    </n-divider>
                    <n-form-item
                      :label="$t('page.user.settings.preference_privacy.preference.public_profile')"
                    >
                      <n-switch>
                        <template #checked>
                          {{ $t("page.user.settings.common.enabled") }}
                        </template>
                        <template #unchecked>
                          {{ $t("page.user.settings.common.disabled") }}
                        </template>
                      </n-switch>
                    </n-form-item>
                  </n-form>
                </n-tab-pane>
              </n-tabs>
            </n-card>
          </div>
        </div>
      </div>
    </n-space>
  </ScrollContainer>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, reactive, watch } from "vue";
import {
  NForm,
  NFormItem,
  NSelect,
  NTabs,
  NTabPane,
  NCard,
  NAvatar,
  NUpload,
  NInputGroup,
  NButton,
  NInput,
  NDivider,
  NH1,
  NSpace,
  NSwitch,
  FormInst,
  FormRules,
  FormItemRule,
} from "naive-ui";
import { useI18n } from "vue-i18n";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faCamera } from "@fortawesome/free-solid-svg-icons";
import { useThemeStore } from "@/stores/theme";
import { useUserStore } from "@/stores/user";
import { themeOptions } from "@/themes";
import { userService } from "@/services/user";
import { notification } from "@/utils/notification";
import { ScrollContainer } from "@/components/scroll-container";
import { AvatarCropper } from "@/components/avatar-cropper";
import { authService } from "@/services/auth";

const userStore = useUserStore();
const themeStore = useThemeStore();
const { t } = useI18n();

// --------- Personal 个人信息设置 ---------
// Profile (TODO: 增加签名的保存方法)
const avatarUrl = computed(() => {
  if (!userStore.currentUser?.uuid) return "";
  return userService.getAvatarUrl(userStore.currentUser.uuid) + `?t=${userStore.avatarTimestamp}`;
});

const profileForm = reactive({
  username: userStore.currentUser?.username || "",
  bio: userStore.currentUser?.bio || "",
});

const handleAvatarCrop = async (blob: Blob) => {
  try {
    const file = new File([blob], "avatar.png", { type: "image/png" });
    await userService.uploadAvatar(file);
    userStore.refreshAvatar();
  } catch (e: any) {
    console.error(e);
  }
};

const handleSaveProfile = async () => {
  try {
    await userService.updateProfile({
      username: profileForm.username,
    });
    await userStore.checkAuth();
  } catch (e: any) {
    console.error(e);
  }
};

watch(
  () => userStore.currentUser,
  (user) => {
    if (user) {
      profileForm.username = user.username;
    }
  },
  { immediate: true }
);

// URLs (TODO: 增加外链的设置)
const urlForm = reactive({
  urls: userStore.currentUser?.urls || {},
});
// --------- Personal 个人信息设置 ---------

// --------- Account_Security 账户与安全设置 ---------
// Account
const rebuildConfirm = ref("");

const handleRebuildUserDir = async () => {
  if (!userStore.currentUser?.uuid) return;
  if (rebuildConfirm.value !== userStore.currentUser.uuid) {
    notification.error({
      content: "UUID 输入错误",
      duration: 3000,
    });
    return;
  }
  try {
    await userService.rebuildUserDir(userStore.currentUser.uuid);
    rebuildConfirm.value = "";
  } catch (e: any) {
    console.error(e);
  }
};

// Security
const passwordForm = reactive({
  oldPassword: "",
  newPassword: "",
  confirmPassword: "",
  verifyCode: "",
});

const passwordFormRef = ref<FormInst | null>(null);
const countdown = ref(0);

const sendCode = async () => {
  if (countdown.value > 0) return;
  try {
    if (userStore.currentUser?.email) {
      await authService.sendCode(userStore.currentUser.email, "update_password");
      countdown.value = 60;
      const timer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          clearInterval(timer);
        }
      }, 1000);
    }
  } catch (e: any) {
    console.error(e);
  }
};

const passwordRules: FormRules = {
  oldPassword: {
    required: true,
    message: t("page.register.password.validation"),
    trigger: "blur",
  },
  newPassword: {
    required: true,
    message: t("page.register.password.validation"),
    trigger: "blur",
  },
  confirmPassword: [
    {
      required: true,
      message: t("page.register.confirmPassword.validation.confirmPasswordRequired"),
      trigger: "blur",
    },
    {
      validator: (rule: FormItemRule, value: string) => {
        return value === passwordForm.newPassword;
      },
      message: t("page.register.confirmPassword.validation.passwordsDoNotMatch"),
      trigger: ["blur", "password-input"],
    },
  ],
  verifyCode: {
    required: true,
    message: t("page.register.code.validation"),
    trigger: "blur",
  },
};

const handleSavePassword = async (e: MouseEvent) => {
  e.preventDefault();
  // 1. 验证表单
  try {
    await passwordFormRef.value?.validate();
  } catch (errors) {
    return;
  }

  const identifier = userStore.currentUser?.email || userStore.currentUser?.username;
  if (!identifier) return;

  // 2. 向 auth service 验证旧密码是否正确
  try {
    await authService.login(
      {
        identifier,
        password: passwordForm.oldPassword,
      },
      { silent: true }
    );
  } catch (e: any) {
    console.error(e);
    return;
  }

  // 3. 验证验证码
  try {
    await authService.verifyCode(identifier, passwordForm.verifyCode, "update_password");
  } catch (e: any) {
    console.error(e);
    return;
  }

  // 5. 更新密码
  try {
    await userService.updateProfile({
      password: passwordForm.newPassword,
    });
    await userStore.checkAuth();
    notification.success({
      content: "密码修改成功", // 可根据多语言调整
      duration: 2000,
    });
    // 清空表单
    passwordForm.oldPassword = "";
    passwordForm.newPassword = "";
    passwordForm.confirmPassword = "";
    passwordForm.verifyCode = "";
  } catch (e: any) {
    console.error(e);
  }
};
// --------- Account_Security 账户与安全设置 ---------

// --------- 个性化与隐私设置 ---------
// Preferences
const preferenceForm = reactive({
  theme: themeStore.currentTheme,
});

const currentTheme = computed({
  get() {
    return themeStore.currentTheme;
  },
  set(v: string) {
    themeStore.setTheme(v);
  },
});
// Privacy

// --------- 个性化与隐私设置 ---------

// 初始化
onMounted(() => {
  if (!userStore.currentUser) {
    userStore.checkAuth();
  }
});
</script>

<style scoped>
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
</style>
