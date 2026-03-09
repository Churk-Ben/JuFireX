## 用户模块 (User)

**Base URL**: `/api/user`

### 1. 获取所有用户列表

- **URL**: `/list`
- **Method**: `GET`
- **Description**: 获取系统中所有用户。需要管理员权限。

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

### 2. 获取指定用户信息

- **URL**: `/<uuid>`
- **Method**: `GET`
- **Description**: 获取指定用户的公开信息。

**Response**:

```json
{
  "level": "success",
  "data": {
    "uuid": "...",
    "username": "user1",
    "role": 1,
    "role_name": "成员",
    "is_active": true,
    "created_at": "2025-01-01T12:00:00Z"
  }
}
```

### 3. 上传头像

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

### 4. 获取头像文件

- **URL**: `/avatar/<uuid>/<filename>`
- **Method**: `GET`
- **Description**: 获取指定用户的头像图片文件。

**Response**: 图片流

### 5. 重建用户目录

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
