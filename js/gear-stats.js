// 装备统计功能
class GearStats {
  constructor() {
    this.gearStats = document.getElementById('gear-stats');
    this.classFilter = document.getElementById('class-filter');
    this.roleFilter = document.getElementById('role-filter');
    this.init();
  }
  
  async init() {
    try {
      await this.loadGearStats();
      
      // 添加过滤器事件监听
      this.classFilter.addEventListener('change', () => this.loadGearStats());
      this.roleFilter.addEventListener('change', () => this.loadGearStats());
    } catch (error) {
      this.showError(error);
    }
  }
  
  async loadGearStats() {
    try {
      this.gearStats.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 正在加载装备数据...';
      
      const classFilter = this.classFilter.value;
      const roleFilter = this.roleFilter.value;
      
      const response = await fetch(`/.netlify/functions/gear-stats?class=${classFilter}&role=${roleFilter}`);
      if (!response.ok) throw new Error('网络响应不正常');
      
      const data = await response.json();
      if (!data.players) throw new Error('数据格式不正确');
      
      this.renderGearStats(data);
    } catch (error) {
      this.showError(error);
    }
  }
  
  renderGearStats(data) {
    let html = `
      <div class="gear-summary">
        <div>
          <i class="fas fa-users"></i> 人数: <strong>${data.players.length}</strong>
        </div>
        <div>
          <i class="fas fa-shield-alt"></i> 平均装等: <strong>${data.avgItemLevel.toFixed(1)}</strong>
        </div>
        <div>
          <i class="fas fa-crown"></i> 最高装等: <strong>${data.maxItemLevel}</strong>
          <small>(${data.maxItemLevelPlayer})</small>
        </div>
        <div>
          <i class="fas fa-vest"></i> 平均套装: <strong>${data.avgTierSet.toFixed(1)}/4</strong>
        </div>
      </div>
      <table class="dkp-table">
        <thead>
          <tr>
            <th>玩家</th>
            <th>装等</th>
            <th>武器</th>
            <th>饰品</th>
            <th>套装</th>
            <th>更新时间</th>
          </tr>
        </thead>
        <tbody>
    `;
    
    data.players.forEach(player => {
      html += `
        <tr>
          <td>
            <img src="img/classes/${player.class}.png" width="20" alt="${player.class}" 
                 onerror="this.src='img/classes/default.png'">
            ${player.name}
          </td>
          <td>${player.itemLevel}</td>
          <td>${player.weapon || '-'}</td>
          <td>${player.trinkets.join(', ') || '-'}</td>
          <td>
            ${player.tierSet}/4
            ${player.tierSet === 4 ? '<i class="fas fa-check" style="color: var(--color-success);"></i>' : ''}
          </td>
          <td>${new Date(player.lastUpdated).toLocaleDateString()}</td>
        </tr>
      `;
    });
    
    html += `
        </tbody>
      </table>
    `;
    
    this.gearStats.innerHTML = html;
  }
  
  showError(error) {
    this.gearStats.innerHTML = `
      <div class="error">
        <i class="fas fa-exclamation-triangle"></i> 
        无法加载装备数据: ${error.message}
      </div>
    `;
  }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  new GearStats();
});
