// 颜色映射：level 0-4 → GitHub 官方色
const colors = ["#2a2b2bff", "#9be9a8", "#40c463", "#30a14e", "#216e39"];

// 使用GitHub GraphQL API获取真实贡献数据
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
        'Authorization': token ? `Bearer ${token}` : undefined
    };

    // 移除undefined的header
    if (!token) {
        delete headers.Authorization;
    }

    const response = await fetch('https://api.github.com/graphql', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
            query: query,
            variables: { userName: user }
        })
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`GitHub API错误: ${errorData.message || response.statusText}`);
    }

    const data = await response.json();

    if (data.errors) {
        throw new Error(`GraphQL错误: ${data.errors[0].message}`);
    }

    if (!data.data.user) {
        throw new Error('用户不存在');
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


// 映射GitHub的贡献级别到数字
function mapContributionLevel(level) {
    const levelMap = {
        'NONE': 0,
        'FIRST_QUARTILE': 1,
        'SECOND_QUARTILE': 2,
        'THIRD_QUARTILE': 3,
        'FOURTH_QUARTILE': 4
    };
    return levelMap[level] || 0;
}




// 生成空贡献数据（53周*7天=371天，GitHub实际显示一年）
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

async function fetchContributions(user, token) {
    if (!token) {
        console.error('必须提供GitHub Personal Access Token才能获取贡献数据。');
        return getEmptyContributions();
    }
    try {
        return await fetchRealContributions(user, token);
    } catch (err) {
        console.error('获取GitHub贡献数据失败:', err);
        return getEmptyContributions();
    }
}

// 缓存DOM元素
const userInput = document.getElementById('userInput');
const tokenInput = document.getElementById('tokenInput');
const showBtn = document.getElementById('showBtn');
const wall = document.getElementById('wall');

function render() {
    const user = userInput.value.trim() || "Churk-Ben";
    const token = tokenInput.value.trim() || "APIKEY";

    // 禁用按钮防止重复点击
    showBtn.disabled = true;
    showBtn.textContent = '加载中...';

    fetchContributions(user, token)
        .then((days) => {
            wall.innerHTML = ""; // 清空旧墙

            let totalContributions = 0;
            let maxStreak = 0;
            let currentStreak = 0;

            days.forEach((d) => {
                const cell = document.createElement("div");
                cell.className = "cell";
                cell.style.backgroundColor = colors[d.level];
                cell.title = `${d.date}: ${d.count} contribution${d.count !== 1 ? "s" : ""}`;
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
        })
        .catch((err) => {
            console.error('渲染失败:', err);
        })
        .finally(() => {
            showBtn.disabled = false;
            showBtn.textContent = '渲染贡献墙';
        });
}

// 添加回车键支持
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        render();
    }
});

tokenInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        render();
    }
});

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', function () {
    // 初始化时直接渲染空贡献墙
    const empty = getEmptyContributions();
    wall.innerHTML = '';
    empty.forEach((d) => {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.style.backgroundColor = colors[0];
        cell.title = `${d.date}: 0 contributions`;
        wall.appendChild(cell);
    });
});