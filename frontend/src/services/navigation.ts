import { request } from "@/utils/request";

export interface Navigation {
  uuid: string;
  title: string;
  url: string;
  icon?: string;
  description?: string;
  category?: string;
  is_public: boolean;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface CreateNavigationDto {
  title: string;
  url: string;
  icon?: string;
  description?: string;
  category?: string;
  is_public?: boolean;
  order?: number;
}

export interface UpdateNavigationDto extends Partial<CreateNavigationDto> {}

export const navigationService = {
  /**
   * Get all navigations
   * @param showAll If true, returns all navigations (admin only). If false, returns only public ones.
   */
  async getAll(showAll: boolean = false): Promise<Navigation[]> {
    return request<Navigation[]>(`/api/navigation/?all=${showAll}`);
  },

  /**
   * Create a new navigation
   */
  async create(data: CreateNavigationDto): Promise<Navigation> {
    return request<Navigation>("/api/navigation/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an existing navigation
   */
  async update(uuid: string, data: UpdateNavigationDto): Promise<Navigation> {
    return request<Navigation>(`/api/navigation/${uuid}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a navigation
   */
  async delete(uuid: string): Promise<void> {
    return request<void>(`/api/navigation/${uuid}`, {
      method: "DELETE",
    });
  },
};
