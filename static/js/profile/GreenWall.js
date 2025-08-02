// JuFire Studio - GitHub贡献墙组件

// 颜色映射：level 0-4
const CONTRIBUTION_COLORS = [
    "rgba(40, 42, 43, 0.8)",   // level 0: 底色
    "rgba(56, 102, 65, 0.7)",  // level 1: 深绿
    "rgba(33, 110, 57, 0.9)",  // level 2: 暗绿
    "rgba(48, 161, 78, 0.8)",  // level 3: 中绿
    "rgba(64, 196, 99, 0.7)"   // level 4: 亮绿
];

// GitHub贡献级别映射
const CONTRIBUTION_LEVEL_MAP = {
    'NONE': 0,
    'FIRST_QUARTILE': 1,
    'SECOND_QUARTILE': 2,
    'THIRD_QUARTILE': 3,
    'FOURTH_QUARTILE': 4
};

// 缓存DOM元素
let userInput, tokenInput, showBtn, wall;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function () {
    initializeGreenWall();
});

/**
 * 初始化GitHub贡献墙组件
 */
function initializeGreenWall() {
    // 缓存DOM元素
    userInput = document.getElementById('userInput');
    tokenInput = document.getElementById('tokenInput');
    showBtn = document.getElementById('showBtn');
    wall = document.getElementById('wall');

    if (!userInput || !tokenInput || !showBtn || !wall) {
        showNotification('页面元素加载失败，请刷新页面重试', 'error');
        return;
    }

    setupEventListeners();
    renderEmptyWall();
}

/**
 * 设置事件监听器
 */
function setupEventListeners() {
    // 渲染按钮点击事件
    showBtn.addEventListener('click', handleRender);

    // 回车键支持
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            handleRender();
        }
    });

    tokenInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            handleRender();
        }
    });
}

/**
 * 使用GitHub GraphQL API获取真实贡献数据
 * @param {string} user - GitHub用户名
 * @param {string} token - GitHub Personal Access Token
 * @returns {Promise<Array>} 贡献数据数组
 */
async function fetchRealContributions(user, token) {
    const query = `
        query($userName: String!) {
          user(login: $userName) {
            contributionsCollection {
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    contributionCount
                    date
                    contributionLevel
                  }
                }
              }
            }
          }
        }
      `;

    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };

    let data;
    try {
        // 直接使用fetch调用GitHub API，避免CORS问题
        const response = await fetch('https://api.github.com/graphql', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                query: query,
                variables: { userName: user }
            })
        });

        if (!response.ok) {
            let errorData;
            try {
                errorData = await response.json();
            } catch {
                errorData = {};
            }
            const errorMessage = errorData.message || response.statusText || response.status || '未知错误';
            showNotification(`GitHub API错误: ${errorMessage}`, 'error');
            return null;
        }

        data = await response.json();
    } catch (error) {
        console.error('GitHub API请求失败:', error);
        showNotification('网络错误，请检查网络连接', 'error');
        return null;
    }

    if (data.errors) {
        showNotification(`GraphQL错误: ${data.errors[0].message}`, 'error');
        return null;
    }

    if (!data.data.user) {
        showNotification('GitHub用户不存在，请检查用户名', 'warning');
        return null;
    }

    const weeks = data.data.user.contributionsCollection.contributionCalendar.weeks;
    const contributions = [];

    // 重新组织数据以匹配GitHub的列优先排列
    const contributionsByDate = {};
    weeks.forEach(week => {
        week.contributionDays.forEach(day => {
            contributionsByDate[day.date] = {
                date: day.date,
                count: day.contributionCount,
                level: mapContributionLevel(day.contributionLevel)
            };
        });
    });

    // 按周和星期重新排列（列优先）
    weeks.forEach(week => {
        week.contributionDays.forEach(day => {
            contributions.push(contributionsByDate[day.date]);
        });
    });

    return contributions;
}


/**
 * 映射GitHub的贡献级别到数字
 * @param {string} level - GitHub贡献级别
 * @returns {number} 对应的数字级别
 */
function mapContributionLevel(level) {
    return CONTRIBUTION_LEVEL_MAP[level] || 0;
}

/**
 * 生成空贡献数据（53周*7天=371天，GitHub实际显示一年）
 * @returns {Array} 空贡献数据数组
 */
function getEmptyContributions() {
    const days = 53 * 7;
    const today = new Date();
    const result = [];

    for (let i = days - 1; i >= 0; i--) {
        const d = new Date(today);
        d.setDate(today.getDate() - i);
        result.push({
            date: d.toISOString().slice(0, 10),
            count: 0,
            level: 0
        });
    }

    return result;
}

/**
 * 获取GitHub贡献数据
 * @param {string} user - GitHub用户名
 * @param {string} token - GitHub Personal Access Token
 * @returns {Promise<Array>} 贡献数据数组
 */
async function fetchContributions(user, token) {
    if (!token) {
        showNotification('必须提供GitHub Personal Access Token才能获取贡献数据', 'warning');
        return getEmptyContributions();
    }

    try {
        const contributions = await fetchRealContributions(user, token);
        if (contributions) {
            showNotification('贡献数据加载成功', 'success');
            return contributions;
        }
        return getEmptyContributions();
    } catch (error) {
        console.error('获取GitHub贡献数据失败:', error);
        showNotification('获取GitHub贡献数据失败，显示空白贡献墙', 'error');
        return getEmptyContributions();
    }
}

/**
 * 处理渲染按钮点击事件
 */
function handleRender() {
    const user = userInput.value.trim() || "Churk-Ben";
    const token = tokenInput.value.trim();

    if (!user) {
        showNotification('请输入GitHub用户名', 'warning');
        return;
    }

    setButtonLoading(true);

    fetchContributions(user, token)
        .then((days) => {
            renderContributionWall(days);
        })
        .catch((error) => {
            console.error('渲染失败:', error);
            showNotification('渲染贡献墙失败，请重试', 'error');
        })
        .finally(() => {
            setButtonLoading(false);
        });
}

/**
 * 渲染贡献墙
 * @param {Array} days - 贡献数据数组
 */
function renderContributionWall(days) {
    if (!days || !Array.isArray(days)) {
        showNotification('贡献数据格式错误', 'error');
        return;
    }

    wall.innerHTML = ''; // 清空旧墙

    let totalContributions = 0;
    let maxStreak = 0;
    let currentStreak = 0;

    days.forEach((d) => {
        const cell = createContributionCell(d);
        wall.appendChild(cell);

        totalContributions += d.count;

        // 计算连续贡献天数
        if (d.count > 0) {
            currentStreak++;
            maxStreak = Math.max(maxStreak, currentStreak);
        } else {
            currentStreak = 0;
        }
    });

    // 可以在这里添加统计信息显示
    console.log(`总贡献: ${totalContributions}, 最长连续: ${maxStreak}天`);
}

/**
 * 创建贡献单元格
 * @param {Object} contribution - 贡献数据对象
 * @returns {HTMLElement} 贡献单元格DOM元素
 */
function createContributionCell(contribution) {
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.style.backgroundColor = CONTRIBUTION_COLORS[contribution.level];
    cell.title = `${contribution.date}: ${contribution.count} contribution${contribution.count !== 1 ? 's' : ''}`;
    return cell;
}

/**
 * 设置按钮加载状态
 * @param {boolean} isLoading - 是否为加载状态
 */
function setButtonLoading(isLoading) {
    showBtn.disabled = isLoading;
    showBtn.textContent = isLoading ? '加载中...' : '渲染贡献墙';
}

/**
 * 渲染空白贡献墙
 */
function renderEmptyWall() {
    const emptyContributions = getEmptyContributions();
    wall.innerHTML = '';

    emptyContributions.forEach((d) => {
        const cell = createContributionCell(d);
        wall.appendChild(cell);
    });
}

// 将需要全局访问的函数暴露到window对象
Object.assign(window, {
    handleRender,
    renderContributionWall
});