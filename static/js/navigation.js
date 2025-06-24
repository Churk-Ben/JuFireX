document.addEventListener('DOMContentLoaded', function () {
    // 隐藏和恢复导航卡片
    document.querySelectorAll('.hide-card-btn').forEach(button => {
        button.addEventListener('click', function () {
            const cardId = this.dataset.cardId;
            const cardElement = this.closest('.navigation-card');

            fetch('/api/navigation/hide/' + cardId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content,
                },
                body: JSON.stringify({ nav_item_id: cardId })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        cardElement.style.display = 'none';
                        showNotification('卡片已隐藏', 'success');
                    } else {
                        showNotification(data.message || '操作失败', 'error');
                    }
                })
                .catch(error => {
                    showNotification('请求失败', 'error');
                    console.error('Error:', error);
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

            api.toggleNavigationCardPrivacy(cardId, isPrivate, {
                headers: {
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
                }
            }).then(data => {
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


// 隐藏卡片函数
function hideCard(navItemId) {
    fetch('/api/navigation/hide/' + navItemId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({ nav_item_id: navItemId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 隐藏卡片
                document.querySelector(`.nav-card-col[data-nav-item-id="${navItemId}"]`).style.display = 'none';
                showNotification('卡片已隐藏', 'success');
                // 添加到隐藏卡片列表
                const hiddenCard = document.querySelector(`.nav-card-col[data-nav-item-id="${navItemId}"]`).cloneNode(true);
                hiddenCard.style.display = 'block';
                document.getElementById('hidden-cards-list').appendChild(hiddenCard);
            } else {
                showNotification(data.message || '隐藏失败', 'error');
            }
        })
        .catch(error => {
            showNotification('请求失败', 'error');
            console.error('Error:', error);
        });
}

// 切换隐私状态函数
function togglePrivacy(navItemId, isPublic, element) {
    fetch('/api/navigation/toggle_privacy/' + navItemId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({
            nav_item_id: navItemId,
            is_public: !isPublic
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 更新按钮文本和状态
                if (isPublic) {
                    element.textContent = '设为公开';
                    element.dataset.isPublic = '0';
                } else {
                    element.textContent = '设为私有';
                    element.dataset.isPublic = '1';
                }
            } else {
                alert(data.message || '操作失败');
            }
        })
        .catch(error => console.error('Error:', error));
}