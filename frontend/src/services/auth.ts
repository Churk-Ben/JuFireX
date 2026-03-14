import { request } from "@/utils/request";
import type { User } from "@/types/models";

export const authService = {
  login(data: any) {
    return request<User>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  logout() {
    return request("/api/auth/logout", {
      method: "POST",
    });
  },

  register(data: any) {
    return request<User>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  sendCode(email: string) {
    return request("/api/auth/code/send", {
      method: "POST",
      body: JSON.stringify({
        identifier: email,
        method: "email",
        scene: "register",
      }),
    });
  },

  verifyCode(email: string, code: string) {
    return request("/api/auth/code/verify", {
      method: "POST",
      body: JSON.stringify({
        identifier: email,
        code,
        method: "email",
        scene: "register",
      }),
    });
  },

  getMe() {
    return request<User>("/api/auth/me", {}, { silent: true });
  },
};
