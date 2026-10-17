/**
 * iframe错误处理
 */

import { icon } from '../core/icons.js';
import { escapeAttr } from '../core/dom.js';

export class IframeErrorHandler {
  constructor() {
    this.init();
  }
  
  init() {
    // 处理所有iframe的加载错误
    const iframes = document.querySelectorAll('iframe');
    iframes.forEach(iframe => {
      this.setupIframeErrorHandling(iframe);
    });
  }
  
  setupIframeErrorHandling(iframe) {
    // 监听加载错误
    iframe.addEventListener('error', (e) => {
      console.warn('iframe加载失败:', e.target.src);
      this.showFallbackContent(iframe);
    });
    
    // 监听加载超时
    const timeout = setTimeout(() => {
      if (iframe.contentDocument === null) {
        console.warn('iframe加载超时:', iframe.src);
        this.showFallbackContent(iframe);
      }
    }, 10000); // 10秒超时
    
    // 加载成功后清除超时
    iframe.addEventListener('load', () => {
      clearTimeout(timeout);
    });
  }
  
  showFallbackContent(iframe) {
    const container = iframe.parentElement;
    if (!container) return;

    // 样式全部在 css/media.css 的 .iframe-fallback 系列里；
    // 这里只输出结构，避免内联样式与 CSS 冲突、也避免内联事件处理器（CSP）
    const fallbackHTML = `
      <div class="iframe-fallback">
        <div class="iframe-fallback-icon">${icon('tv')}</div>
        <h3>视频加载失败</h3>
        <p>由于网络或权限限制，无法加载视频内容</p>
        <a href="${escapeAttr(iframe.src)}" target="_blank" rel="noopener">在新窗口打开视频</a>
      </div>
    `;

    // 替换iframe
    iframe.style.display = 'none';
    container.insertAdjacentHTML('beforeend', fallbackHTML);
  }
} 