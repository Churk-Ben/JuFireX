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
    // 头像上传按钮
    const customAvatarUploadBtn = document.getElementById('customAvatarUploadBtn');
    const avatarUploadInput = document.getElementById('avatarUpload');
    const avatarFileName = document.getElementById('avatarFileName');

    if (customAvatarUploadBtn) {
        customAvatarUploadBtn.addEventListener('click', () => avatarUploadInput.click());
    }
    if (avatarFileName) {
        avatarFileName.addEventListener('click', () => avatarUploadInput.click());
    }
    if (avatarUploadInput) {
        avatarUploadInput.addEventListener('change', handleAvatarFileChange);
    }

    // 保存头像按钮
    document.getElementById('saveAvatarBtn')?.addEventListener('click', handleSaveAvatar);

    // 添加项目表单
    document.getElementById('addProjectForm')?.addEventListener('submit', handleProjectCreation);

    // 使用事件委托处理按钮点击
    document.body.addEventListener('click', function (event) {
        const target = event.target.closest('button');
        if (!target) return;

        // 开通文档空间
        if (target.matches('[onclick^="openDocs"]')) {
            const projectId = target.getAttribute('onclick').match(/\d+/)[0];
            openDocs(projectId);
        }

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
    new AvatarCropper({
        imageInput: document.getElementById('avatarUpload'),
        previewContainer: document.getElementById('avatarPreview'),
        cropButton: document.getElementById('cropAvatarBtn'),
        cancelButton: document.getElementById('cancelCropBtn'),
        resultInput: document.getElementById('croppedAvatarData'),
        cropperContainer: document.getElementById('cropperContainer')
    });
}

// 处理头像文件选择变化
function handleAvatarFileChange() {
    const avatarUploadInput = document.getElementById('avatarUpload');
    const avatarFileName = document.getElementById('avatarFileName');
    if (avatarUploadInput.files.length > 0) {
        avatarFileName.textContent = avatarUploadInput.files[0].name;
        avatarFileName.classList.remove('text-muted');
    } else {
        avatarFileName.textContent = '未选择文件';
        avatarFileName.classList.add('text-muted');
    }
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

// 开通项目文档空间函数
function openDocs(projectId) {
    API.post(`/api/projects/${projectId}/open-docs`)
        .then(data => {
            if (data.success) {
                showNotification('文档空间开通成功！', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showNotification(data.message || '开通文档空间失败', 'error');
            }
        })
        .catch(error => {
            console.error('Error opening docs:', error);
            showNotification('开通文档空间时发生错误，请重试', 'error');
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
    openDocs,
    deleteProject
});