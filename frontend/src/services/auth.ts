import { request } from "@/utils/request";
import type { User } from "@/types/models";

export const authService = {
  getMe() {
    return request<User>("/api/auth/me", {}, { silent: true });
  },

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

  setup2fa() {
    return request<{ uri: string; recovery_codes: string[] }>("/api/auth/2fa/setup", {
      method: "GET",
    });
  },

  check2fa() {
    return request<{ is_enabled: boolean }>("/api/auth/2fa/check", {
      method: "GET",
    });
  },

  enable2fa(code: string) {
    return request("/api/auth/2fa/enable", {
      method: "POST",
      body: JSON.stringify({ code }),
    });
  },

  disable2fa(code: string) {
    return request("/api/auth/2fa/disable", {
      method: "POST",
      body: JSON.stringify({ code }),
    });
  },

  verify2fa(uuid: string, code: string) {
    return request("/api/auth/2fa/verify", {
      method: "POST",
      body: JSON.stringify({
        uuid,
        code,
      }),
    });
  },
};
