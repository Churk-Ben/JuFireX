// 全局变量
let categories = [];

document.addEventListener('DOMContentLoaded', initializeNavigationPage);

function initializeNavigationPage() {
    loadCategories().catch(error => {
        console.error('Initialization failed:', error);
        showNotification('页面初始化失败，无法加载分类数据', 'danger');
    });
    setupEventListeners();
}

function setupEventListeners() {
    // 使用事件委托处理动态生成的元素
    document.body.addEventListener('click', handleDynamicClicks);

    // 静态按钮事件监听
    document.getElementById('saveCategoryBtn')?.addEventListener('click', handleSaveCategory);
    document.getElementById('updateCategoryBtn')?.addEventListener('click', handleUpdateCategory);
    document.getElementById('confirmDeleteCategoryBtn')?.addEventListener('click', handleConfirmDeleteCategory);
    document.getElementById('saveNavItemBtn')?.addEventListener('click', handleSaveNavItem);
    document.getElementById('updateNavItemBtn')?.addEventListener('click', handleUpdateNavItem);
    document.getElementById('confirmDeleteNavItemBtn')?.addEventListener('click', handleConfirmDeleteNavItem);
}

function handleDynamicClicks(event) {
    const target = event.target;
    const link = target.closest('a, button');
    if (!link) return;

    // 分类操作
    if (link.matches('.edit-category')) {
        event.preventDefault();
        openCategoryModal('editCategoryModal', link.dataset);
    }
    if (link.matches('.delete-category')) {
        event.preventDefault();
        openDeleteCategoryModal(link.dataset);
    }

    // 导航项操作
    if (link.matches('[data-bs-target="#addNavItemModal"]')) {
        openNavItemModal('addNavItemModal', link.dataset);
    }
    if (link.matches('.edit-nav-item')) {
        event.preventDefault();
        openNavItemModal('editNavItemModal', link.dataset);
    }
    if (link.matches('.delete-nav-item')) {
        event.preventDefault();
        openDeleteNavItemModal(link.dataset);
    }
    if (link.matches('.toggle-visibility')) {
        event.preventDefault();
        handleToggleVisibility(link.dataset);
    }
    if (link.matches('.unhide-nav-item')) {
        event.preventDefault();
        handleUnhideNavItem(link.dataset);
    }
}

// API 响应处理
function handleApiResponse(reload = true) {
    return data => {
        if (data.success) {
            showNotification(data.message, 'success');
            if (reload) setTimeout(() => location.reload(), 500);
        } else {
            showNotification(data.message || '操作失败', 'danger');
        }
    };
}

function handleApiError(action) {
    return error => {
        console.error(`Error during ${action}:`, error);
        showNotification(`${action}时出错`, 'danger');
    };
}

// 分类管理
function handleSaveCategory() {
    const name = document.getElementById('categoryName').value;
    if (!name) return showNotification('分类名称不能为空', 'warning');

    const payload = {
        name,
        icon: document.getElementById('categoryIcon').value,
        order: parseInt(document.getElementById('categoryOrder').value) || 0
    };
    API.post('/api/nav-categories', payload)
        .then(handleApiResponse())
        .catch(handleApiError('创建分类'));
}

function handleUpdateCategory() {
    const categoryId = document.getElementById('editCategoryId').value;
    const name = document.getElementById('editCategoryName').value;
    if (!name) return showNotification('分类名称不能为空', 'warning');

    const payload = {
        name,
        icon: document.getElementById('editCategoryIcon').value,
        order: parseInt(document.getElementById('editCategoryOrder').value) || 0
    };
    API.put(`/api/nav-categories/${categoryId}`, payload)
        .then(handleApiResponse())
        .catch(handleApiError('更新分类'));
}

function handleConfirmDeleteCategory() {
    const categoryId = document.getElementById('deleteCategoryId').value;
    API.delete(`/api/nav-categories/${categoryId}`)
        .then(handleApiResponse())
        .catch(handleApiError('删除分类'));
}

function openCategoryModal(modalId, dataset) {
    document.getElementById('editCategoryId').value = dataset.categoryId;
    document.getElementById('editCategoryName').value = dataset.categoryName;
    document.getElementById('editCategoryIcon').value = dataset.categoryIcon;
    document.getElementById('editCategoryOrder').value = dataset.categoryOrder;
    bootstrap.Modal.getOrCreateInstance(document.getElementById(modalId)).show();
}

function openDeleteCategoryModal(dataset) {
    document.getElementById('deleteCategoryId').value = dataset.categoryId;
    document.getElementById('deleteCategoryConfirmMessage').textContent = `确定要删除分类 "${dataset.categoryName}" 吗？此操作将同时删除该分类下的所有导航项，且不可撤销。`;
    bootstrap.Modal.getOrCreateInstance(document.getElementById('deleteCategoryConfirmModal')).show();
}

// 导航项管理
function handleSaveNavItem() {
    const form = document.getElementById('addNavItemForm');
    if (!validateNavItemForm(form)) return;

    const payload = getNavItemFormData(form);
    API.post('/api/nav-items', payload)
        .then(handleApiResponse())
        .catch(handleApiError('创建导航项'));
}

function handleUpdateNavItem() {
    const form = document.getElementById('editNavItemForm');
    if (!validateNavItemForm(form)) return;

    const itemId = document.getElementById('editNavItemId').value;
    const payload = getNavItemFormData(form);
    API.put(`/api/nav-items/${itemId}`, payload)
        .then(handleApiResponse())
        .catch(handleApiError('更新导航项'));
}

function handleConfirmDeleteNavItem() {
    const itemId = document.getElementById('deleteNavItemId').value;
    API.delete(`/api/nav-items/${itemId}`)
        .then(handleApiResponse())
        .catch(handleApiError('删除导航项'));
}

function handleToggleVisibility(dataset) {
    const { itemId, isPublic } = dataset;
    API.put(`/api/nav-items/${itemId}/visibility`, { is_public: !(isPublic === 'true') })
        .then(handleApiResponse())
        .catch(handleApiError('更新导航项状态'));
}

function handleUnhideNavItem(dataset) {
    const { itemId, itemTitle } = dataset;
    if (confirm(`确定要显示导航项 "${itemTitle}" 吗？`)) {
        API.post(`/api/navigation/unhide/${itemId}`, {})
            .then(handleApiResponse())
            .catch(handleApiError('显示导航项'));
    }
}

async function openNavItemModal(modalId, dataset) {
    try {
        if (!categories || categories.length === 0) {
            await loadCategories();
        }
        populateCategorySelects();

        if (modalId === 'addNavItemModal') {
            document.getElementById('navItemCategory').value = dataset.categoryId || '';
        } else if (modalId === 'editNavItemModal') {
            document.getElementById('editNavItemId').value = dataset.itemId;
            document.getElementById('editNavItemTitle').value = dataset.itemTitle;
            document.getElementById('editNavItemUrl').value = dataset.itemUrl;
            document.getElementById('editNavItemDescription').value = dataset.itemDescription;
            document.getElementById('editNavItemIcon').value = dataset.itemIcon;
            document.getElementById('editNavItemIsPublic').checked = dataset.itemIsPublic === 'true';
            document.getElementById('editNavItemCategory').value = dataset.itemCategoryId;
            document.getElementById('editNavItemOrder').value = dataset.itemOrder;
        }

        bootstrap.Modal.getOrCreateInstance(document.getElementById(modalId)).show();
    } catch (error) {
        showNotification('加载分类数据失败', 'danger');
    }
}

function openDeleteNavItemModal(dataset) {
    document.getElementById('deleteNavItemId').value = dataset.itemId;
    document.getElementById('deleteNavItemConfirmMessage').textContent = `确定要删除导航项 "${dataset.itemTitle}" 吗？此操作不可撤销。`;
    bootstrap.Modal.getOrCreateInstance(document.getElementById('deleteNavItemConfirmModal')).show();
}

function getNavItemFormData(form) {
    const formData = new FormData(form);
    return {
        title: formData.get('title'),
        url: formData.get('url'),
        description: formData.get('description'),
        icon: formData.get('icon'),
        category_id: parseInt(formData.get('category_id')),
        is_public: form.querySelector('[name="is_public"]').checked,
        order: parseInt(formData.get('order')) || 0
    };
}

function validateNavItemForm(form) {
    const data = getNavItemFormData(form);
    if (!data.title) {
        showNotification('标题不能为空', 'warning');
        return false;
    }
    if (!data.url) {
        showNotification('URL不能为空', 'warning');
        return false;
    }
    if (!data.category_id) {
        showNotification('请选择分类', 'warning');
        return false;
    }
    return true;
}

// 数据加载与UI填充
async function loadCategories() {
    try {
        const response = await API.get('/api/nav-categories');
        if (response.success) {
            categories = response.categories;
            populateCategorySelects();
            return categories;
        } else {
            throw new Error('Failed to load categories');
        }
    } catch (error) {
        console.error('Error loading categories:', error);
        throw error; // Re-throw to be caught by caller
    }
}

function populateCategorySelects() {
    const selects = document.querySelectorAll('#navItemCategory, #editNavItemCategory');
    selects.forEach(select => {
        const currentValue = select.value;
        select.innerHTML = '<option value="">请选择分类</option>';
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name;
            select.appendChild(option);
        });
        select.value = currentValue;
    });
}