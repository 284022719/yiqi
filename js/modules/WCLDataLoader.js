/**
 * WCL数据处理器
 */
export class WCLDataLoader {
  constructor() {
    this.loadingEl = document.getElementById('loading');
    this.errorEl = document.getElementById('error');
    this.tableEl = document.getElementById('wcl-table');
    
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
      throw new Error('没有找到近期活动记录');
    }
    
    const tbody = this.tableEl.querySelector('tbody');
    tbody.innerHTML = '';
    
    reports.forEach(report => {
      const row = document.createElement('tr');
      const date = new Date(report.startTime);
      const killCount = report.fights.filter(f => f.kill).length;
      const totalEncounters = new Set(report.fights.map(f => f.encounterID)).size;
      
      row.innerHTML = `
        <td>${date.toLocaleDateString('zh-CN')}</td>
        <td>${report.zone?.name || '未知区域'}</td>
        <td>${killCount}/${totalEncounters}</td>
        <td>${report.owner?.name || '未知'}</td>
        <td>
          <a href="https://www.warcraftlogs.com/reports/${report.code}" 
             target="_blank" 
             class="button wcl-button">
            查看详情
          </a>
        </td>
      `;
      
      tbody.appendChild(row);
    });
    
    this.tableEl.style.display = 'table';
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
  }
} 