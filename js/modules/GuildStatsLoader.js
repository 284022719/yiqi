/**
 * 公会统计数据加载与渲染
 *
 * 数据来源：data/page_data.json（由 tools/build_page_data.py 生成）。
 * 图表渲染统一走 components/Chart.js，本模块只负责取数与映射。
 */

import { getClassIcon, getClassInfo, resolveClassColor } from '../data/wow-classes.js';
import {
  DEFAULT_CHART_COLOR,
  FACTION_COLORS,
  FACTION_NAMES,
  GENDER_COLORS,
  RACE_COLORS,
  REALM_COLORS
} from '../data/palettes.js';
import { renderBarChart, renderPieChart } from '../components/Chart.js';
import { byId, escapeAttr, escapeHtml } from '../core/dom.js';
import { icon } from '../core/icons.js';
import { log } from '../config.js';

const REALM_LIMIT = 25;

const STATS_DATA_URL = window.location.pathname.includes('/pages/')
  ? '../data/page_data.json'
  : 'data/page_data.json';

function setText(id, value) {
  const element = byId(id);
  if (element && value !== null && value !== undefined) {
    element.textContent = value;
  }
}

function emptyRow(colspan, iconName, title, note) {
  return `
    <tr>
      <td colspan="${colspan}" class="table-empty">
        <div class="table-empty-icon">${icon(iconName)}</div>
        <div class="table-empty-title">${escapeHtml(title)}</div>
        <div class="table-empty-note">${escapeHtml(note)}</div>
      </td>
    </tr>
  `;
}

export class GuildStatsLoader {
  constructor() {
    this.statsData = null;
  }

  async init() {
    try {
      await this.loadStats();
      this.renderStats();
      this.renderCharts();
      this.renderRankings();
    } catch (error) {
      console.error('GuildStatsLoader: 加载统计数据失败:', error.message);
      this.showError('统计数据加载失败，请稍后重试');
    }
  }

  async loadStats() {
    const response = await fetch(STATS_DATA_URL);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    this.statsData = await response.json();
    log('GuildStatsLoader: 数据已加载', this.statsData.meta);
  }

  // ------------------------------------------------------------------ 概览

  renderStats() {
    const stats = this.statsData?.stats;
    if (!stats) return;

    const activeWindow = stats.activeWindow;
    const generatedAt = this.statsData.lastUpdated || '未知';
    const dataAsOf = this.statsData.dataAsOf || activeWindow?.latest || generatedAt;

    setText('totalMembers', stats.totalMembers);
    setText('activeMembers', stats.activeMembers);
    // 展示「数据本身截至的时间」，避免把生成时间误读成数据新鲜度
    setText('lastUpdated', dataAsOf);
    setText('activeWindowHint', ` · 页面生成于 ${generatedAt}`);

    if (stats.dataCompleteness) {
      setText('dataCompleteness', `${stats.dataCompleteness.percentage}%`);
    }

    if (activeWindow?.days) {
      setText('activeMembersLabel', `近 ${activeWindow.days} 天活跃`);
    }
  }

  // ------------------------------------------------------------------ 图表

  renderCharts() {
    const charts = this.statsData?.charts || {};
    document.querySelector('.stats-charts')?.setAttribute('aria-busy', 'false');

    renderBarChart(byId('classChart'), charts.classDistribution, {
      colorOf: (name) => resolveClassColor(name),
      emptyText: '暂无职业数据'
    });

    renderPieChart(byId('factionChart'), charts.factionDistribution, {
      colorOf: (name) => FACTION_COLORS[name] || DEFAULT_CHART_COLOR,
      labelOf: (item) => FACTION_NAMES[item.name] || item.name,
      emptyText: '暂无阵营数据'
    });

    renderPieChart(byId('genderChart'), charts.genderDistribution, {
      colorOf: (name) => GENDER_COLORS[name] || GENDER_COLORS['未知'],
      emptyText: '暂无性别数据'
    });

    renderBarChart(byId('raceChart'), charts.raceDistribution, {
      colorOf: (name) => RACE_COLORS[name] || DEFAULT_CHART_COLOR,
      emptyText: '暂无种族数据'
    });

    renderBarChart(byId('realmChart'), (charts.realmDistribution || []).slice(0, REALM_LIMIT), {
      colorOf: (name) => REALM_COLORS[name] || DEFAULT_CHART_COLOR,
      emptyText: '暂无服务器数据'
    });
  }

  // ------------------------------------------------------------------ 排行

  renderRankings() {
    this.renderAchievementRanking();
    this.renderMythicScoreRanking();
  }

  renderAchievementRanking() {
    const container = byId('achievementRanking');
    const tbody = container?.querySelector('tbody');
    if (!tbody) return;

    const data = this.statsData?.rankings?.achievementRanking || [];
    if (data.length === 0) {
      tbody.innerHTML = emptyRow(4, 'trophy', '暂无成就点数数据', '请稍后再试');
      return;
    }

    tbody.innerHTML = data.map((item) => {
      const classColor = getClassInfo(item.class)?.color || 'var(--color-text)';

      return `
        <tr>
          <td class="rank ${item.rank <= 3 ? 'top-3' : ''}">${item.rank}</td>
          <td class="character-name">${escapeHtml(item.name)}</td>
          <td class="class" style="color: ${classColor};">
            <img src="${escapeAttr(getClassIcon(item.class))}" alt="${escapeAttr(item.class)}" class="class-icon-img" loading="lazy">
            ${escapeHtml(item.class)}
          </td>
          <td class="achievement-points">${Number(item.achievement_points || 0).toLocaleString()}</td>
        </tr>
      `;
    }).join('');
  }

  renderMythicScoreRanking() {
    const container = byId('mythicScoreRanking');
    const tbody = container?.querySelector('tbody');
    if (!tbody) return;

    const data = this.statsData?.rankings?.mythicScoreRanking || [];
    if (data.length === 0) {
      tbody.innerHTML = emptyRow(5, 'key', '暂无史诗钥石评分数据', '当前数据中所有角色的史诗钥石评分均为 0');
      return;
    }

    tbody.innerHTML = data.map((item) => {
      const classColor = getClassInfo(item.class)?.color || 'var(--color-text)';
      const itemLevel = item.average_item_level
        ? Number(item.average_item_level).toFixed(1)
        : 'N/A';

      return `
        <tr>
          <td class="rank ${item.rank <= 3 ? 'top-3' : ''}">${item.rank}</td>
          <td class="character-name">${escapeHtml(item.name)}</td>
          <td class="class" style="color: ${classColor};">
            <img src="${escapeAttr(getClassIcon(item.class))}" alt="${escapeAttr(item.class)}" class="class-icon-img" loading="lazy">
            ${escapeHtml(item.class)}
          </td>
          <td class="mythic-score">${Number(item.mythic_score || 0).toLocaleString()}</td>
          <td class="item-level">${itemLevel}</td>
        </tr>
      `;
    }).join('');
  }

  // ------------------------------------------------------------------ 兜底

  showError(message) {
    ['classChart', 'factionChart', 'genderChart', 'raceChart', 'realmChart'].forEach((id) => {
      const container = byId(id);
      if (container) {
        container.innerHTML = `<p class="chart-empty">${escapeHtml(message)}</p>`;
      }
    });
  }
}
