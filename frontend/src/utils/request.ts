import { createDiscreteApi, darkTheme } from "naive-ui";

// 检查主题模式, 从 localStorage 或系统偏好设置中获取
const themeMode = localStorage.getItem("themeMode");
const isDark =
  themeMode === "dark" ||
  (!themeMode &&
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches);

// 为通知添加亚克力效果 (背景模糊)
const style = document.createElement("style");
style.textContent = `
  .n-notification {
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    min-height: 6rem;
    max-width: 30rem;
  }

  .n-notification-main__content {
    padding-top: 4px;
    font-size: 1rem;
  }
`;
document.head.appendChild(style);

const { notification } = createDiscreteApi(["notification"], {
  configProviderProps: {
    theme: isDark ? darkTheme : undefined,
    themeOverrides: {
      Notification: {
        color: isDark ? "rgba(24, 24, 28, 0.7)" : "rgba(255, 255, 255, 0.7)",
      },
    },
  },
  notificationProviderProps: {
    placement: "bottom-right",
  },
});

export async function request<T = any>(
  url: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers);
  if (!headers.has("Content-Type") && !(options.body instanceof FormData)) {
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
    if (data && typeof data === "object") {
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
