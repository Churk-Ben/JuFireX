# 后端 API 文档

本文档详细描述了 JuFireX 后端提供的 API 接口。

## 目录

1. [通用说明](#通用说明)
2. [认证模块 (Auth)](#认证模块-auth)
3. [博客模块 (Blog)](#博客模块-blog)
4. [导航模块 (Navigation)](#导航模块-navigation)
5. [项目模块 (Project)](#项目模块-project)
6. [用户模块 (User)](#用户模块-user)

---

## 通用说明

### 响应格式

所有 API 接口遵循统一的 JSON 响应格式：

```json
{
  "level": "success" | "warning" | "error" | "info",
  "message": "操作结果描述",
  "data": { ... } // 可选，成功时返回的数据
}
```

- **level**: 消息级别，前端根据此级别显示不同的通知样式。
- **message**: 提示消息内容。
- **data**: 具体的业务数据负载。

---

## 认证模块 (Auth)

**Base URL**: `/api/auth`

### 1. 用户登录

- **URL**: `/login`
- **Method**: `POST`
- **Description**: 用户登录接口，支持 ID, 邮箱或 UUID 登录。

**Request Body**:

```json
{
  "identifier": "user@example.com", // ID, 邮箱或 UUID
  "password": "your_password"
}
```

**Response (Success)**:

```json
{
  "level": "success",
  "message": "登录成功",
  "data": {
    "id": 1,
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "username": "admin",
    "email": "admin@example.com",
    "role": 99,
    "role_name": "Super Admin",
    ...
  }
}
```

**Response (Error)**:

```json
{
  "level": "error",
  "message": "用户名或密码错误"
}
```

### 2. 用户注册

- **URL**: `/register`
- **Method**: `POST`
- **Description**: 新用户注册。

**Request Body**:

```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "secure_password"
}
```

**Response (Success)**:

```json
{
  "level": "success",
  "message": "注册成功",
  "data": { ... } // 用户对象
}
```

### 3. 用户注销

- **URL**: `/logout`
- **Method**: `POST`
- **Description**: 注销当前登录状态。

**Response**:

```json
{
  "level": "success",
  "message": "白白~"
}
```

### 4. 获取当前用户信息

- **URL**: `/me`
- **Method**: `GET`
- **Description**: 获取当前登录用户的详细信息。需要登录。

**Response**:

```json
{
  "level": "success",
  "message": "获取用户信息成功",
  "data": {
    "uuid": "...",
    "username": "...",
    "email": "...",
    ...
  }
}
```

---

## 博客模块 (Blog)

**Base URL**: `/api/blog`

### 1. 获取博客列表

- **URL**: `/`
- **Method**: `GET`
- **Query Params**:
  - `all`: `true` | `false` (可选，默认 `false`)。管理员传递 `true` 可查看所有博客（包括私有）。
- **Description**: 获取博客文章列表。普通用户只能看到公开的和自己的文章。

**Response**:

```json
{
  "level": "success",
  "data": [
    {
      "uuid": "...",
      "title": "Blog Title",
      "owner_uuid": "...",
      "is_public": true,
      ...
    }
  ]
}
```

### 2. 获取博客详情

- **URL**: `/<uuid>`
- **Method**: `GET`
- **Description**: 获取指定 UUID 的博客详情。会自动增加浏览量。

**Response**:

```json
{
  "level": "success",
  "data": {
    "uuid": "...",
    "title": "Blog Title",
    "content": "Markdown Content...",
    "views": 10,
    ...
  }
}
```

### 3. 创建博客

- **URL**: `/`
- **Method**: `POST`
- **Description**: 创建新的博客文章。需要成员权限。

**Request Body**:

```json
{
  "title": "My New Blog",
  "content": "This is content...",
  "is_public": true,
  "tags": ["tech", "life"]
}
```

**Response**:

```json
{
  "level": "success",
  "message": "创建成功",
  "data": { ... } // 创建后的博客对象
}
```

### 4. 更新博客

- **URL**: `/<uuid>`
- **Method**: `PUT`
- **Description**: 更新博客文章。需要所有者或管理员权限。

**Request Body**:

```json
{
  "title": "Updated Title",
  "content": "Updated content..."
}
```

**Response**:

```json
{
  "level": "success",
  "message": "更新成功",
  "data": { ... }
}
```

### 5. 删除博客

- **URL**: `/<uuid>`
- **Method**: `DELETE`
- **Description**: 删除博客文章。需要所有者或管理员权限。

**Response**:

```json
{
  "level": "success",
  "message": "删除成功"
}
```

---

## 导航模块 (Navigation)

**Base URL**: `/api/navigation`

### 1. 获取导航分类

- **URL**: `/categories`
- **Method**: `GET`
- **Description**: 获取所有可用的导航分类列表。

**Response**:

```json
{
  "level": "success",
  "data": ["Technology", "Design", "Tools", ...]
}
```

### 2. 获取导航列表

- **URL**: `/`
- **Method**: `GET`
- **Query Params**:
  - `all`: `true` | `false` (可选)。管理员查看所有。
- **Description**: 获取导航链接列表。

**Response**:

```json
{
  "level": "success",
  "data": [
    {
      "uuid": "...",
      "title": "Google",
      "url": "https://google.com",
      "category": "Tools",
      ...
    }
  ]
}
```

### 3. 创建导航

- **URL**: `/`
- **Method**: `POST`
- **Description**: 创建新的导航项。需要成员权限。

**Request Body**:

```json
{
  "title": "New Site",
  "url": "https://example.com",
  "category": "Tools",
  "description": "A useful site",
  "is_public": true
}
```

**Response**:

```json
{
  "level": "success",
  "message": "导航创建成功",
  "data": { ... }
}
```

### 4. 更新导航

- **URL**: `/<uuid>`
- **Method**: `PUT`
- **Description**: 更新导航项。需要所有者或管理员权限。

**Request Body**:

```json
{
  "title": "Updated Site Name",
  "url": "https://updated-url.com"
}
```

**Response**:

```json
{
  "level": "success",
  "message": "导航更新成功",
  "data": { ... }
}
```

### 5. 删除导航

- **URL**: `/<uuid>`
- **Method**: `DELETE`
- **Description**: 删除导航项。需要所有者或管理员权限。

**Response**:

```json
{
  "level": "success",
  "message": "导航删除成功"
}
```

---

## 项目模块 (Project)

**Base URL**: `/api/project`

### 1. 获取项目列表

- **URL**: `/`
- **Method**: `GET`
- **Query Params**:
  - `all`: `true` | `false` (可选)。
- **Description**: 获取项目列表。

**Response**:

```json
{
  "level": "success",
  "data": [
    {
      "uuid": "...",
      "title": "Project Alpha",
      "description": "...",
      "is_public": true,
      ...
    }
  ]
}
```

### 2. 获取项目详情

- **URL**: `/<uuid>`
- **Method**: `GET`
- **Description**: 获取项目概览信息。

**Response**:

```json
{
  "level": "success",
  "data": {
    "uuid": "...",
    "title": "Project Alpha",
    "readme": "# README content...",
    "metadata": { ... }
  }
}
```

### 3. 获取项目文件树

- **URL**: `/<uuid>/files`
- **Method**: `GET`
- **Query Params**:
  - `path`: 相对路径 (可选，默认为根目录)。
- **Description**: 获取项目指定目录下的文件列表。

**Response**:

```json
{
  "level": "success",
  "data": [
    {
      "name": "src",
      "type": "directory",
      "path": "src",
      "size": 0
    },
    {
      "name": "main.py",
      "type": "file",
      "path": "main.py",
      "size": 1024
    }
  ]
}
```

### 4. 获取文件内容

- **URL**: `/<uuid>/file`
- **Method**: `GET`
- **Query Params**:
  - `path`: 文件相对路径 (必须)。
- **Description**: 获取项目内指定文件的内容。

**Response**:

```json
{
  "level": "success",
  "data": "File content string..."
}
```

**Error Responses**:

- 404: 路径或文件不存在
- 403: 权限不足
- 400: 文件过大或无法读取 (二进制文件)

### 5. 创建项目

- **URL**: `/`
- **Method**: `POST`
- **Description**: 创建新项目。

**Request Body**:

```json
{
  "title": "New Project",
  "description": "Project description",
  "is_public": false
}
```

**Response**:

```json
{
  "level": "success",
  "message": "项目创建成功",
  "data": { ... }
}
```

### 6. 更新项目

- **URL**: `/<uuid>`
- **Method**: `PUT`
- **Description**: 更新项目元数据。

**Request Body**:

```json
{
  "title": "New Title",
  "description": "New Description"
}
```

**Response**:

```json
{
  "level": "success",
  "message": "项目更新成功",
  "data": { ... }
}
```

### 7. 删除项目

- **URL**: `/<uuid>`
- **Method**: `DELETE`
- **Description**: 删除项目。

**Response**:

```json
{
  "level": "success",
  "message": "项目删除成功"
}
```

---

## 用户模块 (User)

**Base URL**: `/api/user`

### 1. 获取所有用户列表

- **URL**: `/list`
- **Method**: `GET`
- **Description**: 获取系统中所有用户。需要超级管理员权限。

**Response**:

```json
{
  "level": "success",
  "data": [
    {
      "uuid": "...",
      "username": "user1",
      "role_name": "Member",
      ...
    }
  ]
}
```

### 2. 上传头像

- **URL**: `/avatar`
- **Method**: `POST`
- **Description**: 上传并更新当前用户的头像。需要登录。

**Request Body**:

- `avatar`: 文件对象 (multipart/form-data)

**Response**:

```json
{
  "level": "success",
  "message": "头像上传成功",
  "data": {
    "avatar_url": "/api/user/avatar/uuid/filename.jpg",
    "filename": "filename.jpg"
  }
}
```

### 3. 获取头像文件

- **URL**: `/avatar/<uuid>/<filename>`
- **Method**: `GET`
- **Description**: 获取指定用户的头像图片文件。

**Response**: 图片流

### 4. 重建用户目录

- **URL**: `/rebuild/<uuid>`
- **Method**: `POST`
- **Description**: 重建用户的存储目录结构（备份旧数据）。需要本人或超级管理员权限。

**Request Body**:

```json
{
  "uuid": "target_user_uuid"
}
```

**Response**:

```json
{
  "level": "success",
  "message": "用户目录重建成功"
}
```
