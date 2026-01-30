import { request } from "@/utils/request";
import type { ApiResponse } from "@/utils/request";
import type { User } from "@/services/auth";

export const userService = {
  /**
   * Upload user avatar
   * @param file The image file to upload
   */
  async uploadAvatar(
    file: File | Blob,
  ): Promise<{ avatar_url: string; filename: string }> {
    const formData = new FormData();
    formData.append("avatar", file);

    return request<{ avatar_url: string; filename: string }>(
      "/api/user/avatar",
      {
        method: "POST",
        body: formData,
      },
    );
  },

  /**
   * Get avatar URL for a user
   * @param uuid User UUID
   * @param filename Avatar filename (e.g. avatar.png)
   */
  getAvatarUrl(uuid: string, filename: string = "avatar.png"): string {
    return `/api/user/avatar/${uuid}/${filename}`;
  },

  /**
   * Get all users (Admin only)
   */
  async getAll(): Promise<User[]> {
    return request<User[]>("/api/user/list", {
      method: "GET",
    });
  },
};
