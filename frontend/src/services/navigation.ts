import { request } from "@/utils/request";
import type { Navigation } from "@/types/models";
import type { CreateNavigationDto, UpdateNavigationDto } from "@/types/api";

export const navigationService = {
  async getAll(showAll: boolean = false): Promise<Navigation[]> {
    return request<Navigation[]>(`/api/navigation/?all=${showAll}`);
  },

  async create(data: CreateNavigationDto): Promise<Navigation> {
    return request<Navigation>("/api/navigation/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  async update(uuid: string, data: UpdateNavigationDto): Promise<Navigation> {
    return request<Navigation>(`/api/navigation/${uuid}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  async delete(uuid: string): Promise<void> {
    return request<void>(`/api/navigation/${uuid}`, {
      method: "DELETE",
    });
  },
};
