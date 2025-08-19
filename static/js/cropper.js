// 头像裁剪功能的JavaScript代码

class AvatarCropper {
    constructor(options) {
        this.imageInput = options.imageInput;
        this.previewContainer = options.previewContainer;
        this.cropButton = options.cropButton;
        this.cancelButton = options.cancelButton;
        this.resultInput = options.resultInput;
        this.cropperContainer = options.cropperContainer;
        this.cropperImage = null;
        this.cropper = null;
        this.croppedImageUrl = null;

        this.init();
    }

    init() {
        // 监听文件选择
        this.imageInput.addEventListener('change', this.handleFileSelect.bind(this));

        // 监听重置按钮
        if (this.cancelButton) {
            this.cancelButton.addEventListener('click', this.cancelCrop.bind(this));
        }

        // 监听裁剪按钮
        if (this.cropButton) {
            this.cropButton.addEventListener('click', this.cropImage.bind(this));
        }

        // 获取初始头像URL
        const img = this.previewContainer.querySelector('img');
        this.initialAvatarUrl = img ? img.src : null;
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (!file) return;

        // 检查文件类型
        if (!file.type.match('image.*')) {
            showNotification('请上传图片文件', 'warning');
            return;
        }

        // 创建文件阅读器
        const reader = new FileReader();
        reader.onload = (e) => {
            // 显示裁剪容器
            this.cropperContainer.style.display = 'block';

            // 创建图片元素
            if (this.cropperImage) {
                this.cropperImage.src = e.target.result;
            } else {
                this.cropperImage = document.createElement('img');
                this.cropperImage.id = 'cropperImage';
                this.cropperImage.src = e.target.result;
                this.cropperContainer.appendChild(this.cropperImage);
            }

            // 初始化裁剪器
            if (this.cropper) {
                this.cropper.destroy();
            }

            this.cropper = new Cropper(this.cropperImage, {
                aspectRatio: 1,
                viewMode: 1,
                dragMode: 'move',
                autoCropArea: 0.8,
                restore: false,
                guides: true,
                center: true,
                highlight: true,
                cropBoxMovable: true,
                cropBoxResizable: true,
                toggleDragModeOnDblclick: false,
                background: true, // 显示背景网格
                modal: true, // 显示黑色模态背景
            });

            // 更新文件名显示
            const avatarFileName = document.getElementById('avatarFileName');
            if (avatarFileName) {
                avatarFileName.textContent = '已加载图像';
                avatarFileName.classList.remove('text-muted');
            }
        };

        reader.readAsDataURL(file);
    }

    cropImage() {
        if (!this.cropper) return;

        // 获取裁剪后的图像
        const canvas = this.cropper.getCroppedCanvas({
            width: 120,
            height: 120,
            minWidth: 100,
            minHeight: 100,
            maxWidth: 500,
            maxHeight: 500,
            fillColor: '#fff',
            imageSmoothingEnabled: true,
            imageSmoothingQuality: 'high',
        });

        // 转换为base64
        this.croppedImageUrl = canvas.toDataURL('image/jpeg');

        // 显示预览
        this.previewContainer.innerHTML = '';
        const img = document.createElement('img');
        img.src = this.croppedImageUrl;
        img.classList.add('avatar');
        this.previewContainer.appendChild(img);

        // 设置隐藏输入值
        if (this.resultInput) {
            this.resultInput.value = this.croppedImageUrl;
        }

        // 隐藏裁剪容器
        this.cropperContainer.style.display = 'none';

        // 销毁裁剪器
        this.cropper.destroy();
        this.cropper = null;
    }

    cancelCrop() {
        // 清空裁剪器
        if (this.cropper) {
            this.cropper.destroy();
            this.cropper = null;
        }

        // 清空裁剪容器
        this.cropperContainer.style.display = 'none';

        // 清空文件输入
        this.imageInput.value = '';

        // 还原初始头像
        this.previewContainer.innerHTML = '';
        if (this.initialAvatarUrl) {
            const img = document.createElement('img');
            img.src = this.initialAvatarUrl;
            img.classList.add('avatar');
            this.previewContainer.appendChild(img);
        }
        else {
            const i = document.createElement('i');
            i.classList.add('avatar', 'fas', 'fa-user-circle');
            this.previewContainer.appendChild(i);
        }

        // 清空隐藏输入值
        if (this.resultInput) {
            this.resultInput.value = '';
        }
    }

}

// 导出到全局作用域
window.AvatarCropper = AvatarCropper;