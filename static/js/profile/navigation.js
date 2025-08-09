/**
 * 个人主页导航功能
 * 实现点击导航按钮时切换显示对应内容
 */

document.addEventListener('DOMContentLoaded', function () {
  // 获取所有导航项
  const navItems = document.querySelectorAll('.profile-nav-item');

  // 获取所有内容区域
  const projectsContent = document.getElementById('profile-projects-content');
  const contributionsContent = document.getElementById('profile-contributions-content');
  const achievementsContent = document.getElementById('profile-achievements-content');

  // 内容区域数组，方便批量操作
  const contentAreas = [projectsContent, contributionsContent, achievementsContent];

  // 初始化页面，根据当前active的导航项显示对应内容
  function initializeContent() {
    const activeNavItem = document.querySelector('.profile-nav-item.active');
    if (activeNavItem) {
      const activeLink = activeNavItem.querySelector('.profile-nav-link');
      const activeHash = activeLink.getAttribute('href');

      showContentByHash(activeHash);
    } else {
      hideAllContent();
      if (projectsContent) projectsContent.style.display = 'block';
    }
  }

  // 隐藏所有内容区域
  function hideAllContent() {
    contentAreas.forEach(content => {
      if (content) {
        content.classList.remove('active');
      }
    });
  }

  // 根据hash显示对应内容
  function showContentByHash(hash) {
    hideAllContent();

    let contentToShow = null;

    switch (hash) {
      case '#Projects':
        contentToShow = projectsContent;
        break;
      case '#Contributions':
        contentToShow = contributionsContent;
        break;
      case '#Achievements':
        contentToShow = achievementsContent;
        break;
      default:
        contentToShow = projectsContent;
        break;
    }

    // 添加激活类触发动画
    if (contentToShow) {
      contentToShow.classList.add('active');
    }
  }

  // 为所有导航项添加点击事件
  navItems.forEach(item => {
    // 只处理前三个导航项（项目、贡献墙、里程碑）
    const link = item.querySelector('.profile-nav-link');
    const hash = link.getAttribute('href');

    // 只为前三个导航项添加点击事件（排除设置按钮）
    if (hash === '#Projects' || hash === '#Contributions' || hash === '#Achievements') {
      item.addEventListener('click', function (e) {
        // 阻止默认行为，防止页面跳转
        e.preventDefault();

        // 移除所有导航项的active类
        navItems.forEach(navItem => {
          navItem.classList.remove('active');
        });

        // 为当前点击的导航项添加active类
        this.classList.add('active');

        // 显示对应内容
        showContentByHash(hash);
      });
    }
  });

  // 检查URL中是否有hash，如果有则显示对应内容
  function checkUrlHash() {
    const hash = window.location.hash;
    if (hash) {
      // 找到对应的导航项并激活
      navItems.forEach(item => {
        const link = item.querySelector('.profile-nav-link');
        if (link && link.getAttribute('href') === hash) {
          // 移除所有导航项的active类
          navItems.forEach(navItem => {
            navItem.classList.remove('active');
          });

          // 为当前导航项添加active类
          item.classList.add('active');

          // 显示对应内容
          showContentByHash(hash);
        }
      });
    } else {
      // 没有hash，初始化内容
      initializeContent();
    }
  }

  // 页面加载时检查URL hash
  checkUrlHash();

  // 监听hash变化事件
  window.addEventListener('hashchange', checkUrlHash);

  // 初始化页面内容
  initializeContent();
});