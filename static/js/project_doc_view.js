document.addEventListener('DOMContentLoaded', function () {
    // 获取当前文档信息
    const projectId = document.getElementById('edit_project_id')?.value;
    const filename = document.getElementById('edit_filename')?.value;

    // 编辑文档功能
    const editDocModal = document.getElementById('editDocModal');
    const editDocTitle = document.getElementById('editDocTitle');
    const editDocContent = document.getElementById('editDocContent');
    const saveDocBtn = document.getElementById('saveDocBtn');

    // 当编辑模态框打开时，加载当前文档内容
    if (editDocModal) {
        editDocModal.addEventListener('show.bs.modal', function () {
            // 设置文档标题（去掉.md扩展名）
            const titleWithoutExt = filename.endsWith('.md')
                ? filename.substring(0, filename.length - 3)
                : filename;
            editDocTitle.value = titleWithoutExt;

            // 获取当前页面上的Markdown内容
            const currentContent = document.querySelector('textarea#editDocContent');
            if (!currentContent.value) {
                // 如果内容为空，从页面获取原始内容
                const originalContent = document.querySelector('script#original-content');
                if (originalContent) {
                    editDocContent.value = originalContent.textContent;
                }
            }
        });
    }

    // 保存编辑的文档
    if (saveDocBtn) {
        saveDocBtn.addEventListener('click', function () {
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

            API.put(`/api/projects/${projectId}/docs/${filename}`, data)
                .then(data => {
                    if (data.success) {
                        showNotification(data.message, 'success');
                        if (data.filename !== filename) {
                            setTimeout(() => window.location.href = `/projects/${projectId}/docs/${data.filename}`, 1500);
                        } else {
                            setTimeout(() => window.location.reload(), 1500);
                        }
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

    // 删除文档功能
    const deleteDocBtn = document.getElementById('deleteDocBtn');

    if (deleteDocBtn) {
        deleteDocBtn.addEventListener('click', function () {
            if (confirm(`确定要删除文档 ${filename} 吗？此操作不可恢复！`)) {
                API.delete(`/api/projects/${projectId}/docs/${filename}`)
                    .then(data => {
                        if (data.success) {
                            showNotification(data.message, 'success');
                            setTimeout(() => window.location.href = `/projects/${projectId}/docs`, 1500);
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
    }
});