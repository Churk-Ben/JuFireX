// 管理导航分类和导航项的JavaScript文件

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

    // 添加分类
    saveCategoryBtn.addEventListener('click', function () {
        const name = document.getElementById('categoryName').value;
        const icon = document.getElementById('categoryIcon').value;
        const order = document.getElementById('categoryOrder').value;

        if (!name) {
            showNotification('分类名称不能为空', 'warning');
            return;
        }

        fetch('/api/nav-categories', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                icon: icon,
                order: parseInt(order) || 0
            })
        })
            .then(response => response.json())
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

        fetch(`/api/nav-categories/${categoryId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                icon: icon,
                order: parseInt(order) || 0
            })
        })
            .then(response => response.json())
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

        fetch(`/api/nav-categories/${categoryId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
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
            if (categoryId) {
                document.getElementById('navItemCategory').value = categoryId;
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

        fetch('/api/nav-items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                url: url,
                description: description,
                icon: icon,
                category_id: parseInt(categoryId),
                is_public: isPublic,
                order: parseInt(order) || 0
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(data.message, 'success');
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

        fetch(`/api/nav-items/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                url: url,
                description: description,
                icon: icon,
                category_id: parseInt(categoryId),
                is_public: isPublic,
                order: parseInt(order) || 0
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(data.message, 'success');
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

        fetch(`/api/nav-items/${itemId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
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

            fetch(`/api/nav-items/${itemId}/visibility`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    is_public: !isPublic
                })
            })
                .then(response => response.json())
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
});