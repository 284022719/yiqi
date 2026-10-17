/**
 * 一起公会网站 - 全局配置与错误处理
 */

export const CONFIG = {
  // 置为 true 时输出调试日志；生产环境保持 false
  debug: false,
  particleCount: 150,
  particleColors: ['#FFD700', '#785A28', '#FFFFFF', '#FFA500'],
  maxConnectionDistance: 100
};

/** 调试日志：仅在 CONFIG.debug 为真时输出 */
export function log(...args) {
  if (CONFIG.debug) {
    // eslint-disable-next-line no-console -- 调试日志的唯一出口，统一受 debug 开关控制
    console.log(...args);
  }
}

export function initGlobalErrorHandling() {
  window.addEventListener('error', (event) => {
    // 过滤 B 站播放器产生的跨域噪音
    if (event.filename && (
      event.filename.includes('bilibili.com') ||
      event.filename.includes('bilivideo.com') ||
      (event.message || '').includes('bilibili') ||
      (event.message || '').includes('compute-pressure') ||
      (event.message || '').includes('cross-origin')
    )) {
      return;
    }

    console.error('JavaScript错误:', {
      message: event.message,
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
      error: event.error
    });
  });

  window.addEventListener('unhandledrejection', (event) => {
    const reason = String(event.reason ?? '');

    if (
      reason.includes('bilibili') ||
      reason.includes('compute-pressure') ||
      reason.includes('cross-origin')
    ) {
      return;
    }

    console.error('未处理的Promise拒绝:', event.reason);
  });
}
