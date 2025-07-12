// 搜索功能
document.getElementById('searchInput').addEventListener('input', function () {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('#usersTable tbody tr');

    rows.forEach(row => {
        const username = row.querySelector('h6').textContent.toLowerCase();
        const email = row.querySelector('small').textContent.toLowerCase();

        if (username.includes(searchTerm) || email.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// 角色变更
document.querySelectorAll('.role-select').forEach(select => {
    select.addEventListener('change', function () {
        const userId = this.dataset.userId;
        const newRole = this.value;

        if (confirm('确定要修改用户角色吗？')) {
            updateUserRole(userId, newRole);
        } else {
            // 恢复原值
            this.selectedIndex = this.dataset.originalIndex || 0;
        }
    });

    // 保存原始选中索引
    select.dataset.originalIndex = select.selectedIndex;
});

// 更新用户角色
function updateUserRole(userId, role) {
    API.put(`/api/users/${userId}/role`, { role: parseInt(role) })
        .then(data => {
            if (data.success) {
                showNotification('用户角色更新成功！', 'success');
                location.reload();
            } else {
                showNotification('更新失败：' + data.message, 'error');
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('更新失败，请重试', 'error');
            location.reload();
        });
}

// 切换用户状态
function toggleUserStatus(userId, currentStatus) {
    const action = currentStatus ? '禁用' : '启用';
    if (confirm(`确定要${action}这个用户吗？`)) {
        API.put(`/api/users/${userId}/status`, { is_active: !currentStatus })
            .then(data => {
                if (data.success) {
                    showNotification(`用户${action}成功！`, 'success');
                    location.reload();
                } else {
                    showNotification(`${action}失败：` + data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification(`${action}失败，请重试`, 'error');
            });
    }
}

// 查看用户详情
function viewUserDetails(userId) {
    API.get(`/api/users/${userId}`)
        .then(data => {
            if (data.success) {
                const user = data.user;
                const avatarHtml = user.avatar_path ?
                    `<img src="/uploads/avatars/${user.avatar_path}" alt="${user.username}的头像" class="rounded-circle" style="width: 80px; height: 80px; object-fit: cover; border: 3px solid var(--github-accent);">` :
                    `<i class="fas fa-user-circle" style="font-size: 4rem; color: var(--github-accent)"></i>`;

                const content = `
                <div class="card mb-4 border-0">
                    <div class="card-body">
                        <div class="d-flex align-items-center mb-4">
                            <div class="me-3">
                                ${avatarHtml}
                            </div>
                            <div>
                                <h4 class="mb-1">${user.username}</h4>
                                <p class="text-muted mb-0">${user.email}</p>
                                <div class="mt-1">
                                    <span class="badge bg-${user.is_active ? 'success' : 'danger'} me-2">${user.is_active ? '活跃' : '禁用'}</span>
                                    <span class="badge" style="background-color: var(--github-accent);">${user.role_name}</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row mt-4">
                            <div class="col-md-6">
                                <div class="card" style="background-color: rgba(88, 166, 255, 0.1); border-color: var(--github-accent);">
                                    <div class="card-body">
                                        <h6 class="card-title"><i class="fas fa-info-circle me-2"></i>基本信息</h6>
                                        <hr style="border-color: rgba(88, 166, 255, 0.3);">
                                        <p><strong>注册时间：</strong> ${user.created_at}</p>
                                        <p><strong>活跃天数：</strong> ${user.active_days} 天</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card" style="background-color: rgba(88, 166, 255, 0.1); border-color: var(--github-accent);">
                                    <div class="card-body">
                                        <h6 class="card-title"><i class="fas fa-chart-bar me-2"></i>统计信息</h6>
                                        <hr style="border-color: rgba(88, 166, 255, 0.3);">
                                        <p><strong>项目数量：</strong> ${user.project_count}</p>
                                        <p><strong>精选项目：</strong> ${user.featured_project_count}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="d-flex justify-content-end mt-3">
                    <button class="btn btn-sm btn-outline-warning me-2" onclick="toggleUserStatus(${user.id}, ${user.is_active})">
                        <i class="fas fa-${user.is_active ? 'ban' : 'check'} me-1"></i>
                        ${user.is_active ? '禁用用户' : '启用用户'}
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteUser(${user.id})">
                        <i class="fas fa-trash me-1"></i>
                        删除用户
                    </button>
                </div>
            `;
                document.getElementById('userDetailsContent').innerHTML = content;
                new bootstrap.Modal(document.getElementById('userDetailsModal')).show();
            } else {
                showNotification('获取用户详情失败：' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('获取用户详情失败，请重试', 'error');
        });
}

// 删除用户
function deleteUser(userId) {
    if (confirm('确定要删除这个用户吗？此操作不可恢复！\n\n注意：删除用户将同时删除其所有项目。')) {
        API.delete(`/api/users/${userId}`)
            .then(data => {
                if (data.success) {
                    showNotification('用户删除成功！', 'success');
                    location.reload();
                } else {
                    showNotification('删除失败：' + data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('删除失败，请重试', 'error');
            });
    }
}