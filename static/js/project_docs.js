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

            // 使用fetch上传文件，因为API类目前不支持FormData
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
    const createDocForm = document.getElementById('createDocForm');
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
});