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

        // 监听裁剪按钮
        if (this.cropButton) {
            this.cropButton.addEventListener('click', this.cropImage.bind(this));
        }

        // 监听取消按钮
        if (this.cancelButton) {
            this.cancelButton.addEventListener('click', this.cancelCrop.bind(this));
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (!file) return;

        // 检查文件类型
        if (!file.type.match('image.*')) {
            alert('请选择图片文件！');
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
                aspectRatio: 1, // 1:1 圆形头像
                viewMode: 1,
                dragMode: 'move',
                autoCropArea: 0.8, // 减小初始裁剪区域
                restore: false,
                guides: true,
                center: true,
                highlight: true, // 高亮显示裁剪区域
                cropBoxMovable: true,
                cropBoxResizable: true,
                toggleDragModeOnDblclick: false,
                background: true, // 显示背景网格
                modal: true, // 显示黑色模态背景
            });
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
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.borderRadius = '50%';
        img.style.objectFit = 'cover';
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
        if (this.cropper) {
            this.cropper.destroy();
            this.cropper = null;
        }

        // 隐藏裁剪容器
        this.cropperContainer.style.display = 'none';

        // 清空文件输入
        this.imageInput.value = '';
    }
}

// 导出到全局作用域
window.AvatarCropper = AvatarCropper;