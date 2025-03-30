export function loadNavigation() {
    const navHTML = `
      <nav class="nav" aria-label="主菜单">
        <ul>
          <li><a href="index.html">首页</a></li>
          
          <li class="dropdown">
            <a href="#" class="dropbtn" aria-haspopup="true" aria-expanded="false">实用网站 ▼</a>
            <div class="dropdown-content">
              <a href="https://www.warcraftlogs.com/guild/rankings/586445/latest?difficulty=4" target="_blank" class="dropdown-item">
                <span class="dropdown-icon">
                  <img src="img/nav/wcl.png" alt="WCL图标">
                </span>
                <div class="dropdown-text">
                  <span class="dropdown-title">Warcraft Logs</span>
                  <span class="dropdown-desc">战斗数据分析与排行</span>
                </div>
              </a>
              <a href="https://raider.io" target="_blank" class="dropdown-item">
                <span class="dropdown-icon">
                  <img src="https://cdn.raiderio.net/images/mstile-144x144.png" alt="Raider.IO图标">
                </span>
                <div class="dropdown-text">
                  <span class="dropdown-title">Raider.IO</span>
                  <span class="dropdown-desc">大秘境评分</span>
                </div>
              </a>
            </div>
          </li>
  
          <li class="dropdown">
            <a href="#" class="dropbtn">团本工具 ▼</a>
            <div class="dropdown-content">
              <a href="https://raidplan.io/plan/create?raid=wow.undermine" target="_blank" class="dropdown-item">        
                <div class="dropdown-text">
                  <span class="dropdown-title">RaidPlan</span>
                  <span class="dropdown-desc">战术图绘制</span>
                </div>
              </a>
            </div>
          </li>
  
          <li><a href="wcl.html">开荒记录</a></li>
        </ul>
      </nav>
    `;
    
    const header = document.querySelector('.guild-header');
    if (header) {
      header.insertAdjacentHTML('afterend', navHTML);
    }
  }