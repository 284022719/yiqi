/**
 * iframe错误处理
 */
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
    
    // 创建备用内容
    const fallbackHTML = `
      <div class="iframe-fallback" style="
        width: 100%;
        height: 400px;
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #FFD700;
        text-align: center;
        padding: 20px;
        border: 2px solid #FFD700;
      ">
        <div style="font-size: 48px; margin-bottom: 20px;">📺</div>
        <h3 style="margin: 0 0 10px 0; color: #FFD700;">视频加载失败</h3>
        <p style="margin: 0 0 20px 0; color: #ccc;">由于网络或权限限制，无法加载视频内容</p>
        <a href="${iframe.src}" target="_blank" style="
          background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
          color: #000;
          padding: 10px 20px;
          border-radius: 5px;
          text-decoration: none;
          font-weight: bold;
          transition: all 0.3s ease;
        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
          在新窗口打开视频
        </a>
      </div>
    `;
    
    // 替换iframe
    iframe.style.display = 'none';
    container.insertAdjacentHTML('beforeend', fallbackHTML);
  }
} 