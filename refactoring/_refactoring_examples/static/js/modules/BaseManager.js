/**
 * 基础管理器类 - 消除重复的CRUD操作代码
 * 提供通用的增删改查功能，其他管理器可以继承使用
 */
class BaseManager {
    constructor(options = {}) {
        this.apiEndpoint = options.apiEndpoint || '';
        this.entityName = options.entityName || 'item';
        this.containerSelector = options.containerSelector || '';
        this.searchInputSelector = options.searchInputSelector || '';
        this.addFormSelector = options.addFormSelector || '';
        this.editFormSelector = options.editFormSelector || '';
        this.addModalSelector = options.addModalSelector || '';
        this.editModalSelector = options.editModalSelector || '';
        
        // 初始化
        this.init();
    }
    
    /**
     * 初始化管理器
     */
    init() {
        this.bindEvents();
        this.loadItems();
    }
    
    /**
     * 绑定事件监听器
     */
    bindEvents() {
        // 搜索功能
        if (this.searchInputSelector) {
            const searchInput = document.querySelector(this.searchInputSelector);
            if (searchInput) {
                searchInput.addEventListener('input', 
                    Utils.debounce((e) => this.handleSearch(e.target.value), 300)
                );
            }
        }
        
        // 添加表单提交
        if (this.addFormSelector) {
            const addForm = document.querySelector(this.addFormSelector);
            if (addForm) {
                addForm.addEventListener('submit', (e) => this.handleAdd(e));
            }
        }
        
        // 编辑表单提交
        if (this.editFormSelector) {
            const editForm = document.querySelector(this.editFormSelector);
            if (editForm) {
                editForm.addEventListener('submit', (e) => this.handleEdit(e));
            }
        }
        
        // 容器内的操作按钮（编辑、删除等）
        if (this.containerSelector) {
            const container = document.querySelector(this.containerSelector);
            if (container) {
                container.addEventListener('click', (e) => this.handleContainerClick(e));
            }
        }
    }
    
    /**
     * 处理容器内的点击事件
     */
    handleContainerClick(event) {
        const target = event.target.closest('[data-action]');
        if (!target) return;
        
        const action = target.dataset.action;
        const itemId = target.dataset.id;
        
        switch (action) {
            case 'edit':
                this.openEditModal(itemId);
                break;
            case 'delete':
                this.confirmDelete(itemId);
                break;
            case 'toggle':
                this.toggleStatus(itemId, target.dataset.field);
                break;
            default:
                // 子类可以重写此方法处理自定义操作
                this.handleCustomAction(action, itemId, target);
        }
    }
    
    /**
     * 加载项目列表
     */
    async loadItems(searchQuery = '') {
        try {
            const params = searchQuery ? { search: searchQuery } : {};
            const response = await API.get(this.apiEndpoint, params);
            
            if (response.success) {
                this.renderItems(response.data);
            } else {
                this.handleError(`加载${this.entityName}失败`, response.message);
            }
        } catch (error) {
            this.handleError(`加载${this.entityName}失败`, error.message);
        }
    }
    
    /**
     * 处理搜索
     */
    async handleSearch(query) {
        await this.loadItems(query);
    }
    
    /**
     * 处理添加操作
     */
    async handleAdd(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        
        try {
            const response = await API.post(this.apiEndpoint, formData);
            
            if (response.success) {
                this.handleSuccess(`${this.entityName}添加成功`);
                this.closeModal(this.addModalSelector);
                form.reset();
                await this.loadItems();
            } else {
                this.handleError(`添加${this.entityName}失败`, response.message);
            }
        } catch (error) {
            this.handleError(`添加${this.entityName}失败`, error.message);
        }
    }
    
    /**
     * 处理编辑操作
     */
    async handleEdit(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        const itemId = formData.get('id');
        
        if (!itemId) {
            this.handleError('编辑失败', '未找到项目ID');
            return;
        }
        
        try {
            const response = await API.put(`${this.apiEndpoint}/${itemId}`, formData);
            
            if (response.success) {
                this.handleSuccess(`${this.entityName}更新成功`);
                this.closeModal(this.editModalSelector);
                await this.loadItems();
            } else {
                this.handleError(`更新${this.entityName}失败`, response.message);
            }
        } catch (error) {
            this.handleError(`更新${this.entityName}失败`, error.message);
        }
    }
    
    /**
     * 打开编辑模态框
     */
    async openEditModal(itemId) {
        try {
            const response = await API.get(`${this.apiEndpoint}/${itemId}`);
            
            if (response.success) {
                this.populateEditForm(response.data);
                this.showModal(this.editModalSelector);
            } else {
                this.handleError('获取数据失败', response.message);
            }
        } catch (error) {
            this.handleError('获取数据失败', error.message);
        }
    }
    
    /**
     * 确认删除
     */
    confirmDelete(itemId) {
        if (confirm(`确定要删除这个${this.entityName}吗？此操作不可撤销。`)) {
            this.deleteItem(itemId);
        }
    }
    
    /**
     * 删除项目
     */
    async deleteItem(itemId) {
        try {
            const response = await API.delete(`${this.apiEndpoint}/${itemId}`);
            
            if (response.success) {
                this.handleSuccess(`${this.entityName}删除成功`);
                await this.loadItems();
            } else {
                this.handleError(`删除${this.entityName}失败`, response.message);
            }
        } catch (error) {
            this.handleError(`删除${this.entityName}失败`, error.message);
        }
    }
    
    /**
     * 切换状态
     */
    async toggleStatus(itemId, field) {
        try {
            const response = await API.put(`${this.apiEndpoint}/${itemId}/toggle`, { field });
            
            if (response.success) {
                this.handleSuccess('状态更新成功');
                await this.loadItems();
            } else {
                this.handleError('状态更新失败', response.message);
            }
        } catch (error) {
            this.handleError('状态更新失败', error.message);
        }
    }
    
    // ========== 工具方法 ==========
    
    /**
     * 显示模态框
     */
    showModal(selector) {
        const modal = document.querySelector(selector);
        if (modal) {
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
        }
    }
    
    /**
     * 关闭模态框
     */
    closeModal(selector) {
        const modal = document.querySelector(selector);
        if (modal) {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        }
    }
    
    /**
     * 处理成功响应
     */
    handleSuccess(message) {
        showNotification(message, 'success');
    }
    
    /**
     * 处理错误响应
     */
    handleError(title, message) {
        showNotification(`${title}: ${message}`, 'error');
    }
    
    // ========== 需要子类实现的方法 ==========
    
    /**
     * 渲染项目列表 - 子类必须实现
     */
    renderItems(items) {
        throw new Error('renderItems method must be implemented by subclass');
    }
    
    /**
     * 填充编辑表单 - 子类必须实现
     */
    populateEditForm(item) {
        throw new Error('populateEditForm method must be implemented by subclass');
    }
    
    /**
     * 处理自定义操作 - 子类可以重写
     */
    handleCustomAction(action, itemId, target) {
        console.warn(`Unhandled action: ${action}`);
    }
}

// 导出基础管理器
window.BaseManager = BaseManager;