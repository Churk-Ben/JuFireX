// 全局变量
let categories = [];
let currentEditingItemId = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function () {
    initializeNavigation();
    loadCategories();
    setupEventListeners();
    setupModalEventListeners();
});

// 初始化导航功能
function initializeNavigation() {
    // 为所有导航项卡片添加事件监听器
    setupCardEventListeners();

    // 初始化模态框预览功能
    setupPreviewUpdates();
}

// 设置卡片事件监听器
function setupCardEventListeners() {
    // 隐藏导航项
    document.querySelectorAll('.hide-nav-item').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const itemId = this.getAttribute('data-item-id');
            hideNavItem(itemId);
        });
    });

    // 编辑导航项
    document.querySelectorAll('.edit-nav-item').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const itemId = this.getAttribute('data-item-id');
            openEditModal(itemId);
        });
    });

    // 删除导航项
    document.querySelectorAll('.delete-nav-item').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const itemId = this.getAttribute('data-item-id');
            deleteNavItem(itemId);
        });
    });

    // 切换公开/私有状态
    document.querySelectorAll('.toggle-privacy').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const itemId = this.getAttribute('data-item-id');
            toggleItemPrivacy(itemId);
        });
    });
}

// 设置主要事件监听器
function setupEventListeners() {
    // 管理导航按钮
    const manageBtn = document.getElementById('manageNavBtn');
    if (manageBtn) {
        manageBtn.addEventListener('click', function () {
            openManageModal();
        });
    }

    // 添加导航项按钮
    const addBtn = document.getElementById('addNavItemBtn');
    if (addBtn) {
        addBtn.addEventListener('click', function () {
            openAddModal();
        });
    }
}

// 设置模态框事件监听器
function setupModalEventListeners() {
    // 添加导航项表单提交
    const addForm = document.getElementById('addNavItemForm');
    if (addForm) {
        addForm.addEventListener('submit', function (e) {
            e.preventDefault();
            submitAddForm();
        });
    }

    // 添加导航项保存按钮
    const saveNavItemBtn = document.getElementById('saveNavItemBtn');
    if (saveNavItemBtn) {
        saveNavItemBtn.addEventListener('click', function (e) {
            e.preventDefault();
            submitAddForm();
        });
    }

    // 编辑导航项表单提交
    const editForm = document.getElementById('editNavItemForm');
    if (editForm) {
        editForm.addEventListener('submit', function (e) {
            e.preventDefault();
            submitEditForm();
        });
    }

    // 编辑导航项更新按钮
    const updateNavItemBtn = document.getElementById('updateNavItemBtn');
    if (updateNavItemBtn) {
        updateNavItemBtn.addEventListener('click', function (e) {
            e.preventDefault();
            submitEditForm();
        });
    }

    // 恢复全部按钮
    const restoreAllBtn = document.getElementById('restoreAllBtn');
    if (restoreAllBtn) {
        restoreAllBtn.addEventListener('click', function () {
            restoreAllHiddenItems();
        });
    }

    // 导航管理模态框显示时加载隐藏项
    const navigationManageModal = document.getElementById('navigationManageModal');
    if (navigationManageModal) {
        navigationManageModal.addEventListener('shown.bs.modal', function () {
            loadHiddenItems();
        });
    }
}

// 设置预览更新功能
function setupPreviewUpdates() {
    // 添加模态框预览
    setupFormPreview('addNavItemForm', {
        title: 'previewTitle',
        description: 'previewDescription',
        icon: 'previewIcon'
    });

    // 编辑模态框预览
    setupFormPreview('editNavItemForm', {
        title: 'editPreviewTitle',
        description: 'editPreviewDescription',
        icon: 'editPreviewIcon'
    });
}

// 设置表单预览功能
function setupFormPreview(formId, previewIds) {
    const form = document.getElementById(formId);
    if (!form) return;

    const titleInput = form.querySelector('[name="title"]');
    const descInput = form.querySelector('[name="description"]');
    const iconInput = form.querySelector('[name="icon"]');

    if (titleInput) {
        titleInput.addEventListener('input', function () {
            const previewTitle = document.getElementById(previewIds.title);
            if (previewTitle) {
                previewTitle.textContent = this.value || '导航项标题';
            }
        });
    }

    if (descInput) {
        descInput.addEventListener('input', function () {
            const previewDesc = document.getElementById(previewIds.description);
            if (previewDesc) {
                previewDesc.textContent = this.value || '导航项描述';
            }
        });
    }

    if (iconInput) {
        iconInput.addEventListener('input', function () {
            const previewIcon = document.getElementById(previewIds.icon);
            if (previewIcon) {
                previewIcon.className = this.value || 'fas fa-link';
                previewIcon.className += ' me-2 text-primary';
            }
        });
    }
}

// 获取CSRF Token
function getCSRFToken() {
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    return csrfMeta ? csrfMeta.getAttribute('content') : '';
}

// 加载分类数据
function loadCategories() {
    return fetch('/api/nav-categories', {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                categories = data.categories;
                populateCategorySelects();
                return data.categories;
            } else {
                throw new Error('Failed to load categories');
            }
        })
        .catch(error => {
            console.error('Error loading categories:', error);
            throw error;
        });
}

// 填充分类选择框
function populateCategorySelects() {
    const selects = document.querySelectorAll('#navItemCategory, #editNavItemCategory');
    selects.forEach(select => {
        select.innerHTML = '<option value="">请选择分类</option>';
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name;
            select.appendChild(option);
        });
    });
}

// 打开管理模态框
function openManageModal() {
    loadHiddenItems();
    const modal = new bootstrap.Modal(document.getElementById('navigationManageModal'));
    modal.show();
}

// 打开添加模态框
function openAddModal() {
    resetForm('addNavItemForm');
    // 确保分类数据已加载
    if (!categories || categories.length === 0) {
        loadCategories().then(() => {
            const modal = new bootstrap.Modal(document.getElementById('addNavItemModal'));
            modal.show();
        }).catch(error => {
            console.error('Error loading categories for add modal:', error);
            showNotification('加载分类数据失败', 'error');
        });
    } else {
        populateCategorySelects();
        const modal = new bootstrap.Modal(document.getElementById('addNavItemModal'));
        modal.show();
    }
}

// 打开编辑模态框
function openEditModal(itemId) {
    currentEditingItemId = itemId;
    // 确保分类数据已加载
    if (!categories || categories.length === 0) {
        loadCategories().then(() => {
            loadItemData(itemId);
            const modal = new bootstrap.Modal(document.getElementById('editNavItemModal'));
            modal.show();
        }).catch(error => {
            console.error('Error loading categories for edit modal:', error);
            showNotification('加载分类数据失败', 'error');
        });
    } else {
        populateCategorySelects();
        loadItemData(itemId);
        const modal = new bootstrap.Modal(document.getElementById('editNavItemModal'));
        modal.show();
    }
}

// 加载导航项数据
function loadItemData(itemId) {
    fetch(`/api/nav-items/${itemId}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateEditForm(data.item);
            } else {
                showNotification('加载数据失败', 'error');
            }
        })
        .catch(error => {
            console.error('Error loading item data:', error);
            showNotification('加载数据失败', 'error');
        });
}

// 填充编辑表单
function populateEditForm(item) {
    const form = document.getElementById('editNavItemForm');
    if (!form) return;

    form.querySelector('[name="title"]').value = item.title || '';
    form.querySelector('[name="description"]').value = item.description || '';
    form.querySelector('[name="url"]').value = item.url || '';
    form.querySelector('[name="icon"]').value = item.icon || '';
    form.querySelector('[name="category_id"]').value = item.category_id || '';
    form.querySelector('[name="is_public"]').checked = item.is_public || false;
}

// 提交添加表单
function submitAddForm() {
    const form = document.getElementById('addNavItemForm');
    const formData = new FormData(form);

    // 将FormData转换为JSON对象
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }

    // 处理复选框值
    const isPublicCheckbox = form.querySelector('[name="is_public"]');
    if (isPublicCheckbox) {
        data.is_public = isPublicCheckbox.checked;
    }

    // 处理数字字段
    if (data.order) {
        data.order = parseInt(data.order);
    }
    if (data.category_id) {
        data.category_id = parseInt(data.category_id);
    }

    fetch('/api/nav-items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('导航项添加成功', 'success');
                bootstrap.Modal.getInstance(document.getElementById('addNavItemModal')).hide();
                location.reload();
            } else {
                showNotification('添加失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error adding item:', error);
            showNotification('添加失败', 'error');
        });
}

// 提交编辑表单
function submitEditForm() {
    const form = document.getElementById('editNavItemForm');
    const formData = new FormData(form);
    const itemId = document.getElementById('editNavItemId').value;

    // 将FormData转换为JSON对象
    const data = {};
    for (let [key, value] of formData.entries()) {
        if (key !== 'id') { // 排除隐藏的id字段
            data[key] = value;
        }
    }

    // 处理复选框值
    const isPublicCheckbox = form.querySelector('[name="is_public"]');
    if (isPublicCheckbox) {
        data.is_public = isPublicCheckbox.checked;
    }

    // 处理数字字段
    if (data.order) {
        data.order = parseInt(data.order);
    }
    if (data.category_id) {
        data.category_id = parseInt(data.category_id);
    }

    fetch(`/api/nav-items/${itemId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('导航项更新成功', 'success');
                bootstrap.Modal.getInstance(document.getElementById('editNavItemModal')).hide();
                location.reload();
            } else {
                showNotification('更新失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error updating item:', error);
            showNotification('更新失败', 'error');
        });
}

// 隐藏导航项
function hideNavItem(itemId) {
    fetch(`/api/navigation/hide/${itemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ nav_item_id: itemId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const card = document.querySelector(`[data-nav-item-id="${itemId}"]`);
                if (card) {
                    card.style.display = 'none';
                }
                showNotification('导航项已隐藏', 'success');
            } else {
                showNotification('隐藏失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error hiding item:', error);
            showNotification('隐藏失败', 'error');
        });
}

// 删除导航项
function deleteNavItem(itemId) {
    if (!confirm('确定要删除这个导航项吗？此操作不可恢复。')) {
        return;
    }

    fetch(`/api/nav-items/${itemId}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const card = document.querySelector(`[data-nav-item-id="${itemId}"]`);
                if (card) {
                    card.remove();
                }
                showNotification('导航项已删除', 'success');
            } else {
                showNotification('删除失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error deleting item:', error);
            showNotification('删除失败', 'error');
        });
}

// 切换导航项隐私状态
function toggleItemPrivacy(itemId) {
    const button = document.querySelector(`[data-nav-item-id="${itemId}"] .toggle-privacy`);
    const isPublic = button ? button.getAttribute('data-is-public') === '1' : false;

    fetch(`/api/nav-items/${itemId}/visibility`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ is_public: !isPublic })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                button.textContent = isPublic ? '设为公开' : '设为私有';
                button.setAttribute('data-is-public', isPublic ? '0' : '1');
                showNotification(isPublic ? '已设为私有' : '已设为公开', 'success');
            } else {
                showNotification('切换失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error toggling privacy:', error);
            showNotification('切换失败', 'error');
        });
}

// 加载隐藏的导航项
function loadHiddenItems() {
    fetch('/api/navigation/hidden_items', {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayHiddenItems(data.items);
            }
        })
        .catch(error => {
            console.error('Error loading hidden items:', error);
        });
}

// 显示隐藏的导航项
function displayHiddenItems(items) {
    const container = document.getElementById('hidden-items-list');
    if (!container) return;

    container.innerHTML = '';

    if (items.length === 0) {
        container.innerHTML = `
            <div class="text-center py-4 text-muted">
                <i class="fas fa-eye mb-2" style="font-size: 2rem;"></i>
                <p class="mb-0">暂无隐藏的导航项</p>
            </div>
        `;
        return;
    }

    items.forEach(item => {
        const itemElement = createHiddenItemElement(item);
        container.appendChild(itemElement);
    });
}

// 创建隐藏项元素
function createHiddenItemElement(item) {
    const div = document.createElement('div');
    div.className = 'card mb-2';
    div.innerHTML = `
        <div class="card-body py-2">
            <div class="d-flex justify-content-between align-items-center">
                <div class="flex-grow-1">
                    <div class="d-flex align-items-center mb-1">
                        <i class="${item.icon || 'fas fa-link'} me-2 text-primary"></i>
                        <h6 class="mb-0 fw-bold">${item.title}</h6>
                    </div>
                    <p class="text-muted small mb-1">${item.description || '暂无描述'}</p>
                    <div class="d-flex align-items-center text-muted small">
                        <span class="me-3"><i class="fas fa-link me-1"></i>${item.url}</span>
                        <span class="me-3"><i class="fas fa-folder me-1"></i>${item.category_name}</span>
                        <span><i class="fas fa-clock me-1"></i>${item.hidden_at}</span>
                    </div>
                </div>
                <button class="btn btn-sm btn-outline-success" onclick="restoreNavItem(${item.id})">
                    <i class="fas fa-eye me-1"></i>取消隐藏
                </button>
            </div>
        </div>
    `;
    return div;
}

// 恢复单个导航项
function restoreNavItem(itemId) {
    fetch(`/api/navigation/unhide/${itemId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('导航项已恢复', 'success');
                loadHiddenItems(); // 重新加载隐藏项列表
                location.reload(); // 刷新页面显示恢复的项
            } else {
                showNotification('恢复失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error restoring item:', error);
            showNotification('恢复失败', 'error');
        });
}

// 恢复所有隐藏的导航项
function restoreAllHiddenItems() {
    if (!confirm('确定要恢复所有隐藏的导航项吗？')) {
        return;
    }

    // 获取所有隐藏项的ID
    const hiddenItems = document.querySelectorAll('#hidden-items-list .card');
    const itemIds = [];

    hiddenItems.forEach(item => {
        const restoreBtn = item.querySelector('button[onclick*="restoreNavItem"]');
        if (restoreBtn) {
            const onclick = restoreBtn.getAttribute('onclick');
            const match = onclick.match(/restoreNavItem\((\d+)\)/);
            if (match) {
                itemIds.push(match[1]);
            }
        }
    });

    if (itemIds.length === 0) {
        showNotification('没有需要恢复的导航项', 'info');
        return;
    }

    let successCount = 0;
    let errorCount = 0;

    // 逐个恢复隐藏项
    const restorePromises = itemIds.map(itemId => {
        return fetch(`/api/navigation/unhide/${itemId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    successCount++;
                } else {
                    errorCount++;
                }
            })
            .catch(error => {
                console.error(`Error restoring item ${itemId}:`, error);
                errorCount++;
            });
    });

    Promise.all(restorePromises).then(() => {
        if (successCount > 0) {
            showNotification(`成功恢复 ${successCount} 个导航项${errorCount > 0 ? `，${errorCount} 个失败` : ''}`, 'success');
            bootstrap.Modal.getInstance(document.getElementById('manageNavModal')).hide();
            location.reload();
        } else {
            showNotification('恢复失败', 'error');
        }
    });
}

// 重置表单
function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
        // 重置预览
        const previewTitle = form.querySelector('.preview-title');
        const previewDesc = form.querySelector('.preview-description');
        const previewIcon = form.querySelector('.preview-icon');

        if (previewTitle) previewTitle.textContent = '导航项标题';
        if (previewDesc) previewDesc.textContent = '导航项描述';
        if (previewIcon) previewIcon.className = 'fas fa-link me-2 text-primary';
    }
}

// 获取CSRF Token
function getCSRFToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}

// 记录导航点击事件
function recordNavClick(itemId, url) {
    // 记录点击事件（可选功能）
    fetch('/api/navigation/click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ item_id: itemId })
    })
        .catch(error => {
            console.error('Error recording click:', error);
        });

    // 打开链接
    window.open(url, '_blank');
}

// 显示通知
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
         ${message}
         <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
     `;

    document.body.appendChild(notification);


    // 自动移除通知
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// 工具函数：格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// 工具函数：截断文本
function truncateText(text, maxLength = 100) {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

// 工具函数：验证URL
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// 编辑导航项
function editNavItem(itemId) {
    // 获取导航项详情
    fetch(`/api/nav-items/${itemId}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const item = data.item;
                // 填充编辑表单
                document.getElementById('editNavItemId').value = item.id;
                document.getElementById('editNavItemTitle').value = item.title;
                document.getElementById('editNavItemUrl').value = item.url;
                document.getElementById('editNavItemDescription').value = item.description || '';
                document.getElementById('editNavItemIcon').value = item.icon || '';
                document.getElementById('editNavItemOrder').value = item.order || 0;
                document.getElementById('editNavItemIsPublic').checked = item.is_public;
                document.getElementById('editNavItemCategory').value = item.category_id;

                // 显示编辑模态框
                const editModal = new bootstrap.Modal(document.getElementById('editNavItemModal'));
                editModal.show();
            } else {
                showNotification('获取导航项信息失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error fetching item:', error);
            showNotification('获取导航项信息失败', 'error');
        });
}

// 切换隐私状态
function togglePrivacy(itemId, isCurrentlyPublic) {
    const newIsPublic = !isCurrentlyPublic;

    fetch(`/api/nav-items/${itemId}/visibility`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ is_public: newIsPublic })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(newIsPublic ? '已设为公开' : '已设为私有', 'success');
                location.reload(); // 刷新页面以更新显示
            } else {
                showNotification('切换失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error toggling privacy:', error);
            showNotification('切换失败', 'error');
        });
}

// 导出函数供全局使用
window.recordNavClick = recordNavClick;
window.restoreNavItem = restoreNavItem;
window.showNotification = showNotification;
window.editNavItem = editNavItem;
window.togglePrivacy = togglePrivacy;
window.deleteNavItem = deleteNavItem;
window.hideNavItem = hideNavItem;