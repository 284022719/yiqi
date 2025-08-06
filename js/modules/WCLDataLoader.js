/**
 * WCL数据处理器
 */
export class WCLDataLoader {
  constructor() {
    this.loadingEl = document.getElementById('loading');
    this.errorEl = document.getElementById('error');
    this.tableEl = document.getElementById('wcl-table');
    this.refreshBtn = document.getElementById('refresh-btn');
    
    if (this.tableEl) {
      this.init();
    }
  }
  
  async init() {
    try {
      this.showLoading();
      const reports = await this.fetchReports();
      this.renderReports(reports);
    } catch (error) {
      this.showError(error.message);
    } finally {
      this.hideLoading();
    }
    
    // 绑定刷新按钮事件
    if (this.refreshBtn) {
      this.refreshBtn.addEventListener('click', () => this.refresh());
    }
  }
  
  async refresh() {
    if (this.refreshBtn) {
      this.refreshBtn.classList.add('loading');
      this.refreshBtn.disabled = true;
    }
    
    try {
      this.showLoading();
      const reports = await this.fetchReports();
      this.renderReports(reports);
      this.hideError();
    } catch (error) {
      this.showError(error.message);
    } finally {
      this.hideLoading();
      if (this.refreshBtn) {
        this.refreshBtn.classList.remove('loading');
        this.refreshBtn.disabled = false;
      }
    }
  }
  
  async fetchReports() {
    const response = await fetch('/.netlify/functions/wcl-proxy');
    const data = await response.json();
    
    if (!response.ok || !data.success) {
      throw new Error(data.error || '服务器返回错误');
    }
    
    if (!data.data?.reports) {
      throw new Error('API返回数据格式不正确');
    }
    
    return data.data.reports;
  }
  
  renderReports(reports) {
    if (!reports || reports.length === 0) {
      this.showEmptyState();
      return;
    }
    
    const tbody = this.tableEl.querySelector('tbody');
    tbody.innerHTML = '';
    
    reports.forEach((report, index) => {
      const row = document.createElement('tr');
      const date = new Date(report.startTime);
      const killCount = report.fights.filter(f => f.kill).length;
      const totalEncounters = new Set(report.fights.map(f => f.encounterID)).size;
      
      // 添加延迟动画效果
      row.style.opacity = '0';
      row.style.transform = 'translateX(-20px)';
      
      row.innerHTML = `
        <td>${date.toLocaleDateString('zh-CN')}</td>
        <td>${report.zone?.name || '未知区域'}</td>
        <td>${killCount}/${totalEncounters}</td>
        <td>${report.owner?.name || '未知'}</td>
        <td>
          <a href="https://www.warcraftlogs.com/reports/${report.code}" 
             target="_blank" 
             class="wcl-button"
             title="查看详细战斗记录">
            <i class="fas fa-external-link-alt"></i> 查看详情
          </a>
        </td>
      `;
      
      tbody.appendChild(row);
      
      // 添加延迟动画
      setTimeout(() => {
        row.style.transition = 'all 0.3s ease';
        row.style.opacity = '1';
        row.style.transform = 'translateX(0)';
      }, index * 100);
    });
    
    // 显示表格
    this.tableEl.style.display = 'table';
    this.tableEl.style.opacity = '0';
    setTimeout(() => {
      this.tableEl.style.transition = 'opacity 0.5s ease';
      this.tableEl.style.opacity = '1';
    }, 100);
  }
  
  showEmptyState() {
    const tbody = this.tableEl.querySelector('tbody');
    tbody.innerHTML = `
      <tr>
        <td colspan="5" style="text-align: center; padding: 3rem 1rem; color: var(--color-text-secondary);">
          <i class="fas fa-info-circle" style="font-size: 2rem; margin-bottom: 1rem; display: block; color: var(--color-primary);"></i>
          <p style="margin: 0; font-size: 1.1rem;">暂无近期活动记录</p>
          <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.7;">请稍后再来查看最新的团队活动</p>
        </td>
      </tr>
    `;
    
    this.tableEl.style.display = 'table';
    this.tableEl.style.opacity = '0';
    setTimeout(() => {
      this.tableEl.style.transition = 'opacity 0.5s ease';
      this.tableEl.style.opacity = '1';
    }, 100);
  }
  
  showLoading() {
    this.loadingEl.style.display = 'block';
    this.errorEl.style.display = 'none';
    this.tableEl.style.display = 'none';
  }
  
  hideLoading() {
    this.loadingEl.style.display = 'none';
  }
  
  showError(message) {
    this.errorEl.textContent = message;
    this.errorEl.style.display = 'block';
    this.tableEl.style.display = 'none';
  }
  
  hideError() {
    this.errorEl.style.display = 'none';
  }
} 