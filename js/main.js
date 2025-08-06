/**
 * 一起公会网站 - 主JavaScript文件
 * 简化版本 - 基于KISS原则
 */

// 导入配置和错误处理
import { initGlobalErrorHandling } from './config.js';

// 导入核心功能模块
import { ImageModal } from './modules/ImageModal.js';
import { ParticleSystem } from './modules/ParticleSystem.js';
import { GuildStatsLoader } from './modules/GuildStatsLoader.js';
import { IframeErrorHandler } from './modules/IframeErrorHandler.js';
import { WCLDataLoader } from './modules/WCLDataLoader.js';
import { ImageUploader } from './modules/ImageUploader.js';

// 导入组件
import { loadHeader } from './components/header.js';
import { loadFooter } from './components/footer.js';

/*************************
 * 页面初始化
 *************************/

// 动态导入导航组件
async function loadNavigation() {
  const { loadNavigation } = await import('./components/nav.js');
  loadNavigation();
}

async function init() {
  // 初始化全局错误处理
  initGlobalErrorHandling();
  
  // 加载页面组件
  loadHeader();
  await loadNavigation();
  loadFooter();
  
  // 初始化核心功能
  new ParticleSystem();
  window.imageModal = new ImageModal();
  new IframeErrorHandler();
  
  // 条件初始化
  if (document.querySelector('.zoomable')) {
    window.imageModal.registerImages(document.querySelectorAll('.zoomable'));
  }
  
  if (document.getElementById('activeMembers')) {
    const statsLoader = new GuildStatsLoader();
    await statsLoader.init();
  }
  
  // 初始化WCL数据加载器（如果存在相关元素）
  if (document.getElementById('wcl-table')) {
    new WCLDataLoader();
  }
  
  // 初始化图片上传器（如果存在相关元素）
  if (document.getElementById('upload-form')) {
    new ImageUploader();
  }
}

/*************************
 * 全局API暴露
 *************************/

// 只暴露核心功能到全局
window.GuildApp = {
  ImageModal,
  ParticleSystem,
  GuildStatsLoader,
  WCLDataLoader,
  ImageUploader
};

/*************************
 * 事件监听器
 *************************/

document.addEventListener('DOMContentLoaded', init);