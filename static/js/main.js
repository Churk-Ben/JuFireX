// JuFire Studio 主要 JavaScript 文件

// 全局变量
let socket;

// 初始化 Socket.IO
function initSocket() {
    if (typeof io === 'undefined') {
        console.error('Socket.IO library not found.');
        return;
    }

    if (socket && socket.connected) {
        return;
    }

    socket = io();

    socket.on('connect', function () {
        console.log('Connected to server');
    });

    socket.on('disconnect', function () {
        console.log('Disconnected from server');
    });

    socket.on('notification', function (data) {
        showNotification(data.message, data.type || 'info');
    });
}

// 显示通知
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';

    // 创建通知元素
    const alertElement = document.createElement('div');
    alertElement.className = `alert ${alertClass} alert-dismissible fade show`;
    alertElement.setAttribute('role', 'alert');

    // 设置通知内容
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close custom-close" aria-label="关闭"></button>
    `;

    // 确保关闭按钮在DOM中完全渲染
    const closeButton = alertElement.querySelector('.custom-close');
    if (closeButton) {
        // 直接在这里绑定事件，确保绑定成功
        closeButton.onclick = function () {
            alertElement.classList.remove('show');
            setTimeout(() => {
                if (alertElement.parentNode) {
                    alertElement.remove();
                }
            }, 300);
            return false; // 阻止事件冒泡
        };
    }

    // 添加到容器
    const container = document.getElementById('messages');
    if (container) {
        container.appendChild(alertElement);

        // 添加进入动画
        setTimeout(() => {
            alertElement.classList.add('show');
        }, 10);

        // 自动隐藏通知
        setTimeout(() => {
            // 添加淡出动画
            alertElement.classList.remove('show');

            // 移除元素
            setTimeout(() => {
                if (alertElement.parentNode) {
                    alertElement.remove();
                }
            }, 300);
        }, 5000);
    }
}

// API 请求封装
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

// 项目管理功能
class ProjectManager {
    static async createProject(formData) {
        try {
            const result = await API.post('/api/projects', formData);
            showNotification(result.message, 'success');
            return result;
        } catch (error) {
            showNotification(error.message, 'error');
            throw error;
        }
    }

    static async toggleFeatured(projectId) {
        try {
            const result = await API.put(`/api/projects/${projectId}/featured`);
            showNotification(result.message, 'success');
            return result;
        } catch (error) {
            showNotification(error.message, 'error');
            throw error;
        }
    }

    static async deleteProject(projectId) {
        if (!confirm('确定要删除这个项目吗？此操作不可撤销。')) {
            return;
        }

        try {
            const result = await API.delete(`/api/projects/${projectId}`);
            showNotification(result.message, 'success');
            return result;
        } catch (error) {
            showNotification(error.message, 'error');
            throw error;
        }
    }
}

// 用户管理功能
class UserManager {
    static async updateUserRole(userId, newRole) {
        try {
            const result = await API.put(`/api/users/${userId}/role`, { role: newRole });
            showNotification(result.message, 'success');
            return result;
        } catch (error) {
            showNotification(error.message, 'error');
            throw error;
        }
    }

    static async toggleUserStatus(userId) {
        try {
            const result = await API.put(`/api/users/${userId}/status`);
            showNotification(result.message, 'success');
            return result;
        } catch (error) {
            showNotification(error.message, 'error');
            throw error;
        }
    }

    static async getUserDetails(userId) {
        try {
            return await API.get(`/api/users/${userId}`);
        } catch (error) {
            showNotification(error.message, 'error');
            throw error;
        }
    }

    static async deleteUser(userId) {
        if (!confirm('确定要删除这个用户吗？此操作不可撤销。')) {
            return;
        }

        try {
            const result = await API.delete(`/api/users/${userId}`);
            showNotification(result.message, 'success');
            return result;
        } catch (error) {
            showNotification(error.message, 'error');
            throw error;
        }
    }
}

// 表单验证
class FormValidator {
    static validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    static validatePassword(password) {
        return password.length >= 6;
    }

    static validateUsername(username) {
        return username.length >= 3 && /^[a-zA-Z0-9_]+$/.test(username);
    }
}

// 工具函数
class Utils {
    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    static formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('zh-CN');
    }

    static truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function () {
    // 恢复页面可见性，防止闪烁
    document.documentElement.style.visibility = 'visible';
    document.body.style.visibility = 'visible';

    // 初始化 Socket.IO
    initSocket();

    // 初始化 Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 添加淡入动画
    document.body.classList.add('fade-in');

    // 处理导航链接的活动状态
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// 导出到全局作用域
window.API = API;
window.ProjectManager = ProjectManager;
window.UserManager = UserManager;
window.FormValidator = FormValidator;
window.Utils = Utils;
window.showNotification = showNotification;