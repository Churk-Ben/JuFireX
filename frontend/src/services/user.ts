import { request } from "@/utils/request";
import type { User } from "@/types/models";
import type { UserAvatar } from "@/types/api";

export const userService = {
  getAvatarUrl(uuid: string, filename: string = "avatar.png"): string {
    return `/api/user/avatar/${uuid}/${filename}`;
  },

  async getAll(): Promise<User[]> {
    return request<User[]>("/api/user/list");
  },

  async uploadAvatar(file: File | Blob): Promise<UserAvatar> {
    const formData = new FormData();
    formData.append("avatar", file);

    return request<UserAvatar>("/api/user/avatar", {
      method: "POST",
      body: formData,
    });
  },
};
