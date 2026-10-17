/**
 * 排名导航组件
 * 用于在总览页面中快速跳转到不同排名部分。
 * 样式见 css/ranking-nav.css。
 */

const TARGET_MAP = {
  'raid-dps': 'raid-dps-tier-list-container',
  'raid-healer': 'raid-healer-tier-list-container',
  'raid-tank': 'raid-tank-tier-list-container',
  'mplus-dps': 'mplus-dps-tier-list-container',
  'mplus-healer': 'mplus-healer-tier-list-container',
  'mplus-tank': 'mplus-tank-tier-list-container'
};

export class RankingNav {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  init() {
    if (!this.container) return;
    this.render();
    this.addEventListeners();
  }

  render() {
    this.container.innerHTML = `
      <div class="ranking-nav">
        <div class="nav-section">
          <h3>🏰 团本排名</h3>
          <div class="nav-buttons">
            <button class="nav-btn" data-target="raid-dps">⚔️ DPS</button>
            <button class="nav-btn" data-target="raid-healer">💚 治疗</button>
            <button class="nav-btn" data-target="raid-tank">🛡️ 坦克</button>
          </div>
        </div>
        <div class="nav-section">
          <h3>⚡ 大秘境排名</h3>
          <div class="nav-buttons">
            <button class="nav-btn" data-target="mplus-dps">⚔️ DPS</button>
            <button class="nav-btn" data-target="mplus-healer">💚 治疗</button>
            <button class="nav-btn" data-target="mplus-tank">🛡️ 坦克</button>
          </div>
        </div>
      </div>
    `;
  }

  addEventListeners() {
    this.container.querySelectorAll('.nav-btn').forEach((button) => {
      button.addEventListener('click', () => {
        this.scrollToSection(button.getAttribute('data-target'));
      });
    });
  }

  scrollToSection(target) {
    const containerId = TARGET_MAP[target];
    if (!containerId) return;

    const element = document.getElementById(containerId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
}
