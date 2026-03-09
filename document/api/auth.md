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
  "message": "用户不存在或密码错误"
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
