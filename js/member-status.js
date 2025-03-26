// 成员在线状态功能
class MemberStatus {
  constructor() {
    this.onlineMembers = document.getElementById('online-members');
    this.init();
  }
  
  async init() {
    try {
      await this.fetchMemberStatus();
      // 每60秒刷新一次数据
      setInterval(() => this.fetchMemberStatus(), 60000);
    } catch (error) {
      this.showError(error);
    }
  }
  
  async fetchMemberStatus() {
    try {
      const response = await fetch('/.netlify/functions/member-status');
      if (!response.ok) throw new Error('网络响应不正常');
      
      const data = await response.json();
      if (!data.members) throw new Error('数据格式不正确');
      
      this.renderMembers(data.members);
    } catch (error) {
      this.showError(error);
    }
  }
  
  renderMembers(members) {
    const onlineCount = members.filter(m => m.status !== 'offline').length;
    const title = `成员在线状态 (${onlineCount}/${members.length})`;
    
    let html = `<h3>${title}</h3>`;
    
    members.forEach(member => {
      html += `
        <div class="online-member">
          <img src="${member.avatar || 'img/classes/default.png'}" 
               class="member-avatar" 
               alt="${member.name}"
               onerror="this.src='img/classes/default.png'">
          <span class="member-status status-${member.status}"></span>
          <span class="member-name">${member.name}</span>
          ${member.activity ? `<span class="member-activity">- ${member.activity}</span>` : ''}
        </div>
      `;
    });
    
    this.onlineMembers.innerHTML = html;
  }
  
  showError(error) {
    this.onlineMembers.innerHTML = `
      <div class="error">
        <i class="fas fa-exclamation-triangle"></i> 
        无法加载成员状态: ${error.message}
      </div>
    `;
  }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  new MemberStatus();
});
