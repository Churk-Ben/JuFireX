# 后端 API 文档

本文档详细描述了 JuFireX 后端提供的 API 接口。

## 模块列表

- [认证模块 (Auth)](./auth.md)
- [博客模块 (Blog)](./blog.md)
- [导航模块 (Navigation)](./navigation.md)
- [项目模块 (Project)](./project.md)
- [用户模块 (User)](./user.md)
- [版本模块 (Version)](./version.md)

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
