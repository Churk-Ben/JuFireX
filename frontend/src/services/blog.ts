import { request } from "@/utils/request";

export interface Blog {
  uuid: string;
  title: string;
  summary?: string;
  content?: string;
  cover_image?: string;
  tags: string[];
  is_public: boolean;
  views: number;
  author_name?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateBlogDto {
  title: string;
  summary?: string;
  content?: string;
  cover_image?: string;
  tags?: string[];
  is_public?: boolean;
  author_name?: string;
}

export interface UpdateBlogDto extends Partial<CreateBlogDto> {}

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
