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
    alertElement.className = `alert ${alertClass} alert-dismissible fade show`;
    alertElement.setAttribute('role', 'alert');

    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close custom-close" aria-label="关闭"></button>
    `;

    const closeButton = alertElement.querySelector('.custom-close');
    if (closeButton) {
        closeButton.onclick = function () {
            alertElement.classList.remove('show');
            setTimeout(() => {
                if (alertElement.parentNode) {
                    alertElement.remove();
                }
            }, 300);
            return false;
        };
    }

    const container = document.getElementById('messages');
    if (container) {
        container.appendChild(alertElement);

        setTimeout(() => {
            alertElement.classList.add('show');
        }, 10);

        setTimeout(() => {
            alertElement.classList.remove('show');
            setTimeout(() => {
                if (alertElement.parentNode) {
                    alertElement.remove();
                }
            }, 300);
        }, 5000);
    }
}

/**
 * API 请求封装
 */
class API {
    static async request(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || '请求失败');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    static async get(url) {
        return this.request(url, { method: 'GET' });
    }

    static async post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async put(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async delete(url) {
        return this.request(url, { method: 'DELETE' });
    }
}