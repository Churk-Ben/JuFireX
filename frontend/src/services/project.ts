import { request } from "@/utils/request";

export interface Project {
  uuid: string;
  title: string;
  description?: string;
  content?: string;
  url?: string;
  icon?: string;
  tags: string[];
  is_public: boolean;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface CreateProjectDto {
  title: string;
  description?: string;
  content?: string;
  url?: string;
  icon?: string;
  tags?: string[];
  is_public?: boolean;
  order?: number;
}

export interface UpdateProjectDto extends Partial<CreateProjectDto> {}

export const projectService = {
  /**
   * Get all projects
   * @param showAll If true, returns all projects (admin only). If false, returns only public ones.
   */
  async getAll(showAll: boolean = false): Promise<Project[]> {
    return request<Project[]>(`/api/project/?all=${showAll}`);
  },

  /**
   * Get project detail
   */
  async getDetail(uuid: string): Promise<Project> {
      return request<Project>(`/api/project/${uuid}`);
  },

  /**
   * Create a new project
   */
  async create(data: CreateProjectDto): Promise<Project> {
    return request<Project>("/api/project/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an existing project
   */
  async update(uuid: string, data: UpdateProjectDto): Promise<Project> {
    return request<Project>(`/api/project/${uuid}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a project
   */
  async delete(uuid: string): Promise<void> {
    return request<void>(`/api/project/${uuid}`, {
      method: "DELETE",
    });
  },
};
