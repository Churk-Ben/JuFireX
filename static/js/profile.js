document.addEventListener('DOMContentLoaded', function () {
    // 初始化头像上传和裁剪功能
    const avatarCropper = new AvatarCropper({
        imageInput: document.getElementById('avatarUpload'),
        previewContainer: document.getElementById('avatarPreview'),
        cropButton: document.getElementById('cropAvatarBtn'),
        cancelButton: document.getElementById('cancelCropBtn'),
        resultInput: document.getElementById('croppedAvatarData'),
        cropperContainer: document.getElementById('cropperContainer')
    });

    // 保存头像按钮
    const saveAvatarBtn = document.getElementById('saveAvatarBtn');
    if (saveAvatarBtn) {
        saveAvatarBtn.addEventListener('click', function () {
            const croppedData = document.getElementById('croppedAvatarData').value;
            if (!croppedData) {
                showNotification('请先选择并裁剪图片', 'error');
                return;
            }

            API.post('/api/users/avatar', { avatar: croppedData })
                .then(data => {
                    if (data.success) {
                        const avatarContainer = document.getElementById('avatarContainer');
                        const oldAvatar = avatarContainer.querySelector('img, i.fas.fa-user-circle');
                        if (oldAvatar) {
                            oldAvatar.remove();
                        }

                        const newAvatar = document.createElement('img');
                        newAvatar.src = data.avatar_url;
                        newAvatar.alt = '用户头像';
                        newAvatar.className = 'rounded-circle';
                        newAvatar.style.width = '120px';
                        newAvatar.style.height = '120px';
                        newAvatar.style.objectFit = 'cover';

                        const button = avatarContainer.querySelector('button');
                        avatarContainer.insertBefore(newAvatar, button);

                        const modal = bootstrap.Modal.getInstance(document.getElementById('avatarModal'));
                        modal.hide();

                        showNotification('头像更新成功', 'success');

                        setTimeout(() => {
                            location.reload();
                        }, 1500);
                    } else {
                        showNotification('头像上传失败: ' + data.message, 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification('头像上传失败，请重试', 'error');
                });
        });
    }

    // 添加项目表单
    const addProjectForm = document.getElementById('addProjectForm');
    if (addProjectForm) {
        addProjectForm.addEventListener('submit', function (e) {
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
        });
    }
});