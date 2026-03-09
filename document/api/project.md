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
- **Description**: 创建新项目。需要管理员权限。

**Request Body**:

```json
{
  "title": "New Project",
  "description": "Project description",
  "readme": "# README content...",
  "url": "https://example.com",
  "icon": "fas:code",
  "tags": ["python", "web"],
  "is_public": false,
  "order": 1
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
