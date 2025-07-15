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
            togglePrivacy(itemId);
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

    // 管理模态框关闭时刷新页面
    const manageModal = document.getElementById('navigationManageModal');
    if (manageModal) {
        manageModal.addEventListener('hidden.bs.modal', function () {
            location.reload();
        });
    }
}

// 恢复单个导航项
window.restoreNavItem = function (itemId) {
    API.post(`/api/navigation/unhide/${itemId}`)
        .then(data => {
            if (data.success) {
                showNotification('导航项已恢复', 'success');
                // 从管理模态框的列表中移除该项
                const itemInModal = document.querySelector(`#navigationManageModal [data-hidden-item-id='${itemId}']`);
                if (itemInModal) {
                    itemInModal.remove();
                }
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
window.restoreAllHiddenItems = function () {
    if (!confirm('确定要恢复所有隐藏的导航项吗？')) {
        return;
    }

    const hiddenItemElements = document.querySelectorAll('[data-hidden-item-id]');
    const itemIds = Array.from(hiddenItemElements).map(el => el.getAttribute('data-hidden-item-id'));

    if (itemIds.length === 0) {
        showNotification('没有需要恢复的导航项', 'info');
        return;
    }

    API.post('/api/navigation/unhide_all', { item_ids: itemIds })
        .then(data => {
            if (data.success) {
                showNotification(`${data.unhidden_count} 个导航项已恢复`, 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                showNotification('恢复失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error restoring all items:', error);
            showNotification('恢复所有项时出错', 'error');
        });
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

// 加载分类数据
function loadCategories() {
    return API.get('/api/nav-categories')
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

    const showModal = () => {
        API.get(`/api/nav-items/${itemId}`)
            .then(data => {
                if (data.success) {
                    populateEditForm(data.item);
                    const modal = new bootstrap.Modal(document.getElementById('editNavItemModal'));
                    modal.show();
                } else {
                    showNotification('获取导航项信息失败: ' + data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error fetching item:', error);
                showNotification('获取导航项信息失败', 'error');
            });
    };

    if (!categories || categories.length === 0) {
        loadCategories().then(() => {
            populateCategorySelects();
            showModal();
        }).catch(error => {
            console.error('Error loading categories for edit modal:', error);
            showNotification('加载分类数据失败', 'error');
        });
    } else {
        populateCategorySelects();
        showModal();
    }
}

// 填充编辑表单
function populateEditForm(item) {
    document.getElementById('editNavItemId').value = item.id;
    document.getElementById('editNavItemTitle').value = item.title;
    document.getElementById('editNavItemUrl').value = item.url;
    document.getElementById('editNavItemDescription').value = item.description || '';
    document.getElementById('editNavItemIcon').value = item.icon || '';
    document.getElementById('editNavItemCategory').value = item.category_id;
    document.getElementById('editNavItemIsPublic').checked = item.is_public;
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

    API.post('/api/nav-items', data)
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

    API.put(`/api/nav-items/${itemId}`, data)
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
    API.post(`/api/navigation/hide/${itemId}`, { nav_item_id: itemId })
        .then(data => {
            if (data.success) {
                showNotification('导航项已隐藏', 'success');
                setTimeout(() => location.reload(), 1000); // 刷新页面
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

    API.delete(`/api/nav-items/${itemId}`)
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

// 打开管理模态框（占位符）
function openManageModal() {
    // TODO: 实现管理模态框的逻辑
    console.log('打开管理模态框');
    // 示例: new bootstrap.Modal(document.getElementById('manageNavModal')).show();
}

// 记录导航点击事件
function recordNavClick(itemId, url) {
    // 记录点击事件（可选功能）
    API.post('/api/navigation/click', { item_id: itemId })
        .catch(error => {
            console.error('Error recording click:', error);
        });

    // 打开链接
    window.open(url, '_blank');
}

// 切换隐私状态
function togglePrivacy(itemId) {
    const itemElement = document.querySelector(`[data-nav-item-id='${itemId}']`);
    if (!itemElement) return;

    const isPublic = itemElement.dataset.isPublic === 'true';
    const newIsPublic = !isPublic;

    API.put(`/api/nav-items/${itemId}/visibility`, { is_public: newIsPublic })
        .then(data => {
            if (data.success) {
                showNotification(newIsPublic ? '已设为公开' : '已设为私有', 'success');
                itemElement.dataset.isPublic = newIsPublic;
                const icon = itemElement.querySelector('.privacy-icon');
                if (icon) {
                    icon.classList.toggle('fa-eye', newIsPublic);
                    icon.classList.toggle('fa-eye-slash', !newIsPublic);
                }
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
window.togglePrivacy = togglePrivacy;
window.deleteNavItem = deleteNavItem;
window.hideNavItem = hideNavItem;