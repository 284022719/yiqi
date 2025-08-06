export function loadNavigation() {
    // 检查当前页面是否在pages文件夹中
    const isInPages = window.location.pathname.includes('/pages/');
    
    // 根据页面位置调整路径前缀
    const homePath = isInPages ? '../index.html' : 'index.html';
    const pagesPath = isInPages ? '' : 'pages/';
    const imgPath = isInPages ? '../img/nav/wcl.png' : 'img/nav/wcl.png';
    
    const navHTML = `
        <ul>
          <li><a href="${homePath}">首页</a></li>
          
          <li class="dropdown">
            <a href="#" class="dropbtn" aria-haspopup="true" aria-expanded="false">实用网站 ▼</a>
            <div class="dropdown-content">
              <a href="https://www.warcraftlogs.com/guild/rankings/586445/latest?difficulty=4" target="_blank" class="dropdown-item">
                <span class="dropdown-icon">
                  <img src="${imgPath}" alt="WCL图标">
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

          <li class="dropdown">
            <a href="#" class="dropbtn" aria-haspopup="true" aria-expanded="false">战术攻略 ▼</a>
            <div class="dropdown-content">
              <a href="${pagesPath}H6.html" target="_blank" class="dropdown-item">
                <div class="dropdown-text">
                  <span class="dropdown-title">H6独臂盗匪</span>
                </div>
              </a>
              <a href="${pagesPath}H7.html" target="_blank" class="dropdown-item">
                <div class="dropdown-text">
                  <span class="dropdown-title">H7穆格·兹伊</span>
                </div>
              </a>
            </div>
          </li>
  
          <li><a href="${pagesPath}gallery.html">公会画廊</a></li>

          <li><a href="${pagesPath}wcl.html">开荒记录</a></li>
          
        </ul>
    `;
    
    const navContainer = document.querySelector('.nav-container');
    if (navContainer) {
      navContainer.innerHTML = navHTML;
    }
  }