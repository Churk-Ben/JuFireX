document.addEventListener('DOMContentLoaded', function () {
    initializeProfilePage();
});

// 初始化个人资料页面
function initializeProfilePage() {
    setupEventListeners();
    initializeAvatarUploader();
}

// 设置事件监听器
function setupEventListeners() {
    // 保存头像按钮
    document.getElementById('saveAvatarBtn')?.addEventListener('click', handleSaveAvatar);

    // 添加项目表单
    document.getElementById('addProjectForm')?.addEventListener('submit', handleProjectCreation);

    // 使用事件委托处理按钮点击
    document.body.addEventListener('click', function (event) {
        const target = event.target.closest('button');
        if (!target) return;

        // 编辑项目
        if (target.dataset.bsTarget === '#editProjectModal') {
            const projectId = target.dataset.projectId;
            const title = target.dataset.projectTitle;
            const description = target.dataset.projectDescription;
            const githubUrl = target.dataset.projectGithubUrl;
            const demoUrl = target.dataset.projectDemoUrl;
            const isFeatured = target.dataset.projectIsFeatured === 'true';

            document.getElementById('editProjectId').value = projectId;
            document.getElementById('editProjectTitle').value = title;
            document.getElementById('editProjectDescription').value = description;
            document.getElementById('editProjectGithub').value = githubUrl;
            document.getElementById('editProjectDemo').value = demoUrl;
            // 移除精选状态设置，避免在编辑时覆盖精选状态
        }
    });

    // 编辑项目表单
    document.getElementById('editProjectForm')?.addEventListener('submit', handleProjectUpdate);
}

// 初始化头像上传和裁剪功能
function initializeAvatarUploader() {
    const avatarUpload = document.getElementById('avatarUpload');
    const customAvatarUploadBtn = document.getElementById('customAvatarUploadBtn');

    // 点击“选择头像”按钮，触发隐藏的文件输入框
    if (customAvatarUploadBtn) {
        customAvatarUploadBtn.addEventListener('click', () => avatarUpload.click());
    }

    // 初始化 AvatarCropper
    new AvatarCropper({
        imageInput: avatarUpload,
        previewContainer: document.getElementById('avatarPreview'),
        cropButton: document.getElementById('cropAvatarBtn'),
        cancelButton: document.getElementById('cancelCropBtn'),
        resultInput: document.getElementById('croppedAvatarData'),
        cropperContainer: document.getElementById('cropperContainer')
    });
}

// 处理保存头像
function handleSaveAvatar() {
    const croppedData = document.getElementById('croppedAvatarData').value;
    if (!croppedData) {
        showNotification('请先选择并裁剪图片', 'error');
        return;
    }

    API.post('/api/users/avatar', { avatar: croppedData })
        .then(data => {
            if (data.success) {
                showNotification('头像更新成功', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showNotification('头像上传失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('头像上传失败，请重试', 'error');
        });
}

// 处理项目创建
function handleProjectCreation(e) {
    e.preventDefault();

    const formData = {
        title: document.getElementById('projectTitle').value,
        description: document.getElementById('projectDescription').value,
        github_url: document.getElementById('projectGithub').value,
        demo_url: document.getElementById('projectDemo').value,
        image_url: document.getElementById('projectImage').value
    };

    const projectManager = new ProjectManager(API);
    projectManager.createProject(formData)
        .then(data => {
            if (data.success) {
                showNotification('项目创建成功!', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showNotification(data.message || '项目创建失败', 'error');
            }
        })
        .catch(error => {
            showNotification('创建项目时发生错误', 'error');
            console.error('Create project error:', error);
        });
}



// 处理项目更新
function handleProjectUpdate(e) {
    e.preventDefault();

    const projectId = document.getElementById('editProjectId').value;
    const formData = {
        title: document.getElementById('editProjectTitle').value,
        description: document.getElementById('editProjectDescription').value,
        github_url: document.getElementById('editProjectGithub').value,
        demo_url: document.getElementById('editProjectDemo').value,
        image_url: document.getElementById('editProjectImage').value,
        // 移除is_featured字段，避免在编辑时覆盖精选状态
    };

    API.put(`/api/projects/${projectId}`, formData)
        .then(data => {
            if (data.success) {
                showNotification('项目更新成功!', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showNotification(data.message || '项目更新失败', 'error');
            }
        })
        .catch(error => {
            showNotification('更新项目时发生错误', 'error');
            console.error('Update project error:', error);
        });
}

// 删除项目函数
function deleteProject(projectId) {
    if (!confirm('确定要删除这个项目吗？这个操作无法撤销。')) {
        return;
    }

    API.delete(`/api/projects/${projectId}`)
        .then(data => {
            if (data.success) {
                showNotification('项目删除成功！', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showNotification(data.message || '删除项目失败', 'error');
            }
        })
        .catch(error => {
            console.error('Error deleting project:', error);
            showNotification('删除项目时发生错误，请重试', 'error');
        });
}


// 将需要全局访问的函数暴露到 window 对象（如果HTML中直接使用了onclick）
// 如果所有事件都通过 event listener 添加，则此步骤非必需
Object.assign(window, {
    deleteProject
});