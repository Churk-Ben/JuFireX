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

    // 配置Socket.IO选项
    socket = io({
        transports: ['polling', 'websocket'],
        upgrade: true,
        rememberUpgrade: true,
        timeout: 20000,
        forceNew: false
    });

    socket.on('connect', function () {
        console.log('Connected to server');
    });

    socket.on('disconnect', function (reason) {
        console.log('Disconnected from server:', reason);
        if (reason === 'io server disconnect') {
            // 服务器主动断开连接，需要手动重连
            socket.connect();
        }
    });

    socket.on('connect_error', function (error) {
        console.error('Connection error:', error);
    });

    socket.on('notification', function (data) {
        showNotification(data.message, data.type || 'info');
    });

    // 添加重连事件监听
    socket.on('reconnect', function (attemptNumber) {
        console.log('Reconnected to server after', attemptNumber, 'attempts');
    });

    socket.on('reconnect_attempt', function (attemptNumber) {
        console.log('Attempting to reconnect...', attemptNumber);
    });

    socket.on('reconnect_error', function (error) {
        console.error('Reconnection error:', error);
    });

    socket.on('reconnect_failed', function () {
        console.error('Failed to reconnect to server');
    });
}



// 项目管理
class ProjectManager {
    constructor(api) {
        this.api = api;
    }

    // 创建项目
    createProject(formData) {
        return this.api.post('/api/projects', formData, true);
    }
}

// 用户管理
class UserManager {
    constructor(api) {
        this.api = api;
    }

    // 更新头像
    updateAvatar(formData) {
        return this.api.post('/profile/update_avatar', formData, true);
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