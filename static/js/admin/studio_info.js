document.addEventListener('DOMContentLoaded', function () {
    initializeStudioInfoPage();
});

function initializeStudioInfoPage() {
    handleLogoUrlNone();
    setupEventListeners();
    setupFormValidation();
    setupFormSubmission();
}

function handleLogoUrlNone() {
    const logoInput = document.getElementById('studioLogo');
    if (logoInput && logoInput.value === 'None') {
        logoInput.value = '';
    }
}

function setupEventListeners() {
    const previewMap = {
        'studioName': updateTextContent('previewName'),
        'studioDescription': updateTextContent('previewDescription'),
        'studioEmail': updateTextContent('previewEmail'),
        'studioGithub': updateGithubLink('previewGithub'),
        'studioLogo': updateLogoPreview
    };

    for (const [elementId, handler] of Object.entries(previewMap)) {
        const element = document.getElementById(elementId);
        if (element) {
            element.addEventListener('input', handler);
        }
    }
}

function updateTextContent(previewId) {
    return function() {
        const previewElement = document.getElementById(previewId);
        if (previewElement) {
            previewElement.textContent = this.value;
        }
    };
}

function updateGithubLink(previewId) {
    return function() {
        const link = document.getElementById(previewId);
        if (link) {
            link.href = this.value;
            link.textContent = this.value;
        }
    };
}

function updateLogoPreview() {
    const container = document.querySelector('.preview-logo-container');
    if (!container) return;

    const logoUrl = this.value.trim();

    if (logoUrl) {
        let imgElement = container.querySelector('img');
        if (!imgElement) {
            imgElement = document.createElement('img');
            imgElement.className = 'preview-logo';
            imgElement.alt = '工作室Logo';
            const iconElement = container.querySelector('.preview-icon');
            if (iconElement) {
                container.removeChild(iconElement);
            }
            container.appendChild(imgElement);
        }
        imgElement.src = logoUrl;
        imgElement.onerror = () => {
            imgElement.src = '';
            showNotification('Logo 图片加载失败，请检查 URL', 'warning');
        };
    } else {
        container.innerHTML = '<i class="fas fa-building preview-icon"></i>';
    }
}

function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                showNotification('请填写所有必填字段', 'warning');
            }
            form.classList.add('was-validated');
        }, false);
    });
}

function setupFormSubmission() {
    const form = document.getElementById('studioInfoForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

function handleFormSubmit(e) {
    e.preventDefault();
    if (!this.checkValidity()) return;

    const submitButton = this.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    setButtonLoading(submitButton, true, '保存中...');

    const formData = {
        name: document.getElementById('studioName').value,
        description: document.getElementById('studioDescription').value,
        contact_email: document.getElementById('studioEmail').value,
        github_url: document.getElementById('studioGithub').value,
        logo_url: document.getElementById('studioLogo').value
    };

    API.put('/api/studio-info', formData)
        .then(handleApiResponse('工作室信息更新成功', '更新失败'))
        .catch(handleApiError('更新失败'))
        .finally(() => setButtonLoading(submitButton, false, originalText));
}

function setButtonLoading(button, isLoading, loadingText) {
    button.disabled = isLoading;
    button.innerHTML = isLoading ? `<i class="fas fa-spinner fa-spin me-2"></i> ${loadingText}` : loadingText;
}

function handleApiResponse(successMessage, errorMessage) {
    return function(data) {
        if (data.success) {
            showNotification(successMessage, 'success');
        } else {
            showNotification(`${errorMessage}: ${data.message}`, 'error');
        }
    };
}

function handleApiError(message) {
    return function(error) {
        console.error('Error:', error);
        showNotification(`${message}，请重试`, 'error');
    };
}