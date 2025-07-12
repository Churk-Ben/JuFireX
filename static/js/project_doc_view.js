document.addEventListener('DOMContentLoaded', function () {
    // 获取CSRF令牌
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

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
                alert('请填写文档标题和内容');
                return;
            }

            // 发送更新请求
            fetch(`/api/projects/${projectId}/docs/${filename}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    docTitle: docTitle,
                    docContent: docContent
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // 更新成功，刷新页面或重定向
                        alert(data.message);
                        if (data.filename !== filename) {
                            // 如果文件名已更改，重定向到新的URL
                            window.location.href = `/projects/${projectId}/docs/${data.filename}`;
                        } else {
                            // 否则刷新当前页面
                            window.location.reload();
                        }
                    } else {
                        // 更新失败，显示错误信息
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('更新文档时出错:', error);
                    alert('更新文档时出错，请稍后重试');
                });
        });
    }

    // 删除文档功能
    const deleteDocBtn = document.getElementById('deleteDocBtn');

    if (deleteDocBtn) {
        deleteDocBtn.addEventListener('click', function () {
            if (confirm(`确定要删除文档 ${filename} 吗？此操作不可恢复！`)) {
                // 发送删除请求
                fetch(`/api/projects/${projectId}/docs/${filename}`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // 删除成功，返回文档列表页面
                            alert(data.message);
                            window.location.href = `/projects/${projectId}/docs`;
                        } else {
                            // 删除失败，显示错误信息
                            alert(data.message);
                        }
                    })
                    .catch(error => {
                        console.error('删除文档时出错:', error);
                        alert('删除文档时出错，请稍后重试');
                    });
            }
        });
    }
});