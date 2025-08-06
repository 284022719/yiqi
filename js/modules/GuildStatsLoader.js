/**
 * 公会统计数据加载器
 */
import { getClassInfo, getClassColor, getClassIcon, getClassEmoji, getTextColor } from '../data/wow-classes.js';
import ClassIcon from '../components/ClassIcon.js';

export class GuildStatsLoader {
  constructor() {
    this.statsData = null;
  }
  
  async init() {
    try {
      console.log('GuildStatsLoader: 开始初始化...');
      await this.loadStats();
      console.log('GuildStatsLoader: 数据加载成功');
      this.renderStats();
      console.log('GuildStatsLoader: 统计数据渲染完成');
      this.renderCharts();
      console.log('GuildStatsLoader: 图表渲染完成');
      this.renderRankings();
      console.log('GuildStatsLoader: 排行榜渲染完成');
    } catch (error) {
      console.error('GuildStatsLoader: 加载统计数据失败:', error);
      this.showError('统计数据加载失败: ' + error.message);
    }
  }
  
  async loadStats() {
    console.log('GuildStatsLoader: 正在获取 data/page_data.json...');
    const response = await fetch('data/page_data.json');
    console.log('GuildStatsLoader: 响应状态:', response.status, response.ok);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    this.statsData = await response.json();
    console.log('GuildStatsLoader: JSON解析成功，数据:', this.statsData);
  }
  
  renderStats() {
    console.log('GuildStatsLoader: 开始渲染统计数据...');
    
    // 更新基础统计数据
    const totalMembersEl = document.getElementById('totalMembers');
    const activeMembersEl = document.getElementById('activeMembers');
    const dataCompletenessEl = document.getElementById('dataCompleteness');
    const lastUpdatedEl = document.getElementById('lastUpdated');
    
    console.log('GuildStatsLoader: 找到元素:', {
      totalMembersEl: !!totalMembersEl,
      activeMembersEl: !!activeMembersEl,
      dataCompletenessEl: !!dataCompletenessEl,
      lastUpdatedEl: !!lastUpdatedEl
    });
    
    if (totalMembersEl) {
      totalMembersEl.textContent = this.statsData.stats.totalMembers;
      console.log('GuildStatsLoader: 设置totalMembers为', this.statsData.stats.totalMembers);
    }
    
    if (activeMembersEl) {
      activeMembersEl.textContent = this.statsData.stats.activeMembers;
      console.log('GuildStatsLoader: 设置activeMembers为', this.statsData.stats.activeMembers);
    }
    
    if (dataCompletenessEl) {
      dataCompletenessEl.textContent = this.statsData.stats.dataCompleteness.percentage + '%';
      console.log('GuildStatsLoader: 设置dataCompleteness为', this.statsData.stats.dataCompleteness.percentage + '%');
    }
    
    if (lastUpdatedEl) {
      lastUpdatedEl.textContent = this.statsData.lastUpdated || '未知';
      console.log('GuildStatsLoader: 设置lastUpdated为', this.statsData.lastUpdated);
    }
    
    console.log('GuildStatsLoader: 统计数据渲染完成');
  }
  
  renderCharts() {
    this.renderClassChart();
    this.renderFactionChart();
    this.renderGenderChart();
    this.renderRaceChart();
    this.renderRealmChart();
  }
  
  renderClassChart() {
    console.log('GuildStatsLoader: 开始渲染职业分布图表...');
    const container = document.getElementById('classChart');
    console.log('GuildStatsLoader: classChart容器:', !!container);
    
    if (!container) {
      console.error('GuildStatsLoader: 未找到classChart容器');
      return;
    }
    
    const data = this.statsData.charts.classDistribution;
    
    // 检查数据是否为空
    if (!data || data.length === 0) {
      container.innerHTML = '<p style="color: #999; text-align: center;">暂无职业数据</p>';
      console.log('GuildStatsLoader: 职业数据为空，显示默认消息');
      return;
    }
    
    const maxValue = Math.max(...data.map(item => item.value));
    console.log('GuildStatsLoader: 职业数据:', data, '最大值:', maxValue);
    
    if (maxValue === 0) {
      container.innerHTML = '<p style="color: #999; text-align: center;">暂无职业数据</p>';
      return;
    }
    
    // 职业颜色映射
    const classColors = {
      '战士': '#C69B6D',
      '圣骑士': '#F48CBA',
      '猎人': '#AAD372',
      '潜行者': '#FFF468',
      '牧师': '#FFFFFF',
      '术士': '#8788EE',
      '法师': '#3FC7EB',
      '武僧': '#00FF98',
      '死亡骑士': '#C41E3A',
      '德鲁伊': '#FF7C0A',
      '萨满祭司': '#0070DD',
      '恶魔猎手': '#A330C9',
      '唤魔师': '#33937F'
    };
    
    const html = data
      .map(item => {
        const percentage = (item.value / maxValue * 100).toFixed(1);
        const classColor = classColors[item.name] || '#FF6B35';
        return `
          <div class="chart-bar">
            <span class="chart-bar-label" style="color: ${classColor}; min-width: 80px;">${item.name}</span>
            <div class="chart-bar-fill" style="width: ${percentage}%; background: linear-gradient(90deg, ${classColor} 0%, ${classColor}80 100%);"></div>
            <span class="chart-bar-value">${item.value}</span>
          </div>
        `;
      }).join('');
    
    container.innerHTML = html;
    console.log('GuildStatsLoader: 职业分布图表渲染完成，HTML长度:', html.length);
  }
  

  
  renderRaceChart() {
    const container = document.getElementById('raceChart');
    const data = this.statsData.charts.raceDistribution;
    
    // 检查数据是否为空
    if (!data || data.length === 0) {
      container.innerHTML = '<p style="color: #999; text-align: center;">暂无种族数据</p>';
      return;
    }
    
    const maxValue = Math.max(...data.map(item => item.value));
    
    if (maxValue === 0) {
      container.innerHTML = '<p style="color: #999; text-align: center;">暂无种族数据</p>';
      return;
    }
    
    // 为不同种族设置不同的颜色
    const raceColors = {
      '人类': '#C79C6E',
      '矮人': '#CD7F32',
      '暗夜精灵': '#C79C6E',
      '侏儒': '#FFC0CB',
      '德莱尼': '#0070DE',
      '狼人': '#8B7355',
      '熊猫人': '#FFD700',
      '虚空精灵': '#9370DB',
      '光铸德莱尼': '#FFD700',
      '黑铁矮人': '#8B4513',
      '库尔提拉斯人': '#4682B4',
      '机械侏儒': '#C0C0C0',
      '兽人': '#C41F3B',
      '牛头人': '#FFD700',
      '巨魔': '#00FF00',
      '亡灵': '#C0C0C0',
      '血精灵': '#FF69B4',
      '地精': '#32CD32',
      '夜之子': '#9370DB',
      '至高岭牛头人': '#8B4513',
      '赞达拉巨魔': '#FFD700',
      '玛格汉兽人': '#8B0000',
      '狐人': '#FFA500',
      '龙希尔': '#FF6B35',
      '土灵': '#8B4513'
    };
    
    const html = data
      .map(item => {
        const percentage = (item.value / maxValue * 100).toFixed(1);
        const raceColor = raceColors[item.name] || '#FF6B35';
        return `
          <div class="chart-bar">
            <span class="chart-bar-label" style="color: ${raceColor}; min-width: 80px;">${item.name}</span>
            <div class="chart-bar-fill" style="width: ${percentage}%; background: linear-gradient(90deg, ${raceColor} 0%, ${raceColor}80 100%);"></div>
            <span class="chart-bar-value">${item.value}</span>
          </div>
        `;
      }).join('');
    
    container.innerHTML = html;
  }
  
  renderFactionChart() {
    const container = document.getElementById('factionChart');
    const data = this.statsData.charts.factionDistribution;
    
    // 检查数据是否为空或全为0
    if (!data || data.length === 0) {
      container.innerHTML = '<p style="color: #999; text-align: center;">暂无阵营数据</p>';
      return;
    }
    
    const total = data.reduce((sum, item) => sum + item.value, 0);
    
    if (total === 0) {
      container.innerHTML = '<p style="color: #999; text-align: center;">暂无阵营数据</p>';
      return;
    }
    
    // 生成饼图
    let currentAngle = 0;
    const pieSlices = data.map(item => {
      const percentage = (item.value / total * 100).toFixed(1);
      const angle = (item.value / total) * 360;
      const factionName = item.name === 'Horde' ? '部落' : '联盟';
      const factionColor = item.name === 'Horde' ? '#C41F3B' : '#0070DE';
      
      const slice = `
        <div class="chart-pie-slice" style="
          background: conic-gradient(from ${currentAngle}deg, ${factionColor} 0deg, ${factionColor} ${angle}deg, transparent ${angle}deg);
        "></div>
      `;
      
      currentAngle += angle;
      return { slice, factionName, percentage, value: item.value, color: factionColor };
    });
    
    const pieChart = `
      <div class="chart-pie" style="background: conic-gradient(${pieSlices.map((item, index) => {
        const startAngle = pieSlices.slice(0, index).reduce((sum, slice) => sum + (slice.value / total * 360), 0);
        const endAngle = startAngle + (item.value / total * 360);
        return `${item.color} ${startAngle}deg ${endAngle}deg`;
      }).join(', ')});">
        <div class="chart-pie-center">${total}</div>
      </div>
      <div style="margin-top: 20px; text-align: center;">
        ${pieSlices.map(item => `
          <div style="margin: 5px 0; display: flex; align-items: center; justify-content: center;">
            <span style="display: inline-block; width: 12px; height: 12px; background: ${item.color}; border-radius: 2px; margin-right: 8px;"></span>
            <span style="color: ${item.color}; font-weight: bold;">${item.factionName}</span>
            <span style="margin-left: 8px; color: var(--color-text-secondary);">${item.value} (${item.percentage}%)</span>
          </div>
        `).join('')}
      </div>
    `;
    
    container.innerHTML = pieChart;
  }
  
  renderGenderChart() {
    const container = document.getElementById('genderChart');
    if (!container) {
      console.warn('GuildStatsLoader: 未找到genderChart容器');
      return;
    }
    
    const data = this.statsData.charts.genderDistribution;
    
    // 检查数据是否为空或全为0
    if (!data || data.length === 0) {
      container.innerHTML = '<p style="color: #999; text-align: center;">暂无性别数据</p>';
      return;
    }

    const total = data.reduce((sum, item) => sum + item.value, 0);

    if (total === 0) {
      container.innerHTML = '<p style="color: #999; text-align: center;">暂无性别数据</p>';
      return;
    }
    
    // 性别颜色配置
    const genderColors = {
      '男': '#0070DE',
      '女': '#FF69B4',
      '未知': '#999999'
    };
    
    // 生成饼图
    let currentAngle = 0;
    const pieSlices = data.map(item => {
      const percentage = (item.value / total * 100).toFixed(1);
      const angle = (item.value / total) * 360;
      const genderColor = genderColors[item.name] || '#999999';
      
      const slice = `
        <div class="chart-pie-slice" style="
          background: conic-gradient(from ${currentAngle}deg, ${genderColor} 0deg, ${genderColor} ${angle}deg, transparent ${angle}deg);
        "></div>
      `;
      
      currentAngle += angle;
      return { slice, genderName: item.name, percentage, value: item.value, color: genderColor };
    });
    
    const pieChart = `
      <div class="chart-pie" style="background: conic-gradient(${pieSlices.map((item, index) => {
        const startAngle = pieSlices.slice(0, index).reduce((sum, slice) => sum + (slice.value / total * 360), 0);
        const endAngle = startAngle + (item.value / total * 360);
        return `${item.color} ${startAngle}deg ${endAngle}deg`;
      }).join(', ')});">
        <div class="chart-pie-center">${total}</div>
      </div>
      <div style="margin-top: 20px; text-align: center;">
        ${pieSlices.map(item => `
          <div style="margin: 5px 0; display: flex; align-items: center; justify-content: center;">
            <span style="display: inline-block; width: 12px; height: 12px; background: ${item.color}; border-radius: 2px; margin-right: 8px;"></span>
            <span style="color: ${item.color}; font-weight: bold;">${item.genderName}</span>
            <span style="margin-left: 8px; color: var(--color-text-secondary);">${item.value} (${item.percentage}%)</span>
          </div>
        `).join('')}
      </div>
    `;
    
    container.innerHTML = pieChart;
  }
  
  renderRealmChart() {
    const container = document.getElementById('realmChart');
    const data = this.statsData.charts.realmDistribution;
    
    // 检查数据是否为空或全为0
    if (!data || data.length === 0) {
      container.innerHTML = '<p style="color: #999; text-align: center;">暂无服务器数据</p>';
      return;
    }
    
    // 只取前25个服务器
    const limitedData = data.slice(0, 25);
    
    const maxValue = Math.max(...limitedData.map(item => item.value));
    
    if (maxValue === 0) {
      container.innerHTML = '<p style="color: #999; text-align: center;">暂无服务器数据</p>';
      return;
    }
    
    // 为不同服务器设置不同的颜色
    const realmColors = {
      '阿尔萨斯': '#FFD700',
      '白银之手': '#C0C0C0',
      '死亡之翼': '#CD7F32',
      '罗宁': '#FF6B35',
      '燃烧之刃': '#9370DB',
      '冬泉谷': '#8B0000',
      '祖达克': '#00CED1',
      '凤凰之神': '#FF1493',
      '阿克蒙德': '#32CD32',
      '国王之谷': '#FF4500',
      '阿古斯': '#9C27B0',
      '影之哀伤': '#8B0000',
      '克尔苏加德': '#FF6B35',
      '斯克提斯': '#9370DB',
      '金色平原': '#FFD700',
      '无尽之海': '#00CED1',
      '红龙军团': '#FF1493',
      '巴瑟拉斯': '#32CD32',
      '塞拉摩': '#FF4500',
      '安苏': '#9C27B0'
    };
    
    const html = limitedData
      .map(item => {
        const percentage = (item.value / maxValue * 100).toFixed(1);
        const realmColor = realmColors[item.name] || '#9C27B0';
        return `
          <div class="chart-bar">
            <span class="chart-bar-label" style="color: ${realmColor};">${item.name}</span>
            <div class="chart-bar-fill" style="width: ${percentage}%; background: linear-gradient(90deg, ${realmColor} 0%, ${realmColor}80 100%);"></div>
            <span class="chart-bar-value">${item.value}</span>
          </div>
        `;
      }).join('');
    
    container.innerHTML = html;
  }
  

  
  renderRankings() {
    console.log('GuildStatsLoader: 开始渲染排行榜...');
    console.log('GuildStatsLoader: 排行榜数据:', this.statsData.rankings);
    
    this.renderAchievementRanking();
    this.renderMythicScoreRanking();
    
    console.log('GuildStatsLoader: 排行榜渲染完成');
  }
  
  renderAchievementRanking() {
    const container = document.getElementById('achievementRanking');
    if (!container) {
      console.warn('GuildStatsLoader: 未找到achievementRanking容器');
      return;
    }
    
    const data = this.statsData.rankings.achievementRanking;
    console.log('GuildStatsLoader: 成就排行榜数据:', data);
    if (!data || data.length === 0) {
      container.querySelector('tbody').innerHTML = `
        <tr>
          <td colspan="4" style="text-align: center; color: #999; padding: 40px 20px;">
            <div style="font-size: 48px; margin-bottom: 10px;">🏆</div>
            <div style="font-size: 16px; margin-bottom: 5px;">暂无成就点数数据</div>
            <div style="font-size: 12px; color: #666;">请稍后再试</div>
          </td>
        </tr>
      `;
      return;
    }
    
    const tbody = container.querySelector('tbody');
    tbody.innerHTML = data.map(item => {
      const classInfo = getClassInfo(item.class);
      const classColor = classInfo ? classInfo.color : 'var(--color-text)';
      const textColor = classInfo ? classInfo.textColor : 'var(--color-text)';
      return `
        <tr>
          <td class="rank ${item.rank <= 3 ? 'top-3' : ''}">${item.rank}</td>
          <td class="character-name">${item.name}</td>
          <td class="class" style="color: ${classColor};">
            <img src="${getClassIcon(item.class)}" alt="${item.class}" style="width: 20px; height: 20px; border-radius: 50%; margin-right: 8px; vertical-align: middle;">
            ${item.class}
          </td>
          <td class="achievement-points">${item.achievement_points.toLocaleString()}</td>
        </tr>
      `;
    }).join('');
  }
  

  
  renderMythicScoreRanking() {
    const container = document.getElementById('mythicScoreRanking');
    if (!container) {
      console.warn('GuildStatsLoader: 未找到mythicScoreRanking容器');
      return;
    }
    
    const data = this.statsData.rankings.mythicScoreRanking;
    console.log('GuildStatsLoader: 史诗钥石评分排行榜数据:', data);
    
    if (!data || data.length === 0) {
      container.querySelector('tbody').innerHTML = `
        <tr>
          <td colspan="5" style="text-align: center; color: #999; padding: 40px 20px;">
            <div style="font-size: 48px; margin-bottom: 10px;">🗝️</div>
            <div style="font-size: 16px; margin-bottom: 5px;">暂无史诗钥石评分数据</div>
            <div style="font-size: 12px; color: #666;">当前数据中所有角色的史诗钥石评分均为0</div>
          </td>
        </tr>
      `;
      return;
    }
    
    const tbody = container.querySelector('tbody');
    tbody.innerHTML = data.map(item => {
      const classInfo = getClassInfo(item.class);
      const classColor = classInfo ? classInfo.color : 'var(--color-text)';
      const textColor = classInfo ? classInfo.textColor : 'var(--color-text)';
      return `
        <tr>
          <td class="rank ${item.rank <= 3 ? 'top-3' : ''}">${item.rank}</td>
          <td class="character-name">${item.name}</td>
          <td class="class" style="color: ${classColor};">
            <img src="${getClassIcon(item.class)}" alt="${item.class}" style="width: 20px; height: 20px; border-radius: 50%; margin-right: 8px; vertical-align: middle;">
            ${item.class}
          </td>
          <td class="mythic-score">${item.mythic_score.toLocaleString()}</td>
          <td class="item-level">${item.average_item_level ? item.average_item_level.toFixed(1) : 'N/A'}</td>
        </tr>
      `;
    }).join('');
  }
  

  
  showError(message) {
    const containers = ['classChart', 'factionChart', 'raceChart', 'realmChart'];
    containers.forEach(id => {
      const container = document.getElementById(id);
      if (container) {
        container.innerHTML = `<p style="color: var(--color-danger);">${message}</p>`;
      }
    });
  }
} 