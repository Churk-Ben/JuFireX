<template>
  <div class="container p-4">
    <n-card :title="t('page.user.settings.title')">
      <n-tabs type="line" animated>
        <!-- 个人信息设置 -->
        <n-tab-pane name="profile" :tab="t('page.user.settings.profile.title')">
          <n-form
            ref="profileFormRef"
            :model="profileForm"
            label-placement="left"
            label-width="120"
            require-mark-placement="right-hanging"
          >
            <n-form-item :label="t('page.user.settings.profile.avatar')">
              <div class="d-flex align-items-center gap-3">
                <n-avatar round :size="80" :src="avatarUrl" />
                <n-upload
                  action="/api/user/avatar"
                  :show-file-list="false"
                  @finish="handleAvatarFinish"
                >
                  <n-button>{{
                    t("page.user.settings.profile.upload_avatar")
                  }}</n-button>
                </n-upload>
              </div>
            </n-form-item>
            <n-form-item
              :label="t('page.user.settings.profile.username')"
              path="username"
            >
              <n-input
                v-model:value="profileForm.username"
                :placeholder="
                  t('page.user.settings.profile.username_placeholder')
                "
              />
            </n-form-item>
            <n-form-item>
              <n-button type="primary" @click="handleSaveProfile">
                {{ t("page.user.settings.common.save") }}
              </n-button>
            </n-form-item>
          </n-form>
        </n-tab-pane>

        <!-- 账户安全设置 -->
        <n-tab-pane name="account" :tab="t('page.user.settings.account.title')">
          <n-list>
            <n-list-item>
              <template #prefix>
                <n-icon>
                  <FontAwesomeIcon :icon="faEnvelope" />
                </n-icon>
              </template>
              <n-thing
                :title="t('page.user.settings.account.email')"
                :description="userStore.currentUser?.email"
              >
              </n-thing>
              <template #suffix>
                <n-button secondary type="primary">
                  {{ t("page.user.settings.account.verify_email") }}
                </n-button>
              </template>
            </n-list-item>
            <n-list-item>
              <template #prefix>
                <n-icon>
                  <FontAwesomeIcon :icon="faKey" />
                </n-icon>
              </template>
              <n-thing
                :title="t('page.user.settings.account.password')"
                :description="t('page.user.settings.account.password_desc')"
              >
              </n-thing>
              <template #suffix>
                <n-button secondary>
                  {{ t("page.user.settings.account.change_password") }}
                </n-button>
              </template>
            </n-list-item>
            <n-list-item>
              <template #prefix>
                <n-icon>
                  <FontAwesomeIcon :icon="faFolderOpen" />
                </n-icon>
              </template>
              <n-thing
                :title="t('page.user.settings.account.rebuild_folder')"
                :description="
                  t('page.user.settings.account.rebuild_folder_desc')
                "
              >
              </n-thing>
              <template #suffix>
                <n-button secondary type="warning">
                  {{ t("page.user.settings.account.rebuild") }}
                </n-button>
              </template>
            </n-list-item>
            <n-list-item>
              <template #prefix>
                <n-icon>
                  <FontAwesomeIcon :icon="faTrash" />
                </n-icon>
              </template>
              <n-thing
                :title="t('page.user.settings.account.delete_account')"
                :description="
                  t('page.user.settings.account.delete_account_desc')
                "
              >
              </n-thing>
              <template #suffix>
                <n-button secondary type="error">
                  {{ t("page.user.settings.account.delete") }}
                </n-button>
              </template>
            </n-list-item>
          </n-list>
        </n-tab-pane>

        <!-- 个性化与隐私 -->
        <n-tab-pane
          name="preference"
          :tab="t('page.user.settings.preference.title')"
        >
          <n-form label-placement="left" label-width="auto">
            <n-divider title-placement="left">{{
              t("page.user.settings.preference.theme_settings")
            }}</n-divider>
            <n-form-item :label="t('page.user.settings.preference.theme')">
              <n-select v-model:value="currentTheme" :options="themeOptions" />
            </n-form-item>
            <n-form-item
              :label="t('page.user.settings.preference.custom_theme')"
            >
              <n-input
                type="textarea"
                :placeholder="
                  t('page.user.settings.preference.custom_theme_placeholder')
                "
                :autosize="{ minRows: 3 }"
              />
            </n-form-item>

            <n-divider title-placement="left">{{
              t("page.user.settings.preference.privacy_settings")
            }}</n-divider>
            <n-form-item
              :label="t('page.user.settings.preference.public_profile')"
            >
              <n-switch>
                <template #checked>
                  {{ t("page.user.settings.common.enabled") }}
                </template>
                <template #unchecked>
                  {{ t("page.user.settings.common.disabled") }}
                </template>
              </n-switch>
            </n-form-item>
          </n-form>
        </n-tab-pane>
      </n-tabs>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, reactive, watch } from "vue";
import { useI18n } from "vue-i18n";
import {
  NForm,
  NFormItem,
  NSelect,
  NTabs,
  NTabPane,
  NCard,
  NAvatar,
  NUpload,
  NButton,
  NInput,
  NList,
  NListItem,
  NThing,
  NIcon,
  NDivider,
  NSwitch,
} from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faEnvelope,
  faKey,
  faFolderOpen,
  faTrash,
} from "@fortawesome/free-solid-svg-icons";
import { useThemeStore } from "@/stores/theme";
import { useUserStore } from "@/stores/user";
import { themeOptions } from "@/themes";
import { userService } from "@/services/user";
import { notification } from "@/utils/notification";

const { t } = useI18n();
const themeStore = useThemeStore();
const userStore = useUserStore();

// Theme
const currentTheme = computed({
  get() {
    return themeStore.currentTheme;
  },
  set(v: string) {
    themeStore.setTheme(v);
  },
});

// Profile
const profileForm = reactive({
  username: userStore.currentUser?.username || "",
});

watch(
  () => userStore.currentUser,
  (user) => {
    if (user) {
      profileForm.username = user.username;
    }
  },
  { immediate: true }
);

const avatarUrl = computed(() => {
  if (userStore.currentUser) {
    return (
      userService.getAvatarUrl(userStore.currentUser.uuid) +
      `?t=${userStore.avatarTimestamp}`
    );
  }
  return "";
});

const handleAvatarFinish = () => {
  userStore.refreshAvatar();
  notification.success({
    content: t("page.user.settings.notification.avatar_updated"),
    duration: 2000,
  });
};

const handleSaveProfile = async () => {
  try {
    await userService.updateProfile({
      username: profileForm.username,
    });
    await userStore.checkAuth();
  } catch (e) {
    console.error(e);
  }
};
</script>
