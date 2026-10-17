/**
 * 图表渲染组件
 *
 * 原先 GuildStatsLoader 里有 3 份近乎逐行重复的条形图与 2 份饼图实现，
 * 这里统一为两个纯渲染函数：只负责把数据转成 DOM，不关心数据来源。
 */

import { escapeAttr, escapeHtml } from '../core/dom.js';

function emptyState(text) {
  return `<p class="chart-empty">${escapeHtml(text)}</p>`;
}

/**
 * 条形图
 * @param {HTMLElement|null} container
 * @param {Array<{name: string, value: number}>} items
 * @param {{colorOf?: (name: string) => string, labelOf?: (item: object) => string, emptyText?: string}} options
 */
export function renderBarChart(container, items, options = {}) {
  if (!container) return;

  const {
    colorOf = () => 'var(--color-primary)',
    labelOf = (item) => item.name,
    emptyText = '暂无数据'
  } = options;

  if (!Array.isArray(items) || items.length === 0) {
    container.innerHTML = emptyState(emptyText);
    return;
  }

  const max = Math.max(...items.map((item) => Number(item.value) || 0));
  if (max <= 0) {
    container.innerHTML = emptyState(emptyText);
    return;
  }

  container.innerHTML = items.map((item) => {
    const value = Number(item.value) || 0;
    const percent = ((value / max) * 100).toFixed(1);
    const color = escapeAttr(colorOf(item.name));

    return `
      <div class="chart-bar">
        <span class="chart-bar-label" style="color: ${color};">${escapeHtml(labelOf(item))}</span>
        <div class="chart-bar-fill" style="width: ${percent}%; background: linear-gradient(90deg, ${color} 0%, ${color}80 100%);"></div>
        <span class="chart-bar-value">${escapeHtml(value)}</span>
      </div>
    `;
  }).join('');
}

/**
 * 饼图（含图例）
 * @param {HTMLElement|null} container
 * @param {Array<{name: string, value: number}>} items
 * @param {{colorOf: (name: string) => string, labelOf?: (item: object) => string, emptyText?: string}} options
 */
export function renderPieChart(container, items, options = {}) {
  if (!container) return;

  const {
    colorOf,
    labelOf = (item) => item.name,
    emptyText = '暂无数据'
  } = options;

  if (!Array.isArray(items) || items.length === 0 || !colorOf) {
    container.innerHTML = emptyState(emptyText);
    return;
  }

  const total = items.reduce((sum, item) => sum + (Number(item.value) || 0), 0);
  if (total <= 0) {
    container.innerHTML = emptyState(emptyText);
    return;
  }

  let angle = 0;
  const stops = items.map((item) => {
    const start = angle;
    angle += ((Number(item.value) || 0) / total) * 360;
    return `${colorOf(item.name)} ${start}deg ${angle}deg`;
  });

  container.innerHTML = `
    <div class="chart-pie" style="background: conic-gradient(${stops.join(', ')});">
      <div class="chart-pie-center">${total}</div>
    </div>
    <ul class="chart-legend">
      ${items.map((item) => {
        const value = Number(item.value) || 0;
        const percent = ((value / total) * 100).toFixed(1);
        const color = escapeAttr(colorOf(item.name));
        return `
          <li>
            <span class="chart-legend-dot" style="background: ${color};"></span>
            <span class="chart-legend-name" style="color: ${color};">${escapeHtml(labelOf(item))}</span>
            <span class="chart-legend-value">${value} (${percent}%)</span>
          </li>
        `;
      }).join('')}
    </ul>
  `;
}
