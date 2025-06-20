document.addEventListener('DOMContentLoaded', function () {
    const api = new API();

    // 隐藏和恢复导航卡片
    document.querySelectorAll('.hide-card-btn').forEach(button => {
        button.addEventListener('click', function () {
            const cardId = this.dataset.cardId;
            const cardElement = this.closest('.navigation-card');

            api.hideNavigationCard(cardId).then(data => {
                if (data.success) {
                    cardElement.style.display = 'none';
                    showNotification('卡片已隐藏', 'success');
                } else {
                    showNotification(data.message || '操作失败', 'error');
                }
            });
        });
    });

    document.getElementById('restore-cards-btn')?.addEventListener('click', function () {
        api.restoreAllNavigationCards().then(data => {
            if (data.success) {
                showNotification('所有卡片已恢复', 'success');
                // 刷新页面以显示恢复的卡片
                location.reload();
            } else {
                showNotification(data.message || '操作失败', 'error');
            }
        });
    });

    // 切换卡片隐私状态
    document.querySelectorAll('.privacy-toggle').forEach(toggle => {
        toggle.addEventListener('change', function () {
            const cardId = this.dataset.cardId;
            const isPrivate = this.checked;

            api.toggleNavigationCardPrivacy(cardId, isPrivate).then(data => {
                if (data.success) {
                    showNotification('隐私状态已更新', 'success');
                } else {
                    showNotification(data.message || '操作失败', 'error');
                    // 如果更新失败，恢复切换按钮的状态
                    this.checked = !isPrivate;
                }
            });
        });
    });
});