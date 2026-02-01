export interface User {
  id: number;
  uuid: string;
  username: string;
  email: string;
  role: number;
  role_name?: string;
  is_active: boolean;
  created_at?: string;
}

export interface Blog {
  uuid: string;
  owner_uuid?: string;
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

export interface Project {
  uuid: string;
  owner_uuid?: string;
  title: string;
  description?: string;
  readme?: string;
  url?: string;
  icon?: string;
  tags: string[];
  is_public: boolean;
  order: number;
  views: number;
  stars: number;
  created_at: string;
  updated_at: string;
}

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
