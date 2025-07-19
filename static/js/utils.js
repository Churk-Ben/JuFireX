// JuFire Studio - 通用工具函数

/**
 * 显示通知消息
 * @param {string} message - 要显示的消息
 * @param {string} type - 通知类型 (success, error, warning, info)
 */
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';

    const alertElement = document.createElement('div');
    alertElement.className = `alert ${alertClass} fade show`;
    alertElement.setAttribute('role', 'alert');
    alertElement.textContent = message;

    const container = document.getElementById('messages');
    if (container) {
        container.appendChild(alertElement);

        setTimeout(() => {
            alertElement.classList.add('show');
        }, 10);

        // 将超时时间从5000ms缩短到3000ms
        setTimeout(() => {
            alertElement.classList.remove('show');
            setTimeout(() => {
                if (alertElement.parentNode) {
                    alertElement.remove();
                }
            }, 300);
        }, 2000);
    }
}

/**
 * API 请求封装
 */
class API {
    static async request(url, options = {}) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
        const defaultOptions = {
            headers: {
                'X-CSRFToken': csrfToken
            },
        };

        // 如果不是 FormData，则添加 Content-Type
        if (!(options.body instanceof FormData)) {
            defaultOptions.headers['Content-Type'] = 'application/json';
        }

        const config = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers,
            },
        };

        const response = await fetch(url, config);

        // 如果响应不成功，抛出响应对象
        if (!response.ok) {
            throw response;
        }

        try {
            return await response.json();
        } catch (error) {
            // 如果响应不是 JSON 格式，返回原始响应
            return response;
        }
    }

    static async get(url) {
        return this.request(url, { method: 'GET' });
    }

    static async post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: data instanceof FormData ? data : JSON.stringify(data)
        });
    }

    static async put(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: data instanceof FormData ? data : JSON.stringify(data)
        });
    }

    static async delete(url) {
        return this.request(url, { method: 'DELETE' });
    }
}