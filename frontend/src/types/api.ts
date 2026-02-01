export interface ApiResponse<T = any> {
  level?: "info" | "success" | "warning" | "error";
  message?: string;
  data?: T;
  [key: string]: any;
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

export interface CreateProjectDto {
  title: string;
  description?: string;
  readme?: string;
  content?: string;
  url?: string;
  icon?: string;
  tags?: string[];
  is_public?: boolean;
  order?: number;
}

export interface UpdateProjectDto extends Partial<CreateProjectDto> {}

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

export interface UserAvatar {
  avatar_url: string;
  filename: string;
}
