/**
 * 排名导航组件
 * 用于在总览页面中快速跳转到不同排名部分
 */

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
    
    this.addStyles();
  }
  
  addEventListeners() {
    const buttons = this.container.querySelectorAll('.nav-btn');
    buttons.forEach(button => {
      button.addEventListener('click', () => {
        const target = button.getAttribute('data-target');
        this.scrollToSection(target);
      });
    });
  }
  
  scrollToSection(target) {
    let containerId;
    switch(target) {
      case 'raid-dps':
        containerId = 'raid-dps-tier-list-container';
        break;
      case 'raid-healer':
        containerId = 'raid-healer-tier-list-container';
        break;
      case 'raid-tank':
        containerId = 'raid-tank-tier-list-container';
        break;
      case 'mplus-dps':
        containerId = 'mplus-dps-tier-list-container';
        break;
      case 'mplus-healer':
        containerId = 'mplus-healer-tier-list-container';
        break;
      case 'mplus-tank':
        containerId = 'mplus-tank-tier-list-container';
        break;
      default:
        return;
    }
    
    const element = document.getElementById(containerId);
    if (element) {
      element.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
      });
    }
  }
  
  addStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .ranking-nav {
        background: var(--color-bg-secondary);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }
      
      .ranking-nav .nav-section {
        margin-bottom: 1.5rem;
      }
      
      .ranking-nav .nav-section:last-child {
        margin-bottom: 0;
      }
      
      .ranking-nav h3 {
        color: var(--color-primary);
        margin-bottom: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
      }
      
      .nav-buttons {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
      }
      
      .nav-btn {
        background: var(--color-bg);
        border: 2px solid var(--color-primary);
        color: var(--color-primary);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s ease;
        min-width: 80px;
      }
      
      .nav-btn:hover {
        background: var(--color-primary);
        color: var(--color-bg);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      }
      
      .nav-btn:active {
        transform: translateY(0);
      }
      
      @media (max-width: 768px) {
        .nav-buttons {
          justify-content: center;
        }
        
        .nav-btn {
          min-width: 70px;
          padding: 0.4rem 0.8rem;
          font-size: 0.8rem;
        }
      }
    `;
    
    document.head.appendChild(style);
  }
}

