document.addEventListener('DOMContentLoaded', function () {
    // 获取CSRF令牌
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // 上传文档功能
    const uploadDocForm = document.getElementById('uploadDocForm');
    const uploadDocBtn = document.getElementById('uploadDocBtn');

    if (uploadDocBtn) {
        uploadDocBtn.addEventListener('click', function () {
            const projectId = document.getElementById('project_id').value;
            const docFile = document.getElementById('docFile').files[0];
            const docName = document.getElementById('docName').value;

            if (!docFile || !docName) {
                alert('请选择文件并填写文档名称');
                return;
            }

            // 创建FormData对象
            const formData = new FormData();
            formData.append('docFile', docFile);
            formData.append('docName', docName);

            // 发送上传请求
            fetch(`/api/projects/${projectId}/docs/upload`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // 上传成功，刷新页面
                        alert(data.message);
                        window.location.reload();
                    } else {
                        // 上传失败，显示错误信息
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('上传文档时出错:', error);
                    alert('上传文档时出错，请稍后重试');
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
                alert('请填写文档标题和内容');
                return;
            }

            // 发送创建请求
            fetch(`/api/projects/${projectId}/docs/create`, {
                method: 'POST',
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
                        // 创建成功，刷新页面
                        alert(data.message);
                        window.location.reload();
                    } else {
                        // 创建失败，显示错误信息
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('创建文档时出错:', error);
                    alert('创建文档时出错，请稍后重试');
                });
        });
    }
});