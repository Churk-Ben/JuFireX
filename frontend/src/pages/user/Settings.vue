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
                <n-tab-pane name="personal" display-directive="show" :tab="$t('page.user.settings.personal.title')">
                  <!-- 档案表单 -->
                  <n-form
                    ref="profileFormRef"
                    :model="profileForm"
                    label-placement="left"
                    label-width="180"
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
                    <n-form-item :label="$t('page.user.settings.personal.profile.username')" path="username" required>
                      <n-input
                        v-model:value="profileForm.username"
                        :placeholder="$t('page.user.settings.personal.profile.username_placeholder')"
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

                  <!-- URL表单 -->
                  <n-form ref="urlFormRef" :model="urlForm" label-placement="left" label-width="180">
                    <n-divider title-placement="left">
                      <span class="divider-title">
                        {{ $t("page.user.settings.personal.urls.title") }}
                      </span>
                    </n-divider>
                    <n-form-item :label="$t('page.user.settings.personal.urls.urls_list')">
                      <n-space vertical size="large" style="width: 100%">
                        <div class="desc">
                          {{ $t("page.user.settings.personal.urls.urls_list_desc") }}
                        </div>
                        <n-dynamic-input
                          path="urls"
                          v-model:value="value"
                          preset="pair"
                          :key-placeholder="$t('page.user.settings.personal.urls.url_name_placeholder')"
                          :value-placeholder="$t('page.user.settings.personal.urls.url_placeholder')"
                        />
                      </n-space>
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
                  <!-- 此账户表单 -->
                  <n-form label-placement="left" label-width="180">
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
                    <n-form-item :label="$t('page.user.settings.account_security.account.rebuild_folder')">
                      <n-space vertical size="large" style="width: 100%">
                        <div class="desc">
                          {{ $t("page.user.settings.account_security.account.rebuild_folder_desc") }}
                        </div>
                        <n-input-group>
                          <n-input v-model:value="rebuildConfirm" placeholder="UUID" />
                          <n-button secondary type="warning" @click="handleRebuildUserDir" :disabled="!rebuildConfirm">
                            {{ $t("page.user.settings.account_security.account.rebuild") }}
                          </n-button>
                        </n-input-group>
                      </n-space>
                    </n-form-item>
                    <n-form-item :label="$t('page.user.settings.account_security.account.delete_account')">
                      <n-space vertical size="large" style="width: 100%">
                        <div class="desc">
                          {{ $t("page.user.settings.account_security.account.delete_account_desc") }}
                        </div>
                        <n-input-group>
                          <n-input v-model:value="deleteConfirm" placeholder="UUID" />
                          <n-button secondary disabled type="error">
                            {{ $t("page.user.settings.account_security.account.delete") }}
                          </n-button>
                        </n-input-group>
                      </n-space>
                    </n-form-item>
                  </n-form>

                  <!-- 修改密码表单 -->
                  <n-form
                    ref="passwordFormRef"
                    :model="passwordForm"
                    :rules="passwordRules"
                    label-placement="left"
                    label-width="180"
                  >
                    <n-divider title-placement="left">
                      <span class="divider-title">
                        {{ $t("page.user.settings.account_security.password.title") }}
                      </span>
                    </n-divider>
                    <n-form-item
                      :label="$t('page.user.settings.account_security.password.old_password')"
                      path="oldPassword"
                    >
                      <n-input
                        type="password"
                        v-model:value="passwordForm.oldPassword"
                        :placeholder="$t('page.user.settings.account_security.password.old_password_placeholder')"
                        show-password-on="click"
                      />
                    </n-form-item>
                    <n-form-item
                      :label="$t('page.user.settings.account_security.password.new_password')"
                      path="newPassword"
                    >
                      <n-space vertical size="large" style="width: 100%">
                        <div class="desc">
                          {{ $t("page.user.settings.account_security.password.new_password_desc") }}
                        </div>
                        <n-input
                          type="password"
                          v-model:value="passwordForm.newPassword"
                          :placeholder="$t('page.user.settings.account_security.password.new_password_placeholder')"
                          show-password-on="click"
                        />
                      </n-space>
                    </n-form-item>
                    <n-form-item
                      :label="$t('page.user.settings.account_security.password.confirm_password')"
                      path="confirmPassword"
                    >
                      <n-input
                        type="password"
                        v-model:value="passwordForm.confirmPassword"
                        :placeholder="$t('page.user.settings.account_security.password.confirm_password_placeholder')"
                        show-password-on="click"
                      />
                    </n-form-item>
                    <n-form-item
                      :label="$t('page.user.settings.account_security.password.verify_code')"
                      path="verifyCode"
                    >
                      <n-input-group>
                        <n-input
                          type="text"
                          v-model:value="passwordForm.verifyCode"
                          :placeholder="$t('page.user.settings.account_security.password.verify_code_placeholder')"
                        />
                        <n-button
                          type="primary"
                          secondary
                          :disabled="
                            countdown > 0 ||
                            !passwordForm.oldPassword ||
                            !passwordForm.newPassword ||
                            !passwordForm.confirmPassword ||
                            passwordForm.newPassword !== passwordForm.confirmPassword
                          "
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
                    <n-form-item style="display: flex; justify-content: flex-end">
                      <n-space size="small">
                        <n-button secondary type="primary">
                          {{ $t("page.user.settings.account_security.password.password_forgot") }}
                        </n-button>
                        <n-button type="primary" @click="handleSavePassword">
                          {{ $t("page.user.settings.account_security.password.password_update") }}
                        </n-button>
                      </n-space>
                    </n-form-item>
                  </n-form>

                  <!-- 2FA表单 -->
                  <n-form label-placement="left" label-width="180">
                    <n-divider title-placement="left">
                      <span class="divider-title">
                        {{ $t("page.user.settings.account_security.2fa.title") }}
                      </span>
                    </n-divider>
                    <n-form-item :label="$t('page.user.settings.account_security.2fa.2fa_enable')">
                      <n-space vertical size="large" style="width: 100%">
                        <div class="desc">
                          {{ $t("page.user.settings.account_security.2fa.2fa_enable_desc") }}
                        </div>
                        <div style="display: flex; justify-content: flex-end">
                          <n-button type="primary" @click="handleBtn2fa">
                            {{
                              isMfaEnabled
                                ? $t("page.user.settings.account_security.2fa.modify")
                                : $t("page.user.settings.account_security.2fa.enable")
                            }}
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
                  <!-- 主题设置表单 -->
                  <n-form ref="preferenceFormRef" :model="preferenceForm" label-placement="left" label-width="180">
                    <n-divider title-placement="left">
                      <span class="divider-title">
                        {{ $t("page.user.settings.preference_privacy.preference.title") }}
                      </span>
                    </n-divider>
                    <n-form-item :label="$t('page.user.settings.preference_privacy.preference.theme')">
                      <n-select v-model:value="currentTheme" :options="themeOptions" />
                    </n-form-item>
                    <n-form-item :label="$t('page.user.settings.preference_privacy.preference.custom_theme')">
                      <n-space vertical size="large" style="width: 100%">
                        <div class="desc">
                          {{ $t("page.user.settings.preference_privacy.preference.custom_theme_desc") }}
                        </div>
                        <n-input
                          type="textarea"
                          :placeholder="$t('page.user.settings.preference_privacy.preference.custom_theme_placeholder')"
                          :autosize="{ minRows: 3 }"
                        />
                      </n-space>
                    </n-form-item>
                  </n-form>

                  <!-- 隐私设置表单 -->
                  <n-form ref="preferenceFormRef" :model="preferenceForm" label-placement="left" label-width="180">
                    <n-divider title-placement="left">
                      <span class="divider-title">
                        {{ $t("page.user.settings.preference_privacy.privacy.title") }}
                      </span>
                    </n-divider>
                    <n-form-item :label="$t('page.user.settings.preference_privacy.privacy.public_profile')">
                      <n-switch />
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
  NDynamicInput,
  NDivider,
  NH1,
  NSpace,
  NSwitch,
  FormInst,
  FormRules,
  FormItemRule,
} from "naive-ui";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
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
const router = useRouter();
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

const value = ref([
  {
    key: "",
    value: "",
  },
]);

// --------- Personal 个人信息设置 ---------

// --------- Account_Security 账户与安全设置 ---------
// Account
const rebuildConfirm = ref("");
const deleteConfirm = ref("");

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

const handleDeleteUser = async () => {};

// Security
const passwordForm = reactive({
  oldPassword: "",
  newPassword: "",
  confirmPassword: "",
  verifyCode: "",
});

const passwordFormRef = ref<FormInst | null>(null);
const countdown = ref(0);
const isMfaEnabled = ref(false);

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

const sendCode = async () => {
  if (countdown.value > 0) return;

  const identifier = userStore.currentUser?.email || userStore.currentUser?.username;
  if (!identifier) return;

  // 1. 发送验证码前，先验证旧密码是否正确
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
    notification.error({
      content: "旧密码错误",
      duration: 3000,
    });
    return;
  }

  // 2. 验证成功后发送验证码
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

  // 2. 验证验证码 (旧密码已经在发送验证码前验证过)
  try {
    await authService.verifyCode(identifier, passwordForm.verifyCode, "update_password");
  } catch (e: any) {
    console.error(e);
    return;
  }

  // 3. 更新密码
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

const handleBtn2fa = () => {
  router.push("/user/settings/mfa");
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

const initMfaStatus = async () => {
  try {
    const res = await authService.check2fa();
    isMfaEnabled.value = res.is_enabled;
  } catch (e: any) {
    console.error(e);
  }
};

// 初始化
onMounted(() => {
  if (!userStore.currentUser) {
    userStore.checkAuth();
  }
  initMfaStatus();
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
