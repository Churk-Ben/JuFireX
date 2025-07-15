document.addEventListener('DOMContentLoaded', function () {
    initializeProjectDocs();
});

function initializeProjectDocs() {
    setupEventListeners();
}

function setupEventListeners() {
    // 使用事件委托处理文档列表中的所有操作
    const docListContainer = document.querySelector('.doc-list-container'); // 假设文档列表都在这个容器里
    if (docListContainer) {
        docListContainer.addEventListener('click', handleDocAction);
    }

    // 上传文档
    document.getElementById('uploadDocBtn')?.addEventListener('click', handleUploadDoc);

    // 新建文档
    document.getElementById('createDocBtn')?.addEventListener('click', handleCreateDoc);

    // 保存编辑后的文档
    document.getElementById('saveDocBtn')?.addEventListener('click', handleSaveDoc);
}

function handleDocAction(e) {
    const target = e.target.closest('.edit-doc, .delete-doc');
    if (!target) return;

    e.preventDefault();
    const docPath = target.dataset.docPath;
    const projectId = getProjectId();

    if (target.classList.contains('edit-doc')) {
        openEditModal(projectId, docPath);
    }

    if (target.classList.contains('delete-doc')) {
        deleteDoc(projectId, docPath);
    }
}

function getProjectId() {
    // 尝试从多个位置获取项目ID，提高稳健性
    const element = document.getElementById('project_id') || document.getElementById('create_project_id') || document.getElementById('edit_project_id');
    if (element) {
        return element.value;
    }
    // 作为后备，从URL解析
    const pathParts = window.location.pathname.split('/');
    const projectIndex = pathParts.indexOf('projects');
    if (projectIndex > -1 && projectIndex + 1 < pathParts.length) {
        return pathParts[projectIndex + 1];
    }
    return null;
}

async function handleUploadDoc() {
    const projectId = getProjectId();
    const docFile = document.getElementById('docFile').files[0];
    const docName = document.getElementById('docName').value;

    if (!docFile || !docName) {
        showNotification('请选择文件并填写文档名称', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('docFile', docFile);
    formData.append('docName', docName);

    try {
        // 文件上传建议保留原生 fetch，因为它对 FormData 的处理更直接
        const response = await fetch(`/api/projects/${projectId}/docs/upload`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            },
            body: formData
        });
        const data = await response.json();
        handleApiResponse(data, '上传成功', '上传失败');
    } catch (error) {
        console.error('上传文档时出错:', error);
        showNotification('上传文档时出错，请稍后重试', 'error');
    }
}

async function handleCreateDoc() {
    const projectId = getProjectId();
    const docTitle = document.getElementById('docTitle').value;
    const docContent = document.getElementById('docContent').value;

    if (!docTitle || !docContent) {
        showNotification('请填写文档标题和内容', 'warning');
        return;
    }

    const payload = { docTitle, docContent };

    try {
        const data = await API.post(`/api/projects/${projectId}/docs/create`, payload);
        handleApiResponse(data, '文档创建成功', '创建失败');
    } catch (error) {
        console.error('创建文档时出错:', error);
        showNotification('创建文档时出错，请稍后重试', 'error');
    }
}

async function openEditModal(projectId, docPath) {
    try {
        const data = await API.get(`/api/projects/${projectId}/docs/${docPath}/raw`);
        if (data.content !== undefined) {
            const editDocModalElement = document.getElementById('editDocModal');
            const editDocModal = new bootstrap.Modal(editDocModalElement);

            document.getElementById('edit_project_id').value = projectId;
            document.getElementById('edit_filename').value = docPath;
            document.getElementById('editDocTitle').value = docPath.endsWith('.md') ? docPath.slice(0, -3) : docPath;
            document.getElementById('editDocContent').value = data.content;

            editDocModal.show();
        } else {
            showNotification(data.message || '无法加载文档内容', 'error');
        }
    } catch (error) {
        console.error('加载文档内容时出错:', error);
        showNotification('加载文档内容时出错', 'error');
    }
}

async function handleSaveDoc() {
    const projectId = document.getElementById('edit_project_id').value;
    const originalFilename = document.getElementById('edit_filename').value;
    const docTitle = document.getElementById('editDocTitle').value;
    const docContent = document.getElementById('editDocContent').value;

    if (!docTitle || !docContent) {
        showNotification('请填写文档标题和内容', 'warning');
        return;
    }

    const payload = { docTitle, docContent };

    try {
        const data = await API.put(`/api/projects/${projectId}/docs/${originalFilename}`, payload);
        if (data.success) {
            const editDocModal = bootstrap.Modal.getInstance(document.getElementById('editDocModal'));
            if (editDocModal) {
                editDocModal.hide();
            }
        }
        handleApiResponse(data, '文档更新成功', '更新失败');
    } catch (error) {
        console.error('更新文档时出错:', error);
        showNotification('更新文档时出错，请稍后重试', 'error');
    }
}

async function deleteDoc(projectId, docPath) {
    if (!confirm(`确定要删除文档 ${docPath} 吗？此操作不可恢复！`)) {
        return;
    }

    try {
        const data = await API.delete(`/api/projects/${projectId}/docs/${docPath}`);
        handleApiResponse(data, '文档删除成功', '删除失败');
    } catch (error) {
        console.error('删除文档时出错:', error);
        showNotification('删除文档时出错，请稍后重试', 'error');
    }
}

function handleApiResponse(data, successMessage, errorMessage) {
    if (data.success) {
        showNotification(data.message || successMessage, 'success');
        setTimeout(() => window.location.reload(), 1500);
    } else {
        showNotification(data.message || errorMessage, 'error');
    }
}