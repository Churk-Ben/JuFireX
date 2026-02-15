import { notification } from "./notification";

export async function request<T = any>(
  url: string,
  options: RequestInit = {},
  config: { silent?: boolean } = {},
): Promise<T> {
  const headers = new Headers(options.headers);
  const method = (options.method || "GET").toUpperCase();
  const body = options.body;
  const hasBody = body !== undefined && body !== null;

  const isFormData =
    typeof FormData !== "undefined" && body instanceof FormData;
  const isURLSearchParams =
    typeof URLSearchParams !== "undefined" && body instanceof URLSearchParams;
  const isBlob = typeof Blob !== "undefined" && body instanceof Blob;
  const isStream =
    typeof ReadableStream !== "undefined" && body instanceof ReadableStream;

  const shouldSetJSON =
    hasBody &&
    method !== "GET" &&
    method !== "HEAD" &&
    !isFormData &&
    !isURLSearchParams &&
    !isBlob &&
    !isStream &&
    !headers.has("Content-Type");

  if (shouldSetJSON) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  const contentType = response.headers.get("content-type");
  let data: any;

  if (contentType && contentType.includes("application/json")) {
    data = await response.json();

    // 统一处理 API 响应
    if (data && typeof data === "object" && !config.silent) {
      const { level, message } = data;
      if (message) {
        switch (level) {
          case "success":
            notification.success({
              content: message,
              duration: 2000,
              keepAliveOnHover: true,
            });
            break;
          case "warning":
            notification.warning({
              content: message,
              duration: 3000,
              keepAliveOnHover: true,
            });
            break;
          case "error":
            notification.error({
              content: message,
              duration: 4000,
              keepAliveOnHover: true,
            });
            break;
          case "info":
            notification.info({
              content: message,
              duration: 2000,
              keepAliveOnHover: true,
            });
            break;
          default:
            // 如果 level 缺失但 message 存在, 默认为 info 通知
            notification.info({
              content: message,
              duration: 2000,
              keepAliveOnHover: true,
            });
            break;
        }
      }
    }
  } else {
    data = await response.text();
  }

  if (!response.ok) {
    const error = new Error(data.message || data.error || response.statusText);
    (error as any).response = response;
    (error as any).data = data;
    throw error;
  }

  // 如果 data 存在 data 字段, 返回 data.data, 否则返回 data
  return data.data !== undefined ? data.data : data;
}
