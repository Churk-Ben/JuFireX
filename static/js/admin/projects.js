// 添加项目
document.addEventListener('DOMContentLoaded', function () {
    // 搜索功能
    document.getElementById('searchInput').addEventListener('input', function () {
        const searchTerm = this.value.toLowerCase();
        const rows = document.querySelectorAll('.table tbody tr');

        rows.forEach(row => {
            const title = row.querySelector('h6').textContent.toLowerCase();
            const description = row.querySelector('small').textContent.toLowerCase();

            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });

    // 项目操作事件委托
    const projectsTable = document.querySelector('.table');
    if (projectsTable) {
        projectsTable.addEventListener('click', function (event) {
            const button = event.target.closest('button');
            if (!button) return;

            const projectId = button.dataset.projectId;

            if (button.classList.contains('toggle-featured')) {
                const isFeatured = button.dataset.isFeatured === 'True';
                toggleFeatured(projectId, isFeatured);
            }

            if (button.classList.contains('edit-project')) {
                editProject(projectId);
            }

            if (button.classList.contains('delete-project')) {
                deleteProject(projectId);
            }
        });
    }

    document.getElementById('addProjectForm').addEventListener('submit', function (e) {
        e.preventDefault()

        const formData = {
            title: document.getElementById('projectTitle').value,
            description: document.getElementById('projectDescription').value,
            github_url: document.getElementById('projectGithub').value,
            demo_url: document.getElementById('projectDemo').value,
            image_url: document.getElementById('projectImage').value,
            is_featured: document.getElementById('projectFeatured').checked
        }

        API.post('/api/projects', formData)
            .then((data) => {
                if (data.success) {
                    showNotification('项目创建成功！', 'success');
                    location.reload()
                } else {
                    showNotification('创建失败：' + data.message, 'error');
                }
            })
            .catch((error) => {
                console.error('Error:', error)
                showNotification('创建失败，请重试', 'error');
            })
    });

    // 编辑项目表单提交
    document.getElementById('editProjectForm').addEventListener('submit', function (e) {
        e.preventDefault()

        const projectId = document.getElementById('editProjectId').value
        const formData = {
            title: document.getElementById('editProjectTitle').value,
            description: document.getElementById('editProjectDescription').value,
            github_url: document.getElementById('editProjectGithub').value,
            demo_url: document.getElementById('editProjectDemo').value,
            image_url: document.getElementById('editProjectImage').value,
            is_featured: document.getElementById('editProjectFeatured').checked
        }

        API.put(`/api/projects/${projectId}`, formData)
            .then((data) => {
                if (data.success) {
                    showNotification('项目更新成功！', 'success');
                    location.reload()
                } else {
                    showNotification('更新失败：' + data.message, 'error');
                }
            })
            .catch((error) => {
                console.error('Error:', error)
                showNotification('更新失败，请重试', 'error');
            })
    });
});

// 切换精选状态
function toggleFeatured(projectId, currentStatus) {
    if (confirm('确定要切换项目的精选状态吗？')) {
        API.put(`/api/projects/${projectId}/featured`, { is_featured: !currentStatus })
            .then((data) => {
                if (data.success) {
                    showNotification('精选状态已更新', 'success');
                    location.reload()
                } else {
                    showNotification('操作失败：' + data.message, 'error');
                }
            })
            .catch((error) => {
                console.error('Error:', error)
                showNotification('操作失败，请重试', 'error');
            })
    }
}

// 编辑项目
function editProject(projectId) {
    // 获取项目详情
    API.get(`/api/projects/${projectId}`)
        .then((data) => {
            if (data.success) {
                const project = data.project

                // 填充表单
                document.getElementById('editProjectId').value = project.id
                document.getElementById('editProjectTitle').value = project.title
                document.getElementById('editProjectDescription').value = project.description
                document.getElementById('editProjectGithub').value = project.github_url || ''
                document.getElementById('editProjectDemo').value = project.demo_url || ''
                document.getElementById('editProjectImage').value = project.image_url || ''
                document.getElementById('editProjectFeatured').checked = project.is_featured

                // 显示模态框
                new bootstrap.Modal(document.getElementById('editProjectModal')).show()
            } else {
                showNotification('获取项目详情失败：' + data.message, 'error');
            }
        })
        .catch((error) => {
            console.error('Error:', error)
            showNotification('获取项目详情失败，请重试', 'error');
        })
}

// 删除项目
function deleteProject(projectId) {
    if (confirm('确定要删除这个项目吗？此操作不可恢复！')) {
        API.delete(`/api/projects/${projectId}`)
            .then((data) => {
                if (data.success) {
                    showNotification('项目删除成功！', 'success');
                    location.reload()
                } else {
                    showNotification('删除失败：' + data.message, 'error');
                }
            })
            .catch((error) => {
                console.error('Error:', error)
                showNotification('删除失败，请重试', 'error');
            })
    }
}