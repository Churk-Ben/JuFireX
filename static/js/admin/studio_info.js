// 实时预览功能
document.addEventListener('DOMContentLoaded', function() {
    // 处理logo URL为"None"的情况
    const logoInput = document.getElementById('studioLogo');
    if (logoInput.value === 'None') {
        logoInput.value = '';
    }
});

// 实时预览功能
document.getElementById('studioName').addEventListener('input', function () {
    document.getElementById('previewName').textContent = this.value
})

document.getElementById('studioDescription').addEventListener('input', function () {
    document.getElementById('previewDescription').textContent = this.value
})

document.getElementById('studioEmail').addEventListener('input', function () {
    document.getElementById('previewEmail').textContent = this.value
})

document.getElementById('studioGithub').addEventListener('input', function () {
    const link = document.getElementById('previewGithub')
    link.href = this.value
    link.textContent = this.value
})

// Logo URL 预览功能
document.getElementById('studioLogo').addEventListener('input', function () {
    const container = document.querySelector('.preview-logo-container')
    const logoUrl = this.value.trim()

    if (logoUrl) {
        // 检查容器中是否已有图片元素
        let imgElement = container.querySelector('img')

        if (!imgElement) {
            // 如果没有图片元素，创建一个新的
            imgElement = document.createElement('img')
            imgElement.className = 'preview-logo'
            imgElement.alt = '工作室Logo'

            // 移除图标（如果存在）
            const iconElement = container.querySelector('.preview-icon')
            if (iconElement) {
                container.removeChild(iconElement)
            }

            container.appendChild(imgElement)
        }

        // 更新图片源
        imgElement.src = logoUrl

        // 添加错误处理
        imgElement.onerror = function () {
            this.src = ''
            showNotification('Logo 图片加载失败，请检查 URL', 'warning')
        }
    } else {
        // 如果 URL 为空，恢复默认图标
        container.innerHTML = '<i class="fas fa-building preview-icon"></i>'
    }
})

    // 表单验证
    ; (function () {
        'use strict'

        // 获取所有需要验证的表单
        const forms = document.querySelectorAll('.needs-validation')

        // 循环并阻止提交
        Array.from(forms).forEach((form) => {
            form.addEventListener(
                'submit',
                (event) => {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                        showNotification('请填写所有必填字段', 'warning')
                    }

                    form.classList.add('was-validated')
                },
                false
            )
        })
    })()

// 表单提交处理
document.getElementById('studioInfoForm').addEventListener('submit', function (e) {
    e.preventDefault()

    if (!this.checkValidity()) {
        return
    }

    const submitButton = this.querySelector('button[type="submit"]')
    const originalText = submitButton.innerHTML
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> 保存中...'
    submitButton.disabled = true

    const formData = {
        name: document.getElementById('studioName').value,
        description: document.getElementById('studioDescription').value,
        contact_email: document.getElementById('studioEmail').value,
        github_url: document.getElementById('studioGithub').value,
        logo_url: document.getElementById('studioLogo').value
    }

    API.put('/api/studio-info', formData)
        .then((data) => {
            if (data.success) {
                showNotification('工作室信息更新成功', 'success')
            } else {
                showNotification('更新失败: ' + data.message, 'error')
            }
        })
        .catch((error) => {
            console.error('Error:', error)
            showNotification('更新失败，请重试', 'error')
        })
        .finally(() => {
            submitButton.innerHTML = originalText
            submitButton.disabled = false
        })
})