/**
 * 通用 Tier List 显示模块
 *
 * 天梯数据只保存专精 id（如 'paladin|防护'），图标与职业信息统一由 specs.js 提供；
 * 职业颜色统一从 CSS 变量解析（wow-classes.js#resolveClassColor），样式全部在 css/tier-list.css。
 */

import { resolveSpec } from '../data/specs.js';
import { resolveClassColor } from '../data/wow-classes.js';
import { escapeAttr, escapeHtml } from '../core/dom.js';
import { icon } from '../core/icons.js';

const TIER_ORDER = ['S', 'A', 'B', 'C', 'D', 'F'];

const TYPE_ICONS = { dps: icon('sword'), healer: icon('heart'), tank: icon('shield') };
const TYPE_NAMES = { dps: 'DPS', healer: '治疗', tank: '坦克' };

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
    this.container.innerHTML = `
      <div class="tier-list">
        <div class="tier-list-header">
          <h2>${TYPE_ICONS[this.type] || ''} ${TYPE_NAMES[this.type] || ''}职业层级排名</h2>
          <div class="tier-list-meta">
            <p class="tier-list-title">${escapeHtml(this.tierData.title)}</p>
            <p class="tier-list-source">
              数据来源: <a href="${escapeAttr(this.tierData.sourceUrl)}" target="_blank" rel="noopener">Wowhead</a>
              (作者: ${escapeHtml(this.tierData.source)}, 更新: ${escapeHtml(this.tierData.lastUpdated)})
            </p>
          </div>
        </div>
        <div class="tier-list-container">
          ${this.renderTiers()}
        </div>
      </div>
    `;
  }

  renderTiers() {
    return TIER_ORDER.map((tierKey, index) => {
      const tier = this.tierData.tiers[tierKey];
      if (!tier || !tier.specs || tier.specs.length === 0) return '';

      const description = tier.description
        ? `<div class="tier-description">${escapeHtml(tier.description)}</div>`
        : '';

      return `
        <div class="tier-row" data-tier="${tierKey}" style="--tier-index:${index};">
          <div class="tier-header">
            <div class="tier-label tier-${tierKey.toLowerCase()}">${escapeHtml(tier.name)}</div>
            ${description}
          </div>
          <div class="tier-specs">
            ${this.renderSpecs(tier.specs)}
          </div>
        </div>
      `;
    }).join('');
  }

  renderSpecs(specIds) {
    return specIds.map((id, index) => {
      let spec;
      try {
        spec = resolveSpec(id);
      } catch (error) {
        console.warn(`TierList: 跳过无法解析的专精 ${id}`);
        return '';
      }

      const color = resolveClassColor(spec.class);

      return `
        <div class="spec-item"
             data-class="${escapeAttr(spec.class)}"
             data-spec="${escapeAttr(spec.spec)}"
             style="--spec-index:${index}; --class-color:${escapeAttr(color)};">
          <div class="spec-icon">
            <img src="${escapeAttr(spec.icon)}" alt="${escapeAttr(spec.name)}" loading="lazy" width="32" height="32">
          </div>
          <div class="spec-info">
            <div class="spec-name">${escapeHtml(spec.spec)}</div>
            <div class="spec-class">${escapeHtml(spec.class)}</div>
          </div>
        </div>
      `;
    }).join('');
  }
}
