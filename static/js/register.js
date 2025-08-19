document.addEventListener('DOMContentLoaded', function () {
    // 初始化步骤切换
    function initStepSwitching() {
        const step1 = document.getElementById('step1');
        const step2 = document.getElementById('step2');
        const step1Indicator = document.getElementById('step1Indicator');
        const step2Indicator = document.getElementById('step2Indicator');
        const nextToStep2Btn = document.getElementById('nextToStep2');
        const backToStep1Btn = document.getElementById('backToStep1');
        const progressBar = document.getElementById('registerProgress');

        // 前往第二步
        nextToStep2Btn.addEventListener('click', function () {
            // 验证第一步表单
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            const agree = document.getElementById('agree').checked;

            if (!username || !email || !password || !confirmPassword) {
                showNotification('请填写所有必填字段', 'error');
                return;
            }

            if (password !== confirmPassword) {
                showNotification('两次输入的密码不一致', 'error');
                return;
            }

            if (!agree) {
                showNotification('请阅读并同意使用条款和隐私政策', 'error');
                return;
            }

            // 切换到第二步
            step1.classList.remove('active');
            step2.classList.add('active');
            step1Indicator.classList.remove('active');
            step2Indicator.classList.add('active');
            progressBar.style.width = '100%';
        });

        // 返回第一步
        backToStep1Btn.addEventListener('click', function () {
            step2.classList.remove('active');
            step1.classList.add('active');
            step2Indicator.classList.remove('active');
            step1Indicator.classList.add('active');
            progressBar.style.width = '50%';
        });

        // 初始化进度条
        progressBar.style.width = '50%';
    }

    function initPasswordStrengthCheck() {
        const passwordInput = document.getElementById('password');
        const strengthBar = document.getElementById('passwordStrength');
        const strengthText = document.getElementById('passwordStrengthText');

        passwordInput.addEventListener('input', function () {
            const password = this.value;
            let score = 0;
            if (password.length >= 8) score++;
            if (/[a-z]/.test(password)) score++;
            if (/[A-Z]/.test(password)) score++;
            if (/[0-9]/.test(password)) score++;
            if (/[^a-zA-Z0-9]/.test(password)) score++;

            const percentage = (score / 5) * 100;
            strengthBar.style.width = percentage + '%';

            if (password.length === 0) {
                strengthBar.className = 'progress-bar';
                strengthText.textContent = '密码强度: 未设置';
            } else if (percentage < 30) {
                strengthBar.className = 'progress-bar bg-danger';
                strengthText.textContent = '密码强度: 弱';
            } else if (percentage < 60) {
                strengthBar.className = 'progress-bar bg-warning';
                strengthText.textContent = '密码强度: 中';
            } else {
                strengthBar.className = 'progress-bar bg-success';
                strengthText.textContent = '密码强度: 强';
            }
        });
    }

    function initPasswordToggle() {
        const toggleBtn = document.getElementById('togglePassword');
        const passwordInput = document.getElementById('password');

        toggleBtn.addEventListener('click', function () {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            const icon = toggleBtn.querySelector('i');
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
        });
    }

    function initAvatarUpload() {
        const previewContainer = document.getElementById('avatarPreview');
        const modalPreviewContainer = document.getElementById('modalAvatarPreview');
        const cropperContainer = document.getElementById('cropperContainer');
        const cropAvatarBtn = document.getElementById('cropAvatarBtn');
        const cancelCropBtn = document.getElementById('cancelCropBtn');
        const saveAvatarBtn = document.getElementById('saveAvatarBtn');
        const croppedAvatarData = document.getElementById('croppedAvatarData');
        const avatarUpload = document.getElementById('avatarUpload');
        const customAvatarUploadBtn = document.getElementById('customAvatarUploadBtn');
        const avatarModal = new bootstrap.Modal(document.getElementById('avatarModal'));

        previewContainer.addEventListener('click', () => avatarModal.show());
        customAvatarUploadBtn.addEventListener('click', () => avatarUpload.click());

        // 使用AvatarCropper类处理头像裁剪
        const avatarCropper = new AvatarCropper({
            imageInput: avatarUpload,
            previewContainer: modalPreviewContainer,
            cropButton: cropAvatarBtn,
            cancelButton: cancelCropBtn,
            resultInput: croppedAvatarData,
            cropperContainer: cropperContainer
        });

        saveAvatarBtn.addEventListener('click', function () {
            const croppedData = croppedAvatarData.value;
            if (!croppedData) {
                showNotification('请先选择并裁剪图片', 'error');
                return;
            }

            previewContainer.innerHTML = '';
            const img = document.createElement('img');
            img.src = croppedData;
            img.classList.add('avatar');
            previewContainer.appendChild(img);

            avatarModal.hide();
            showNotification('头像设置成功', 'success');
        });
    }

    function initFormValidation() {
        document.getElementById('confirm_password').addEventListener('input', function () {
            const password = document.getElementById('password').value;
            const confirmPassword = this.value;
            const helpText = document.getElementById('passwordHelp');

            if (confirmPassword === '') {
                helpText.textContent = '';
                helpText.className = 'form-text text-muted';
                this.classList.remove('is-valid', 'is-invalid');
            } else if (password === confirmPassword) {
                helpText.className = 'form-text text-success';
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
            } else {
                helpText.className = 'form-text text-danger';
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
            }
        });

        document.getElementById('registerForm').addEventListener('submit', function (e) {
            e.preventDefault();

            if (!document.getElementById('agree').checked) {
                showNotification('请阅读并同意使用条款和隐私政策', 'error');
                return;
            }

            const password = document.getElementById('password').value.trim();
            if (!password) {
                showNotification('密码不能为空', 'error');
                return;
            }

            if (password !== document.getElementById('confirm_password').value.trim()) {
                showNotification('两次输入的密码不一致! ', 'error');
                return;
            }

            const formData = new FormData();
            // 手动添加表单字段
            formData.append('username', document.getElementById('username').value.trim());
            formData.append('email', document.getElementById('email').value.trim());
            formData.append('password', password);

            // 处理头像
            const croppedAvatarDataValue = document.getElementById('croppedAvatarData').value;
            if (croppedAvatarDataValue) {
                const byteString = atob(croppedAvatarDataValue.split(',')[1]);
                const mimeString = croppedAvatarDataValue.split(',')[0].split(':')[1].split(';')[0];
                const ab = new ArrayBuffer(byteString.length);
                const ia = new Uint8Array(ab);
                for (let i = 0; i < byteString.length; i++) {
                    ia[i] = byteString.charCodeAt(i);
                }
                const blob = new Blob([ab], { type: mimeString });
                formData.append('avatar', blob, 'avatar.jpg');
            }

            // 添加其他可选字段
            const joinIntention = document.getElementById('join_intention');
            if (joinIntention.checked) {
                formData.append('join_intention', 'true');
                const studioIntention = document.getElementById('studio_intention').value.trim();
                if (studioIntention) {
                    formData.append('studio_intention', studioIntention);
                }
            }

            const submitBtn = document.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>处理中...';
            submitBtn.disabled = true;

            API.request('/register', {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                body: formData
            })
                .then(response => {
                    if (response.redirected) {
                        showNotification('注册成功! 正在跳转到登录页面...', 'success');
                        setTimeout(() => { window.location.href = response.url; }, 1500);
                        return;
                    }

                    if (response.success) {
                        showNotification('注册成功! 正在跳转到登录页面...', 'success');
                        setTimeout(() => { window.location.href = "/login"; }, 1500);
                    } else {
                        throw new Error(response.message || '注册失败，请重试');
                    }
                })

                .catch(error => {
                    console.error('Error:', error);
                    submitBtn.innerHTML = originalBtnText;
                    submitBtn.disabled = false;
                    showNotification(error.message || '注册时发生未知错误，请稍后重试。', 'error');
                });
        });
    }

    function initJoinIntentionToggle() {
        const joinCheckbox = document.getElementById('join_intention');
        const intentionDetails = document.getElementById('selfIntroduction');

        joinCheckbox.addEventListener('change', function () {
            if (this.checked) {
                intentionDetails.classList.add('show');
            } else {
                intentionDetails.classList.remove('show');
                // 清空输入框内容
                document.getElementById('studio_intention').value = '';
            }
        });
    }

    initStepSwitching();
    initPasswordStrengthCheck();
    initPasswordToggle();
    initAvatarUpload();
    initFormValidation();
    initJoinIntentionToggle();
});