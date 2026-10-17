/**
 * 页头组件
 *
 * 路径判断与 nav.js 保持一致：不依赖「`..` 超出根会被浏览器钳制」这一隐式行为。
 */

export function loadHeader() {
  const isInPages = window.location.pathname.includes('/pages/');
  const logoPath = isInPages ? '../img/header-logo.webp' : 'img/header-logo.webp';

  const headerHTML = `
      <div class="header-content">
        <div class="header-logo">
          <img src="${logoPath}" alt="公会标志" class="logo-image" width="465" height="600">
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
