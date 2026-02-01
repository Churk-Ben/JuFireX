import { defineStore } from "pinia";
import { ref } from "vue";
import { authService } from "@/services/auth";
import type { User } from "@/types/models";

export const useUserStore = defineStore("user", () => {
  const currentUser = ref<User | null>(null);
  const loading = ref(false);

  async function login(data: any) {
    loading.value = true;
    try {
      const user = await authService.login(data);
      currentUser.value = user;
      return user;
    } finally {
      loading.value = false;
    }
  }

  async function logout() {
    loading.value = true;
    try {
      await authService.logout();
    } finally {
      currentUser.value = null;
      loading.value = false;
    }
  }

  async function checkAuth() {
    loading.value = true;
    try {
      const user = await authService.getMe();
      currentUser.value = user;
    } catch (e) {
      currentUser.value = null;
    } finally {
      loading.value = false;
    }
  }

  return {
    currentUser,
    loading,
    login,
    logout,
    checkAuth,
  };
});
