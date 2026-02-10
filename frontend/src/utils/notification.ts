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
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
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

// 挂载到 window 对象，方便在控制台或其他非 Vue 上下文中使用
(window as any).$notification = notification;

export { notification };
