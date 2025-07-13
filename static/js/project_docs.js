document.addEventListener('DOMContentLoaded', function () {
    // 上传文档功能
    const uploadDocBtn = document.getElementById('uploadDocBtn');
    if (uploadDocBtn) {
        uploadDocBtn.addEventListener('click', function () {
            const projectId = document.getElementById('project_id').value;
            const docFile = document.getElementById('docFile').files[0];
            const docName = document.getElementById('docName').value;

            if (!docFile || !docName) {
                showNotification('请选择文件并填写文档名称', 'warning');
                return;
            }

            const formData = new FormData();
            formData.append('docFile', docFile);
            formData.append('docName', docName);

            fetch(`/api/projects/${projectId}/docs/upload`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification(data.message, 'success');
                        setTimeout(() => window.location.reload(), 1500);
                    } else {
                        showNotification(data.message, 'error');
                    }
                })
                .catch(error => {
                    console.error('上传文档时出错:', error);
                    showNotification('上传文档时出错，请稍后重试', 'error');
                });
        });
    }

    // 新建文档功能
    const createDocBtn = document.getElementById('createDocBtn');
    if (createDocBtn) {
        createDocBtn.addEventListener('click', function () {
            const projectId = document.getElementById('create_project_id').value;
            const docTitle = document.getElementById('docTitle').value;
            const docContent = document.getElementById('docContent').value;

            if (!docTitle || !docContent) {
                showNotification('请填写文档标题和内容', 'warning');
                return;
            }

            const data = {
                docTitle: docTitle,
                docContent: docContent
            };

            API.post(`/api/projects/${projectId}/docs/create`, data)
                .then(data => {
                    if (data.success) {
                        showNotification(data.message, 'success');
                        setTimeout(() => window.location.reload(), 1500);
                    } else {
                        showNotification(data.message, 'error');
                    }
                })
                .catch(error => {
                    console.error('创建文档时出错:', error);
                    showNotification('创建文档时出错，请稍后重试', 'error');
                });
        });
    }

    // 编辑文档功能
    const editDocModalElement = document.getElementById('editDocModal');
    if (editDocModalElement) {
        const editDocModal = new bootstrap.Modal(editDocModalElement);
        const editDocTitle = document.getElementById('editDocTitle');
        const editDocContent = document.getElementById('editDocContent');
        const saveDocBtn = document.getElementById('saveDocBtn');
        const projectIdForEdit = document.getElementById('edit_project_id');
        const filenameForEdit = document.getElementById('edit_filename');

        document.querySelectorAll('.edit-doc').forEach(button => {
            button.addEventListener('click', function () {
                const docPath = this.dataset.docPath;
                const projectId = window.location.pathname.split('/')[2];

                // API请求获取原始文档内容
                API.get(`/api/projects/${projectId}/docs/${docPath}/raw`)
                    .then(data => {
                        if (data.content !== undefined) {
                            projectIdForEdit.value = projectId;
                            filenameForEdit.value = docPath;

                            const titleWithoutExt = docPath.endsWith('.md')
                                ? docPath.substring(0, docPath.length - 3)
                                : docPath;
                            editDocTitle.value = titleWithoutExt;
                            editDocContent.value = data.content;

                            editDocModal.show();
                        } else {
                            showNotification(data.message || '无法加载文档内容', 'error');
                        }
                    })
                    .catch(error => {
                        console.error('加载文档内容时出错:', error);
                        showNotification('加载文档内容时出错', 'error');
                    });
            });
        });

        if (saveDocBtn) {
            saveDocBtn.addEventListener('click', function () {
                const projectId = projectIdForEdit.value;
                const originalFilename = filenameForEdit.value;
                const docTitle = editDocTitle.value;
                const docContent = editDocContent.value;

                if (!docTitle || !docContent) {
                    showNotification('请填写文档标题和内容', 'warning');
                    return;
                }

                const data = {
                    docTitle: docTitle,
                    docContent: docContent
                };

                API.put(`/api/projects/${projectId}/docs/${originalFilename}`, data)
                    .then(data => {
                        if (data.success) {
                            showNotification(data.message, 'success');
                            editDocModal.hide();
                            setTimeout(() => window.location.reload(), 1500);
                        } else {
                            showNotification(data.message, 'error');
                        }
                    })
                    .catch(error => {
                        console.error('更新文档时出错:', error);
                        showNotification('更新文档时出错，请稍后重试', 'error');
                    });
            });
        }
    }

    // 删除文档功能
    const deleteButtons = document.querySelectorAll('.delete-doc');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const docPath = this.dataset.docPath;
            const projectId = window.location.pathname.split('/')[2];

            if (confirm(`确定要删除文档 ${docPath} 吗？此操作不可恢复！`)) {
                API.delete(`/api/projects/${projectId}/docs/${docPath}`)
                    .then(data => {
                        if (data.success) {
                            showNotification(data.message, 'success');
                            setTimeout(() => window.location.reload(), 1500);
                        } else {
                            showNotification(data.message, 'error');
                        }
                    })
                    .catch(error => {
                        console.error('删除文档时出错:', error);
                        showNotification('删除文档时出错，请稍后重试', 'error');
                    });
            }
        });
    });
});