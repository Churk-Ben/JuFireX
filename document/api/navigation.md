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
  "icon": "fas:link",
  "category": "Tools",
  "description": "A useful site",
  "is_public": true,
  "order": 1
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
