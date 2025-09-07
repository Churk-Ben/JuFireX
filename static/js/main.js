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

    // 自定义 Tooltip 管理器（替代原生 title，支持延迟、越过 overflow 裁剪与顶层显示）
    (function () {
        const DELAY = 450; // ms 延迟显示，避免遮挡视线
        const OFFSET = 10; // 与目标元素的距离
        let showTimer = null;
        let activeTarget = null;

        // 1) 迁移非 Bootstrap tooltip 的 title -> data-title，避免原生气泡
        const migrateTitles = (root = document) => {
            const nodes = root.querySelectorAll('[title]:not([data-bs-toggle="tooltip"])');
            nodes.forEach(el => {
                const t = el.getAttribute('title');
                if (t && !el.hasAttribute('data-title')) {
                    el.setAttribute('data-title', t);
                }
                el.removeAttribute('title');
            });
        };
        migrateTitles(document);

        // 监听动态 DOM 变化，自动迁移
        const mo = new MutationObserver(mutations => {
            mutations.forEach(m => {
                m.addedNodes && m.addedNodes.forEach(node => {
                    if (node.nodeType === 1) {
                        if (node.matches && node.matches('[title]')) migrateTitles(node.parentNode || document);
                        // 扫描其子树
                        migrateTitles(node);
                    }
                });
            });
        });
        mo.observe(document.documentElement, { childList: true, subtree: true });

        // 2) 单例 Tooltip 节点
        let tipEl = document.querySelector('.jfs-tooltip');
        if (!tipEl) {
            tipEl = document.createElement('div');
            tipEl.className = 'jfs-tooltip';
            document.body.appendChild(tipEl);
        }

        const getTooltipText = (el) => el.getAttribute('data-title');

        const positionTooltip = (target) => {
            const rect = target.getBoundingClientRect();
            const tipRect = tipEl.getBoundingClientRect();
            const vw = window.innerWidth;
            const vh = window.innerHeight;

            // 默认显示在元素下方
            let top = rect.bottom + OFFSET;
            let left = rect.left + (rect.width - tipRect.width) / 2;

            // 如果下方空间不足，则显示在上方
            if (top + tipRect.height > vh) {
                top = rect.top - tipRect.height - OFFSET;
            }

            // 水平防溢出
            left = Math.max(8, Math.min(left, vw - tipRect.width - 8));

            tipEl.style.transform = 'translateY(0) scale(1)'; // 复位变换基准
            tipEl.style.left = Math.round(left) + 'px';
            tipEl.style.top = Math.round(top) + 'px';
        };

        const showTooltip = (target) => {
            const text = getTooltipText(target);
            if (!text) return;
            tipEl.textContent = text;
            tipEl.classList.add('show');
            tipEl.style.opacity = '1';
            // 先渲染内容再计算尺寸
            requestAnimationFrame(() => positionTooltip(target));
        };

        const hideTooltip = () => {
            tipEl.classList.remove('show');
            tipEl.style.opacity = '0';
            activeTarget = null;
        };

        const eligible = (el) => {
            if (!el || el.nodeType !== 1) return null;
            // 忽略启用 Bootstrap Tooltip 的元素
            const node = el.closest('[data-title]');
            if (!node) return null;
            if (node.matches('[data-bs-toggle="tooltip"]')) return null;
            return node;
        };

        // 事件委托：鼠标与键盘焦点
        document.addEventListener('mouseover', (e) => {
            const target = eligible(e.target);
            if (!target) return;
            if (activeTarget === target) return;
            clearTimeout(showTimer);
            showTimer = setTimeout(() => {
                activeTarget = target;
                showTooltip(target);
            }, DELAY);
        }, true);

        document.addEventListener('focusin', (e) => {
            const target = eligible(e.target);
            if (!target) return;
            clearTimeout(showTimer);
            showTimer = setTimeout(() => {
                activeTarget = target;
                showTooltip(target);
            }, DELAY);
        });

        // 跟随移动（减少遮挡）
        document.addEventListener('mousemove', (e) => {
            if (!activeTarget) return;
            // 仅在活跃目标仍在 hover 时更新
            positionTooltip(activeTarget);
        });

        // 离开/失焦立即隐藏
        ['mouseout', 'mouseleave'].forEach(evt => {
            document.addEventListener(evt, (e) => {
                if (!activeTarget) return;
                const related = e.relatedTarget;
                if (related && (related === tipEl || (related.closest && related.closest('.jfs-tooltip')))) return;
                clearTimeout(showTimer);
                hideTooltip();
            }, true);
        });
        document.addEventListener('blur', () => {
            clearTimeout(showTimer);
            hideTooltip();
        }, true);

        // 窗口变化时重新定位
        window.addEventListener('scroll', () => { if (activeTarget) positionTooltip(activeTarget); }, true);
        window.addEventListener('resize', () => { if (activeTarget) positionTooltip(activeTarget); });
    })();

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