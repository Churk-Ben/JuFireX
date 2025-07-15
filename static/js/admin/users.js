document.addEventListener('DOMContentLoaded', function () {
    initializeUsersPage();
});

function initializeUsersPage() {
    setupEventListeners();
}

function setupEventListeners() {
    // 搜索功能
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }

    // 角色变更
    document.querySelectorAll('.role-select').forEach(select => {
        select.dataset.originalIndex = select.selectedIndex;
        select.addEventListener('change', handleRoleChange);
    });

    // 用户操作事件委托
    const usersTable = document.getElementById('usersTable');
    if (usersTable) {
        usersTable.addEventListener('click', handleUserAction);
    }
}

function handleSearch() {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('#usersTable tbody tr');

    rows.forEach(row => {
        const username = row.querySelector('h6').textContent.toLowerCase();
        const email = row.querySelector('small').textContent.toLowerCase();
        row.style.display = (username.includes(searchTerm) || email.includes(searchTerm)) ? '' : 'none';
    });
}

function handleRoleChange() {
    const userId = this.dataset.userId;
    const newRole = this.value;

    if (confirm('确定要修改用户角色吗？')) {
        updateUserRole(userId, newRole);
    } else {
        this.selectedIndex = this.dataset.originalIndex || 0;
    }
}

function handleUserAction(event) {
    const button = event.target.closest('button');
    if (!button) return;

    const userId = button.dataset.userId;
    if (!userId) return;

    if (button.classList.contains('toggle-user-status')) {
        const isActive = button.dataset.isActive === 'True';
        toggleUserStatus(userId, isActive);
    } else if (button.classList.contains('delete-user')) {
        deleteUser(userId);
    }
}

function updateUserRole(userId, role) {
    API.put(`/api/users/${userId}/role`, { role: parseInt(role) })
        .then(handleApiResponse('用户角色更新成功！', '更新失败', true))
        .catch(handleApiError('更新失败', true));
}

function toggleUserStatus(userId, currentStatus) {
    const action = currentStatus ? '禁用' : '启用';
    if (!confirm(`确定要${action}这个用户吗？`)) return;

    API.put(`/api/users/${userId}/status`, { is_active: !currentStatus })
        .then(handleApiResponse(`用户${action}成功！`, `${action}失败`))
        .catch(handleApiError(`${action}失败`));
}


function deleteUser(userId) {
    if (!confirm('确定要删除这个用户吗？此操作不可恢复！\n\n注意：删除用户将同时删除其所有项目。')) return;

    API.delete(`/api/users/${userId}`)
        .then(handleApiResponse('用户删除成功！', '删除失败'))
        .catch(handleApiError('删除失败'));
}


function handleApiResponse(successMessage, errorMessage, reloadOnError = false) {
    return function (data) {
        if (data.success) {
            showNotification(successMessage, 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(`${errorMessage}：${data.message}`, 'error');
            if (reloadOnError) setTimeout(() => location.reload(), 1000);
        }
    };
}

function handleApiError(message, reloadOnError = false) {
    return function (error) {
        console.error('Error:', error);
        showNotification(`${message}，请重试`, 'error');
        if (reloadOnError) setTimeout(() => location.reload(), 1000);
    };
}

// 将需要全局访问的函数暴露到 window 对象
Object.assign(window, {
    toggleUserStatus,
    deleteUser
});