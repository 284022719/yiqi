export function loadHeader() {
    const headerHTML = `
      <div class="header-content">
        <div class="header-logo">
          <img src="img/header-logo.png" alt="公会标志" class="logo-image">
        </div>
        <div class="header-text">
          <h1 class="guild-title">一起公会</h1>
          <p class="guild-motto">打本 休闲 洗脚</p>
        </div>
      </div>
    `;
    
    const headerContainer = document.querySelector('.guild-header-container');
    if (headerContainer) {
      headerContainer.innerHTML = headerHTML;
    }
  }