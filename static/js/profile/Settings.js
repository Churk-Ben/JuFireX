// JuFire Studio - 设置页面脚本

class Settings {
  constructor(userId) {
    this.userId = userId;
    this.form = document.getElementById('settings-form');
    this.saveBtn = document.getElementById('save-settings-btn');
    this.resetBtn = document.getElementById('reset-settings-btn');

    // Dangerous Zone
    this.updatePasswordBtn = document.getElementById('update-password-btn');
    this.updateTokenBtn = document.getElementById('update-token-btn');
    this.deleteAccountBtn = document.getElementById('delete-account-btn');

    this.init();
  }

  init() {
    this.saveBtn.addEventListener('click', () => this.saveSettings());
    this.resetBtn.addEventListener('click', () => this.resetSettings());

    // Dangerous Zone
    this.updatePasswordBtn.addEventListener('click', () => this.updatePassword());
    this.updateTokenBtn.addEventListener('click', () => this.updateToken());
    this.deleteAccountBtn.addEventListener('click', () => this.deleteAccount());
  }

  getSettingsData() {
    const formData = new FormData(this.form);
    const settings = {
      preferences: {
        theme: formData.get('theme'),
        notifications: formData.get('notifications') === 'on',
      },
      privacy: {
        show_email: formData.get('show_email') === 'on',
        show_join_date: formData.get('show_join_date') === 'on',
        show_green_wall: formData.get('show_green_wall') === 'on',
        show_nav_counts: formData.get('show_nav_counts') === 'on',
        show_projects: formData.get('show_projects') === 'on',
      },
      linked_accounts: {
        github: {
          username: formData.get('github_username'),
        },
      },
    };
    return settings;
  }

  async saveSettings() {
    const settings = this.getSettingsData();
    try {
      const response = await API.post(`/profile/${this.userId}/settings`, settings);
      showNotification('设置已保存', 'success');
    } catch (error) {
      showNotification('保存设置失败', 'error');
    }
  }

  async resetSettings() {
    // TODO: Implement reset functionality
    showNotification('功能待实现', 'info');
  }

  async updatePassword() {
    const form = document.getElementById('update-password-form');
    const formData = new FormData(form);
    const current_password = formData.get('current_password');
    const new_password = formData.get('new_password');
    const confirm_password = formData.get('confirm_password');

    if (new_password !== confirm_password) {
      showNotification('新密码和确认密码不匹配', 'error');
      return;
    }

    try {
      const response = await API.post(`/profile/${this.userId}/update_password`, {
        current_password,
        new_password,
      });
      showNotification(response.message, 'success');
      bootstrap.Modal.getInstance(document.getElementById('updatePasswordModal')).hide();
    } catch (error) {
      const errorData = await error.json();
      showNotification(errorData.message, 'error');
    }
  }

  async updateToken() {
    const form = document.getElementById('update-token-form');
    const formData = new FormData(form);
    const github_token = formData.get('github_token');

    try {
      const response = await API.post(`/profile/${this.userId}/update_token`, {
        github_token,
      });
      showNotification(response.message, 'success');
      bootstrap.Modal.getInstance(document.getElementById('updateTokenModal')).hide();
    } catch (error) {
      const errorData = await error.json();
      showNotification(errorData.message, 'error');
    }
  }

  async deleteAccount() {
    const form = document.getElementById('delete-account-form');
    const formData = new FormData(form);
    const password = formData.get('confirm_password');
    const confirm_delete = formData.get('confirm_delete') === 'on';

    if (!confirm_delete) {
      showNotification('请确认您要删除账户', 'error');
      return;
    }

    try {
      const response = await API.post(`/profile/${this.userId}/delete_account`, {
        password,
      });
      showNotification(response.message, 'success');
      // Redirect to homepage after account deletion
      window.location.href = '/';
    } catch (error) {
      const errorData = await error.json();
      showNotification(errorData.message, 'error');
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const settingsForm = document.getElementById('settings-form');
  if (settingsForm) {
    const userId = window.location.pathname.split('/')[2];
    new Settings(userId);
  }
});