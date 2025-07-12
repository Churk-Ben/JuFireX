document.addEventListener('DOMContentLoaded', function () {
    // 隐藏和恢复导航卡片
    document.querySelectorAll('.hide-card-btn').forEach(button => {
        button.addEventListener('click', function () {
            const cardId = this.dataset.cardId;
            const cardElement = this.closest('.navigation-card');

            API.post('/api/navigation/hide/' + cardId, { nav_item_id: cardId }, {
                headers: {
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
                }
            })
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
        API.post('/api/navigation/restore-all', {}, {
            headers: {
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            }
        }).then(data => {
            if (data.success) {
                showNotification('所有卡片已恢复', 'success');
                location.reload();
            } else {
                showNotification(data.message || '操作失败', 'error');
            }
        }).catch(error => {
            showNotification('请求失败', 'error');
            console.error('Error:', error);
        });
    });

    // 切换卡片隐私状态
    document.querySelectorAll('.privacy-toggle').forEach(toggle => {
        toggle.addEventListener('change', function () {
            const cardId = this.dataset.cardId;
            const isPrivate = this.checked;

            API.post('/api/navigation/toggle_privacy/' + cardId, { is_public: isPrivate }, {
                headers: {
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
                }
            }).then(data => {
                if (data.success) {
                    showNotification('隐私状态已更新', 'success');
                } else {
                    showNotification(data.message || '操作失败', 'error');
                    this.checked = !isPrivate;
                }
            }).catch(error => {
                showNotification('请求失败', 'error');
                console.error('Error:', error);
                this.checked = !isPrivate;
            });
        });
    });
});


// 隐藏卡片函数
function hideCard(navItemId) {
    API.post('/api/navigation/hide/' + navItemId, { nav_item_id: navItemId }, {
        headers: {
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        }
    })
        .then(data => {
            if (data.success) {
                document.querySelector(`.nav-card-col[data-nav-item-id="${navItemId}"]`).style.display = 'none';
                showNotification('卡片已隐藏', 'success');
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
    API.post('/api/navigation/toggle_privacy/' + navItemId, {
        nav_item_id: navItemId,
        is_public: !isPublic
    }, {
        headers: {
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        }
    })
        .then(data => {
            if (data.success) {
                if (isPublic) {
                    element.textContent = '设为公开';
                    element.dataset.isPublic = '0';
                } else {
                    element.textContent = '设为私有';
                    element.dataset.isPublic = '1';
                }
                showNotification('隐私状态已更新', 'success');
            } else {
                showNotification(data.message || '操作失败', 'error');
            }
        })
        .catch(error => {
            showNotification('请求失败', 'error');
            console.error('Error:', error);
        });
}