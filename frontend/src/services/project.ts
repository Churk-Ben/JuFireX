import { request } from "@/utils/request";
import type { Project } from "@/types/models";
import type { CreateProjectDto, UpdateProjectDto } from "@/types/api";

export const projectService = {
  async getAll(showAll: boolean = false): Promise<Project[]> {
    return request<Project[]>(`/api/project/?all=${showAll}`);
  },

  async getDetail(uuid: string): Promise<Project> {
    return request<Project>(`/api/project/${uuid}`);
  },

  async create(data: CreateProjectDto): Promise<Project> {
    return request<Project>("/api/project/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  async update(uuid: string, data: UpdateProjectDto): Promise<Project> {
    return request<Project>(`/api/project/${uuid}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  async delete(uuid: string): Promise<void> {
    return request<void>(`/api/project/${uuid}`, {
      method: "DELETE",
    });
  },
};
