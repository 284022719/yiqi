/**
 * 一起公会网站 - 主入口
 * 负责组件加载与按页面条件初始化各功能模块。
 */

import { initGlobalErrorHandling } from './config.js';

import { ImageModal } from './modules/ImageModal.js';
import { ParticleSystem } from './modules/ParticleSystem.js';
import { GuildStatsLoader } from './modules/GuildStatsLoader.js';
import { IframeErrorHandler } from './modules/IframeErrorHandler.js';
import { WCLDataLoader } from './modules/WCLDataLoader.js';
import { ImageUploader } from './modules/ImageUploader.js';

import { loadHeader } from './components/header.js';
import { loadFooter } from './components/footer.js';

/** 出现这些元素时页面以数据展示为主，跳过背景粒子动画（省电、省 CPU） */
const DATA_HEAVY_ELEMENTS = ['wcl-table', 'ranking-nav-container'];

async function loadNavigation() {
  const { loadNavigation } = await import('./components/nav.js');
  loadNavigation();
}

function shouldStartParticles() {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return false;
  }
  return !DATA_HEAVY_ELEMENTS.some((id) => document.getElementById(id));
}

async function init() {
  initGlobalErrorHandling();

  loadHeader();
  await loadNavigation();
  loadFooter();

  if (shouldStartParticles()) {
    new ParticleSystem();
  }

  window.imageModal = new ImageModal();
  new IframeErrorHandler();

  const zoomables = document.querySelectorAll('.zoomable');
  if (zoomables.length > 0) {
    window.imageModal.registerImages(zoomables);
  }

  if (document.getElementById('totalMembers') || document.getElementById('activeMembers')) {
    await new GuildStatsLoader().init();
  }

  if (document.getElementById('wcl-table')) {
    new WCLDataLoader();
  }

  if (document.getElementById('upload-form')) {
    new ImageUploader();
  }
}

// 供浏览器控制台调试使用
window.GuildApp = {
  ImageModal,
  ParticleSystem,
  GuildStatsLoader,
  WCLDataLoader,
  ImageUploader
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
