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
  "message": "文章创建成功",
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
  "message": "文章更新成功",
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
  "message": "文章删除成功"
}
```
