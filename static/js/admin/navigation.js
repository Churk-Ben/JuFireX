// 管理导航分类和导航项的JavaScript文件

// 全局变量
let categories = [];

document.addEventListener('DOMContentLoaded', function () {
    // 获取DOM元素
    const categoryAccordion = document.getElementById('categoryAccordion');
    const addCategoryBtn = document.getElementById('addCategoryBtn');
    const saveCategoryBtn = document.getElementById('saveCategoryBtn');
    const updateCategoryBtn = document.getElementById('updateCategoryBtn');
    const confirmDeleteCategoryBtn = document.getElementById('confirmDeleteCategoryBtn');
    const saveNavItemBtn = document.getElementById('saveNavItemBtn');
    const updateNavItemBtn = document.getElementById('updateNavItemBtn');
    const confirmDeleteNavItemBtn = document.getElementById('confirmDeleteNavItemBtn');

    // 初始化时加载分类数据
    loadCategories();

    // 添加分类
    saveCategoryBtn.addEventListener('click', function () {
        const name = document.getElementById('categoryName').value;
        const icon = document.getElementById('categoryIcon').value;
        const order = document.getElementById('categoryOrder').value;

        if (!name) {
            showNotification('分类名称不能为空', 'warning');
            return;
        }

        API.post('/api/nav-categories', { name, icon, order: parseInt(order) || 0 })
            .then(data => {
                if (data.success) {
                    showNotification(data.message, 'success');
                    location.reload();
                } else {
                    showNotification(data.message || '创建分类失败', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('创建分类时出错', 'danger');
            });
    });

    // 编辑分类 - 打开模态框
    document.querySelectorAll('.edit-category').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const categoryId = this.getAttribute('data-category-id');
            const name = this.getAttribute('data-category-name');
            const icon = this.getAttribute('data-category-icon');
            const order = this.getAttribute('data-category-order');

            document.getElementById('editCategoryId').value = categoryId;
            document.getElementById('editCategoryName').value = name;
            document.getElementById('editCategoryIcon').value = icon;
            document.getElementById('editCategoryOrder').value = order;

            const modal = new bootstrap.Modal(document.getElementById('editCategoryModal'));
            modal.show();
        });
    });

    // 更新分类
    updateCategoryBtn.addEventListener('click', function () {
        const categoryId = document.getElementById('editCategoryId').value;
        const name = document.getElementById('editCategoryName').value;
        const icon = document.getElementById('editCategoryIcon').value;
        const order = document.getElementById('editCategoryOrder').value;

        if (!name) {
            showNotification('分类名称不能为空', 'warning');
            return;
        }

        API.put(`/api/nav-categories/${categoryId}`, { name, icon, order: parseInt(order) || 0 })
            .then(data => {
                if (data.success) {
                    showNotification(data.message, 'success');
                    location.reload();
                } else {
                    showNotification(data.message || '更新分类失败', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('更新分类时出错', 'danger');
            });
    });

    // 删除分类 - 打开确认模态框
    document.querySelectorAll('.delete-category').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const categoryId = this.getAttribute('data-category-id');
            const categoryName = this.getAttribute('data-category-name');
            document.getElementById('deleteCategoryId').value = categoryId;
            document.getElementById('deleteCategoryConfirmMessage').textContent = `确定要删除分类 "${categoryName}" 吗？此操作将同时删除该分类下的所有导航项，且不可撤销。`;

            const modal = new bootstrap.Modal(document.getElementById('deleteCategoryConfirmModal'));
            modal.show();
        });
    });

    // 确认删除分类
    confirmDeleteCategoryBtn.addEventListener('click', function () {
        const categoryId = document.getElementById('deleteCategoryId').value;

        API.delete(`/api/nav-categories/${categoryId}`)
            .then(data => {
                if (data.success) {
                    showNotification(data.message, 'success');
                    location.reload();
                } else {
                    showNotification(data.message || '删除分类失败', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('删除分类时出错', 'danger');
            });
    });

    // 添加导航项模态框预设分类
    document.querySelectorAll('[data-bs-target="#addNavItemModal"]').forEach(button => {
        button.addEventListener('click', function () {
            const categoryId = this.getAttribute('data-category-id');
            // 确保分类数据已加载
            if (!categories || categories.length === 0) {
                loadCategories().then(() => {
                    if (categoryId) {
                        document.getElementById('navItemCategory').value = categoryId;
                    }
                }).catch(error => {
                    console.error('Error loading categories for add modal:', error);
                    showNotification('加载分类数据失败', 'danger');
                });
            } else {
                populateCategorySelects();
                if (categoryId) {
                    document.getElementById('navItemCategory').value = categoryId;
                }
            }
        });
    });

    // 添加导航项
    saveNavItemBtn.addEventListener('click', function () {
        const title = document.getElementById('navItemTitle').value;
        const url = document.getElementById('navItemUrl').value;
        const description = document.getElementById('navItemDescription').value;
        const icon = document.getElementById('navItemIcon').value;
        const categoryId = document.getElementById('navItemCategory').value;
        const isPublic = document.getElementById('navItemIsPublic').checked;
        const order = document.getElementById('navItemOrder').value;

        if (!title) {
            showNotification('标题不能为空', 'warning');
            return;
        }
        if (!url) {
            showNotification('URL不能为空', 'warning');
            return;
        }
        if (!categoryId) {
            showNotification('请选择分类', 'warning');
            return;
        }

        API.post('/api/nav-items', {
            title, url, description, icon,
            category_id: parseInt(categoryId),
            is_public: isPublic,
            order: parseInt(order) || 0
        })
            .then(data => {
                if (data.success) {
                    showNotification(data.message, 'success');
                    // 关闭模态框
                    const modal = bootstrap.Modal.getInstance(document.getElementById('addNavItemModal'));
                    if (modal) modal.hide();
                    location.reload();
                } else {
                    showNotification(data.message || '创建导航项失败', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('创建导航项时出错', 'danger');
            });
    });

    // 编辑导航项 - 打开模态框
    document.querySelectorAll('.edit-nav-item').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const itemId = this.getAttribute('data-item-id');
            const title = this.getAttribute('data-item-title');
            const url = this.getAttribute('data-item-url');
            const description = this.getAttribute('data-item-description');
            const icon = this.getAttribute('data-item-icon');
            const isPublic = this.getAttribute('data-item-is-public') === 'true';
            const categoryId = this.getAttribute('data-item-category-id');
            const order = this.getAttribute('data-item-order');

            const populateForm = () => {
                document.getElementById('editNavItemId').value = itemId;
                document.getElementById('editNavItemTitle').value = title;
                document.getElementById('editNavItemUrl').value = url;
                document.getElementById('editNavItemDescription').value = description;
                document.getElementById('editNavItemIcon').value = icon;
                document.getElementById('editNavItemIsPublic').checked = isPublic;
                document.getElementById('editNavItemCategory').value = categoryId;
                document.getElementById('editNavItemOrder').value = order;

                const modal = new bootstrap.Modal(document.getElementById('editNavItemModal'));
                modal.show();
            };

            // 确保分类数据已加载
            if (!categories || categories.length === 0) {
                loadCategories().then(() => {
                    populateForm();
                }).catch(error => {
                    console.error('Error loading categories for edit modal:', error);
                    showNotification('加载分类数据失败', 'danger');
                });
            } else {
                populateCategorySelects();
                populateForm();
            }
        });
    });

    // 更新导航项
    updateNavItemBtn.addEventListener('click', function () {
        const itemId = document.getElementById('editNavItemId').value;
        const title = document.getElementById('editNavItemTitle').value;
        const url = document.getElementById('editNavItemUrl').value;
        const description = document.getElementById('editNavItemDescription').value;
        const icon = document.getElementById('editNavItemIcon').value;
        const categoryId = document.getElementById('editNavItemCategory').value;
        const isPublic = document.getElementById('editNavItemIsPublic').checked;
        const order = document.getElementById('editNavItemOrder').value;

        if (!title) {
            showNotification('标题不能为空', 'warning');
            return;
        }
        if (!url) {
            showNotification('URL不能为空', 'warning');
            return;
        }
        if (!categoryId) {
            showNotification('请选择分类', 'warning');
            return;
        }

        API.put(`/api/nav-items/${itemId}`, {
            title, url, description, icon,
            category_id: parseInt(categoryId),
            is_public: isPublic,
            order: parseInt(order) || 0
        })
            .then(data => {
                if (data.success) {
                    showNotification(data.message, 'success');
                    // 关闭模态框
                    const modal = bootstrap.Modal.getInstance(document.getElementById('editNavItemModal'));
                    if (modal) modal.hide();
                    location.reload();
                } else {
                    showNotification(data.message || '更新导航项失败', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('更新导航项时出错', 'danger');
            });
    });

    // 删除导航项 - 打开确认模态框
    document.querySelectorAll('.delete-nav-item').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const itemId = this.getAttribute('data-item-id');
            const itemTitle = this.getAttribute('data-item-title');
            document.getElementById('deleteNavItemId').value = itemId;
            document.getElementById('deleteNavItemConfirmMessage').textContent = `确定要删除导航项 "${itemTitle}" 吗？此操作不可撤销。`;

            const modal = new bootstrap.Modal(document.getElementById('deleteNavItemConfirmModal'));
            modal.show();
        });
    });

    // 确认删除导航项
    confirmDeleteNavItemBtn.addEventListener('click', function () {
        const itemId = document.getElementById('deleteNavItemId').value;

        API.delete(`/api/nav-items/${itemId}`)
            .then(data => {
                if (data.success) {
                    showNotification(data.message, 'success');
                    location.reload();
                } else {
                    showNotification(data.message || '删除导航项失败', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('删除导航项时出错', 'danger');
            });
    });

    // 切换导航项公开/私有状态
    document.querySelectorAll('.toggle-visibility').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const itemId = this.getAttribute('data-item-id');
            const isPublic = this.getAttribute('data-is-public') === 'true';

            API.put(`/api/nav-items/${itemId}/visibility`, { is_public: !isPublic })
                .then(data => {
                    if (data.success) {
                        showNotification(data.message, 'success');
                        location.reload();
                    } else {
                        showNotification(data.message || '更新导航项状态失败', 'danger');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification('更新导航项状态时出错', 'danger');
                });
        });
    });

    // 取消隐藏导航项
    document.querySelectorAll('.unhide-nav-item').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const itemId = this.getAttribute('data-item-id');
            const itemTitle = this.getAttribute('data-item-title');

            if (confirm(`确定要显示导航项 "${itemTitle}" 吗？`)) {
                API.post(`/api/navigation/unhide/${itemId}`, {})
                    .then(data => {
                        if (data.success) {
                            showNotification(data.message, 'success');
                            location.reload();
                        } else {
                            showNotification(data.message || '显示导航项失败', 'danger');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showNotification('显示导航项时出错', 'danger');
                    });
            }
        });
    });
});

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