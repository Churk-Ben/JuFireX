document.addEventListener('DOMContentLoaded', function () {
    let cropper;

    function initPasswordStrengthChecker() {
        const passwordInput = document.getElementById('password');
        const strengthBar = document.getElementById('password-strength-bar');
        const strengthText = document.getElementById('password-strength-text');

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
        const cropBtn = document.getElementById('cropBtn');
        const cancelCropBtn = document.getElementById('cancelCropBtn');
        const saveAvatarBtn = document.getElementById('saveAvatarBtn');
        const croppedAvatarData = document.getElementById('croppedAvatarData');
        const avatarUpload = document.getElementById('avatarUpload');
        const avatarModal = new bootstrap.Modal(document.getElementById('avatarModal'));

        previewContainer.addEventListener('click', () => avatarModal.show());

        avatarUpload.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (!file || !file.type.match('image.*')) {
                showNotification('请选择有效的图片文件！', 'error');
                return;
            }

            const reader = new FileReader();
            reader.onload = function (e) {
                cropperContainer.style.display = 'block';
                cropperContainer.innerHTML = '';
                const img = document.createElement('img');
                img.id = 'cropperImage';
                img.src = e.target.result;
                img.style.maxWidth = '100%';
                cropperContainer.appendChild(img);

                if (cropper) cropper.destroy();
                cropper = new Cropper(img, { aspectRatio: 1, viewMode: 1 });

                cropBtn.style.display = 'inline-block';
                saveAvatarBtn.style.display = 'none';
            };
            reader.readAsDataURL(file);
        });

        cropBtn.addEventListener('click', function () {
            if (!cropper) return;
            const canvas = cropper.getCroppedCanvas({ width: 200, height: 200 });
            const croppedImageUrl = canvas.toDataURL('image/jpeg');

            modalPreviewContainer.innerHTML = '';
            const modalImg = document.createElement('img');
            modalImg.src = croppedImageUrl;
            modalImg.style.width = '100%';
            modalImg.style.height = '100%';
            modalImg.style.objectFit = 'cover';
            modalPreviewContainer.appendChild(modalImg);

            croppedAvatarData.value = croppedImageUrl;
            cropperContainer.style.display = 'none';
            cropBtn.style.display = 'none';
            saveAvatarBtn.style.display = 'inline-block';
            cropper.destroy();
            cropper = null;
        });

        cancelCropBtn.addEventListener('click', function () {
            if (cropper) {
                cropper.destroy();
                cropper = null;
            }
            cropperContainer.style.display = 'none';
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
            img.style.width = '100%';
            img.style.height = '100%';
            img.style.objectFit = 'cover';
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
                this.classList.remove('is-valid', 'is-invalid');
            } else if (password === confirmPassword) {
                helpText.textContent = '密码匹配 ✓';
                helpText.className = 'form-text text-success';
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
            } else {
                helpText.textContent = '密码不匹配 ✗';
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

            if (document.getElementById('password').value !== document.getElementById('confirm_password').value) {
                showNotification('两次输入的密码不一致！', 'error');
                return;
            }

            const formData = new FormData(this);
            const croppedAvatarDataValue = document.getElementById('croppedAvatarData').value;
            if (croppedAvatarDataValue) {
                formData.delete('avatar');
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

            const submitBtn = document.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>处理中...';
            submitBtn.disabled = true;

            fetch('/register', {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                body: formData,
            })
            .then(response => {
                if (response.redirected) {
                    showNotification('注册成功！正在跳转到登录页面...', 'success');
                    setTimeout(() => { window.location.href = response.url; }, 1500);
                    return null;
                }
                return response.json();
            })
            .then(data => {
                if (!data) return;
                if (data.success) {
                    showNotification('注册成功！正在跳转到登录页面...', 'success');
                    setTimeout(() => { window.location.href = "/login"; }, 1500);
                } else {
                    submitBtn.innerHTML = originalBtnText;
                    submitBtn.disabled = false;
                    showNotification(data.message || '注册失败，请重试', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
                showNotification('注册时发生未知错误，请稍后重试。', 'error');
            });
        });
    }

    initPasswordStrengthChecker();
    initPasswordToggle();
    initAvatarUpload();
    initFormValidation();
});