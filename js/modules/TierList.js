/**
 * 通用 Tier List 显示模块
 */

export class TierList {
  constructor(containerId, tierData, type = 'dps') {
    this.container = document.getElementById(containerId);
    this.tierData = tierData;
    this.type = type;
    this.init();
  }
  
  init() {
    if (!this.container) return;
    this.render();
  }
  
  render() {
    const typeIcons = { 'dps': '⚔️', 'healer': '💚', 'tank': '🛡️' };
    const typeNames = { 'dps': 'DPS', 'healer': '治疗', 'tank': '坦克' };
    
    this.container.innerHTML = `
      <div class="tier-list">
        <div class="tier-list-header">
          <h2>${typeIcons[this.type]} ${typeNames[this.type]}职业层级排名</h2>
          <div class="tier-list-meta">
            <p class="tier-list-title">${this.tierData.title}</p>
            <p class="tier-list-source">
              数据来源: <a href="${this.tierData.sourceUrl}" target="_blank" rel="noopener">Wowhead</a> 
              (作者: ${this.tierData.source}, 更新: ${this.tierData.lastUpdated})
            </p>
          </div>
        </div>
        <div class="tier-list-container">
          ${this.renderTiers()}
        </div>
      </div>
    `;
    
    this.addAnimations();
  }
  
  renderTiers() {
    const tierOrder = ['S', 'A', 'B', 'C', 'D', 'F'];
    let html = '';
    
    tierOrder.forEach((tierKey, index) => {
      const tier = this.tierData.tiers[tierKey];
      if (!tier || tier.specs.length === 0) return;
      
      html += `
        <div class="tier-row" data-tier="${tierKey}" style="animation-delay: ${index * 0.1}s;">
          <div class="tier-header">
            <div class="tier-label tier-${tierKey.toLowerCase()}">${tier.name}</div>
            <div class="tier-description">${tier.description}</div>
          </div>
          <div class="tier-specs">
            ${this.renderSpecs(tier.specs)}
          </div>
        </div>
      `;
    });
    
    return html;
  }
  
  renderSpecs(specs) {
    return specs.map((spec, index) => {
      const classColorHex = this.getClassColorHex(spec.class);
      
      return `
        <div class="spec-item" 
             style="animation-delay: ${index * 0.05}s; background: ${classColorHex}20; border-left: 4px solid ${classColorHex};"
             data-class="${spec.class}"
             data-spec="${spec.spec}">
          <div class="spec-icon">
            <img src="${spec.specIcon}" alt="${spec.name}" loading="lazy">
          </div>
          <div class="spec-info">
            <div class="spec-name" style="color: ${spec.color};">${spec.spec}</div>
            <div class="spec-class">${spec.class}</div>
          </div>
        </div>
      `;
    }).join('');
  }
  
  getClassColorHex(className) {
    const colorMap = {
      '战士': '#C69B6D', '圣骑士': '#F48CBA', '猎人': '#AAD372',
      '潜行者': '#FFF468', '牧师': '#FFFFFF', '术士': '#8788EE',
      '法师': '#3FC7EB', '武僧': '#00FF98', '死亡骑士': '#C41E3A',
      '德鲁伊': '#FF7C0A', '萨满祭司': '#0070DD', '恶魔猎手': '#A330C9',
      '唤魔师': '#33937F'
    };
    
    return colorMap[className] || '#FF6B35';
  }
  
  addAnimations() {
    const style = document.createElement('style');
    style.textContent = `
      .tier-list {
        background: var(--color-bg-secondary);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      }
      
      .tier-list-header {
        text-align: center;
        margin-bottom: 2rem;
      }
      
      .tier-list-header h2 {
        color: var(--color-primary);
        margin-bottom: 0.5rem;
        font-size: 1.8rem;
      }
      
      .tier-list-meta {
        color: var(--color-text-secondary);
        font-size: 0.9rem;
      }
      
      .tier-list-title {
        font-weight: 600;
        margin-bottom: 0.25rem;
      }
      
      .tier-list-source a {
        color: var(--color-primary);
        text-decoration: none;
      }
      
      .tier-list-source a:hover {
        text-decoration: underline;
      }
      
      .tier-row {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: var(--color-bg);
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        opacity: 0;
        transform: translateY(20px);
        animation: fadeInUp 0.6s ease forwards;
      }
      
      .tier-header {
        min-width: 200px;
        margin-right: 2rem;
      }
      
      .tier-label {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        text-align: center;
      }
      
      .tier-s { background: #FFD700; color: #000; font-weight: bold; }
      .tier-a { background: #FF6B6B; color: #fff; font-weight: bold; }
      .tier-b { background: #4ECDC4; color: #fff; font-weight: bold; }
      .tier-c { background: #A8E6CF; color: #000; font-weight: bold; }
      .tier-d { background: #FFB6C1; color: #000; font-weight: bold; }
      .tier-f { background: #D3D3D3; color: #000; font-weight: bold; }
      
      .tier-description {
        font-size: 0.9rem;
        color: var(--color-text-secondary);
        text-align: center;
      }
      
      .tier-specs {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        flex: 1;
      }
      
      .spec-item {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        border-radius: 8px;
        border: 2px solid transparent;
        border-left: 4px solid;
        transition: all 0.3s ease;
        cursor: pointer;
        opacity: 0;
        transform: scale(0.9);
        animation: fadeInScale 0.4s ease forwards;
        width: 200px;
        min-width: 200px;
        box-sizing: border-box;
        backdrop-filter: blur(10px);
      }
      
      .spec-item:hover {
        border-color: var(--color-primary);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      }
      
      .spec-icon {
        width: 32px;
        height: 32px;
        margin-right: 0.75rem;
        border-radius: 50%;
        overflow: hidden;
        background: var(--color-bg);
      }
      
      .spec-icon img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      
      .spec-info {
        display: flex;
        flex-direction: column;
      }
      
      .spec-name {
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
      }
      
      .spec-class {
        font-size: 0.8rem;
        color: var(--color-text-secondary);
      }
      
      @keyframes fadeInUp {
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
      
      @keyframes fadeInScale {
        to {
          opacity: 1;
          transform: scale(1);
        }
      }
      
      @media (max-width: 768px) {
        .tier-list { padding: 1rem; }
        .tier-row { flex-direction: column; align-items: flex-start; }
        .tier-header { min-width: auto; margin-right: 0; margin-bottom: 1rem; width: 100%; }
        .tier-specs { width: 100%; justify-content: center; }
        .spec-item { width: 180px; min-width: 180px; margin: 0.25rem; }
      }
      
      @media (max-width: 480px) {
        .spec-item { width: 160px; min-width: 160px; }
        .tier-specs { justify-content: flex-start; }
      }
    `;
    
    document.head.appendChild(style);
  }
}
