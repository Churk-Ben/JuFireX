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
    // 初始化模态框预览功能
    setupPreviewUpdates();
    // 使用事件委托来处理卡片上的所有操作
    const navContainer = document.querySelector('.nav-cards-container'); // 假设你的导航卡片都在这个容器里
    if (navContainer) {
        navContainer.addEventListener('click', handleCardAction);
    }
}

// 处理导航卡片上的操作
function handleCardAction(e) {
    const target = e.target.closest('a.btn, button.btn');
    if (!target) return;

    e.preventDefault();
    const itemId = target.getAttribute('data-item-id');

    if (target.classList.contains('hide-nav-item')) {
        hideNavItem(itemId);
    } else if (target.classList.contains('edit-nav-item')) {
        openEditModal(itemId);
    } else if (target.classList.contains('delete-nav-item')) {
        deleteNavItem(itemId);
    } else if (target.classList.contains('toggle-privacy')) {
        togglePrivacy(itemId);
    }
}

// 设置主要事件监听器
function setupEventListeners() {
    document.getElementById('manageNavBtn')?.addEventListener('click', openManageModal);
    document.getElementById('addNavItemBtn')?.addEventListener('click', openAddModal);
}

// 设置模态框事件监听器
function setupModalEventListeners() {
    // 辅助函数，用于为表单和按钮添加事件监听器
    const addFormSubmitListener = (formId, buttonId, submitFunction) => {
        const form = document.getElementById(formId);
        const button = document.getElementById(buttonId);
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                submitFunction();
            });
        }
        if (button) {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                submitFunction();
            });
        }
    };

    // 添加导航项
    addFormSubmitListener('addNavItemForm', 'saveNavItemBtn', submitAddForm);

    // 编辑导航项
    addFormSubmitListener('editNavItemForm', 'updateNavItemBtn', submitEditForm);

    // 管理模态框关闭时刷新页面
    const manageModal = document.getElementById('navigationManageModal');
    if (manageModal) {
        manageModal.addEventListener('hidden.bs.modal', () => location.reload());
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
async function openAddModal() {
    resetForm('addNavItemForm');
    try {
        if (!categories || categories.length === 0) {
            await loadCategories();
        }
        populateCategorySelects();
        const modal = new bootstrap.Modal(document.getElementById('addNavItemModal'));
        modal.show();
    } catch (error) {
        console.error('Error preparing add modal:', error);
        showNotification('无法打开添加窗口，分类加载失败。', 'error');
    }
}

// 打开编辑模态框
async function openEditModal(itemId) {
    currentEditingItemId = itemId;

    try {
        if (!categories || categories.length === 0) {
            await loadCategories();
        }
        populateCategorySelects();

        const response = await API.get(`/api/nav-items/${itemId}`);
        if (response.success) {
            populateEditForm(response.item);
            const modal = new bootstrap.Modal(document.getElementById('editNavItemModal'));
            modal.show();
        } else {
            showNotification(`获取导航项信息失败: ${response.message}`, 'error');
        }
    } catch (error) {
        console.error('Error preparing edit modal:', error);
        showNotification('无法打开编辑窗口，数据加载失败。', 'error');
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
    const data = Object.fromEntries(formData.entries());

    data.is_public = form.querySelector('[name="is_public"]').checked;
    if (data.order) data.order = parseInt(data.order, 10);
    if (data.category_id) data.category_id = parseInt(data.category_id, 10);

    API.post('/api/nav-items', data)
        .then(response => {
            if (response.success) {
                showNotification('导航项添加成功', 'success');
                const modal = bootstrap.Modal.getInstance(document.getElementById('addNavItemModal'));
                if (modal) modal.hide();
                setTimeout(() => location.reload(), 1000);
            } else {
                showNotification(`添加失败: ${response.message}`, 'error');
            }
        })
        .catch(error => {
            console.error('Error adding item:', error);
            showNotification('添加失败，请查看控制台日志。', 'error');
        });
}

// 提交编辑表单
function submitEditForm() {
    const form = document.getElementById('editNavItemForm');
    const itemId = document.getElementById('editNavItemId').value;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    delete data.id; // 从数据中移除id

    data.is_public = form.querySelector('[name="is_public"]').checked;
    if (data.order) data.order = parseInt(data.order, 10);
    if (data.category_id) data.category_id = parseInt(data.category_id, 10);

    API.put(`/api/nav-items/${itemId}`, data)
        .then(response => {
            if (response.success) {
                showNotification('导航项更新成功', 'success');
                const modal = bootstrap.Modal.getInstance(document.getElementById('editNavItemModal'));
                if (modal) modal.hide();
                setTimeout(() => location.reload(), 1000);
            } else {
                showNotification(`更新失败: ${response.message}`, 'error');
            }
        })
        .catch(error => {
            console.error('Error updating item:', error);
            showNotification('更新失败，请查看控制台日志。', 'error');
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
    if (!confirm('确定要永久删除这个导航项吗？此操作不可恢复。')) {
        return;
    }

    API.delete(`/api/nav-items/${itemId}`)
        .then(response => {
            if (response.success) {
                const card = document.querySelector(`.card[data-nav-item-id='${itemId}']`);
                if (card) {
                    card.remove();
                }
                showNotification('导航项已成功删除', 'success');
            } else {
                showNotification(`删除失败: ${response.message}`, 'error');
            }
        })
        .catch(error => {
            console.error('Error deleting item:', error);
            showNotification('删除失败，请查看控制台日志。', 'error');
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
                setTimeout(() => location.reload(), 1000);
            } else {
                showNotification('切换失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error toggling privacy:', error);
            showNotification('切换失败', 'error');
        });
    // 刷新页面
}

// 将需要全局访问的函数暴露到 window 对象
Object.assign(window, {
    restoreNavItem,
    togglePrivacy,
    deleteNavItem,
    hideNavItem,
    restoreAllHiddenItems
});