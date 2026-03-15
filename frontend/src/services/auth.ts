import { request } from "@/utils/request";
import type { User } from "@/types/models";

export const authService = {
  login(data: any, config?: { silent?: boolean }) {
    return request<User>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }, config);
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

  sendCode(email: string, scene: string = "register") {
    return request("/api/auth/code/send", {
      method: "POST",
      body: JSON.stringify({
        identifier: email,
        method: "email",
        scene: scene,
      }),
    });
  },

  verifyCode(email: string, code: string, scene: string = "register") {
    return request("/api/auth/code/verify", {
      method: "POST",
      body: JSON.stringify({
        identifier: email,
        code,
        method: "email",
        scene,
      }),
    });
  },

  getMe() {
    return request<User>("/api/auth/me", {}, { silent: true });
  },
};
