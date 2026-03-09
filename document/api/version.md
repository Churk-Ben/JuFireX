## 版本模块 (Version)

**Base URL**: `/api/version`

### 1. 获取后端版本信息

- **URL**: `/`
- **Method**: `GET`
- **Description**: 获取后端当前版本信息。

**Response**:

```json
{
  "level": "success",
  "data": {
    "version": "0.1.0",
    "codename": "Alpha",
    "build_date": "2025-01-01"
  }
}
```
