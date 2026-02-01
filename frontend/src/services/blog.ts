import { request } from "@/utils/request";
import type { Blog } from "@/types/models";
import type { CreateBlogDto, UpdateBlogDto } from "@/types/api";

export const blogService = {
  async getAll(showAll: boolean = false): Promise<Blog[]> {
    return request<Blog[]>(`/api/blog/?all=${showAll}`);
  },

  async getDetail(uuid: string): Promise<Blog> {
    return request<Blog>(`/api/blog/${uuid}`);
  },

  async create(data: CreateBlogDto): Promise<Blog> {
    return request<Blog>("/api/blog/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  async update(uuid: string, data: UpdateBlogDto): Promise<Blog> {
    return request<Blog>(`/api/blog/${uuid}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  async delete(uuid: string): Promise<void> {
    return request<void>(`/api/blog/${uuid}`, {
      method: "DELETE",
    });
  },
};
