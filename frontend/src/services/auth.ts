import { request } from "@/utils/request";

export interface User {
  id: number;
  uuid: string;
  username: string;
  email: string;
  role: number;
  role_name?: string;
  avatar_path?: string;
  is_active: boolean;
  created_at?: string;
}

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

  getMe() {
    return request<User>("/api/auth/me");
  },
};
