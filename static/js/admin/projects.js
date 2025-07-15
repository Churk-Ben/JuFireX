document.addEventListener('DOMContentLoaded', function () {
    initializeProjectsPage();
});

function initializeProjectsPage() {
    setupEventListeners();
}

function setupEventListeners() {
    // 搜索功能
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }

    // 项目操作事件委托
    const projectsTable = document.querySelector('.table');
    if (projectsTable) {
        projectsTable.addEventListener('click', handleProjectAction);
    }

    // 添加项目表单提交
    const addProjectForm = document.getElementById('addProjectForm');
    if (addProjectForm) {
        addProjectForm.addEventListener('submit', handleAddProject);
    }

    // 编辑项目表单提交
    const editProjectForm = document.getElementById('editProjectForm');
    if (editProjectForm) {
        editProjectForm.addEventListener('submit', handleEditProject);
    }
}

function handleSearch() {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('.table tbody tr');

    rows.forEach(row => {
        const title = row.querySelector('h6').textContent.toLowerCase();
        const description = row.querySelector('small').textContent.toLowerCase();
        row.style.display = (title.includes(searchTerm) || description.includes(searchTerm)) ? '' : 'none';
    });
}

function handleProjectAction(event) {
    const button = event.target.closest('button');
    if (!button) return;

    const projectId = button.dataset.projectId;
    if (!projectId) return;

    if (button.classList.contains('toggle-featured')) {
        const isFeatured = button.dataset.isFeatured === 'True';
        toggleFeatured(projectId, isFeatured);
    } else if (button.classList.contains('edit-project')) {
        openEditModal(projectId);
    } else if (button.classList.contains('delete-project')) {
        deleteProject(projectId);
    }
}

function handleAddProject(e) {
    e.preventDefault();
    const formData = getFormData('addProjectForm');

    API.post('/api/projects', formData)
        .then(handleApiResponse('项目创建成功！', '创建失败'))
        .catch(handleApiError('创建失败'));
}

function handleEditProject(e) {
    e.preventDefault();
    const projectId = document.getElementById('editProjectId').value;
    const formData = getFormData('editProjectForm');

    API.put(`/api/projects/${projectId}`, formData)
        .then(handleApiResponse('项目更新成功！', '更新失败'))
        .catch(handleApiError('更新失败'));
}

function toggleFeatured(projectId, currentStatus) {
    API.put(`/api/projects/${projectId}/featured`, { is_featured: !currentStatus })
        .then(handleApiResponse('精选状态已更新', '操作失败'))
        .catch(handleApiError('操作失败'));
}

function openEditModal(projectId) {
    API.get(`/api/projects/${projectId}`)
        .then(data => {
            if (data.success) {
                fillEditForm(data.project);
                new bootstrap.Modal(document.getElementById('editProjectModal')).show();
            } else {
                showNotification('获取项目详情失败：' + data.message, 'error');
            }
        })
        .catch(handleApiError('获取项目详情失败'));
}

function deleteProject(projectId) {
    if (!confirm('确定要删除这个项目吗？此操作不可恢复！')) return;

    API.delete(`/api/projects/${projectId}`)
        .then(handleApiResponse('项目删除成功！', '删除失败'))
        .catch(handleApiError('删除失败'));
}

function getFormData(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const featuredCheckbox = form.querySelector('[name="is_featured"]');
    data.is_featured = featuredCheckbox ? featuredCheckbox.checked : false;
    return data;
}

function fillEditForm(project) {
    document.getElementById('editProjectId').value = project.id;
    document.getElementById('editProjectTitle').value = project.title;
    document.getElementById('editProjectDescription').value = project.description;
    document.getElementById('editProjectGithub').value = project.github_url || '';
    document.getElementById('editProjectDemo').value = project.demo_url || '';
    document.getElementById('editProjectImage').value = project.image_url || '';
    document.getElementById('editProjectFeatured').checked = project.is_featured;
}

function handleApiResponse(successMessage, errorMessage) {
    return function (data) {
        if (data.success) {
            showNotification(successMessage, 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(`${errorMessage}：${data.message}`, 'error');
        }
    };
}

function handleApiError(message) {
    return function (error) {
        console.error('Error:', error);
        showNotification(`${message}，请重试`, 'error');
    };
}