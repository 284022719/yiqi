/**
 * 一起公会网站 - 全局配置文件
 */

/*************************
* 全局配置
*************************/
export const CONFIG = {
  particleCount: 150,
  particleColors: ['#FFD700', '#785A28', '#FFFFFF', '#FFA500'],
  maxConnectionDistance: 100
};

/*************************
* 全局错误处理
*************************/
export function initGlobalErrorHandling() {
  window.addEventListener('error', (event) => {
    // 过滤掉B站相关的错误
    if (event.filename && (
      event.filename.includes('bilibili.com') ||
      event.filename.includes('bilivideo.com') ||
      event.message.includes('bilibili') ||
      event.message.includes('compute-pressure') ||
      event.message.includes('cross-origin')
    )) {
      return; // 忽略B站相关错误
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
    // 过滤掉B站相关的Promise错误
    if (event.reason && (
      event.reason.toString().includes('bilibili') ||
      event.reason.toString().includes('compute-pressure') ||
      event.reason.toString().includes('cross-origin')
    )) {
      return; // 忽略B站相关错误
    }
    
    console.error('未处理的Promise拒绝:', event.reason);
  });
} 