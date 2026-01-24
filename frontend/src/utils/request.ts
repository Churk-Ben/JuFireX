import { createDiscreteApi } from "naive-ui";

const { message: messageApi } = createDiscreteApi(["message"]);

export interface ApiResponse<T = any> {
  level?: "info" | "success" | "warning" | "error";
  message?: string;
  data?: T;
  [key: string]: any;
}

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
    
    // Unify frontend API response handling
    if (data && typeof data === "object") {
      const { level, message } = data;
      if (message) {
        switch (level) {
          case "success":
            messageApi.success(message);
            break;
          case "warning":
            messageApi.warning(message);
            break;
          case "error":
            messageApi.error(message);
            break;
          case "info":
            messageApi.info(message);
            break;
          default:
            // If level is missing but message exists, maybe info? 
            // Or if it's an error status, error.
            if (!response.ok) messageApi.error(message);
            else messageApi.info(message);
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

  // Return the data payload if it exists, otherwise return the whole response
  return data.data !== undefined ? data.data : data;
}
