/**
 * 内联 SVG 图标集
 *
 * 只收录 UI 控件里用到的功能性图标；正文里的装饰性 emoji（如攻略页标题的 🏮）
 * 属于内容表达，继续保留 emoji。
 *
 * 用法：icon('shield') → 一段 <svg>，尺寸随 font-size（1em），颜色随 currentColor。
 */

const PATHS = {
  sword:
    '<path d="M12 1.8 15 9H9l3-7.2Z"/>' +
    '<rect x="5.2" y="9.2" width="13.6" height="2.2" rx="1.1"/>' +
    '<rect x="10.9" y="11.4" width="2.2" height="6.6" rx="1.1"/>' +
    '<circle cx="12" cy="20.2" r="1.7"/>',
  heart:
    '<path d="M12 20.5S3.8 15.4 3.8 9.6A4.7 4.7 0 0 1 12 6.3a4.7 4.7 0 0 1 8.2 3.3c0 5.8-8.2 10.9-8.2 10.9Z"/>',
  shield:
    '<path d="M12 2.2 20 5v6.3c0 5.1-3.5 8.4-8 9.7-4.5-1.3-8-4.6-8-9.7V5l8-2.8Z"/>',
  castle:
    '<path d="M3 21V8h3V4.5h3V8h6V4.5h3V8h3v13H3Zm5-3.5h3v-3H8v3Zm5 0h3v-3h-3v3Z"/>',
  bolt: '<path d="M13.2 2 4 14.2h6L8.8 22 20 9.8h-6.2L13.2 2Z"/>',
  trophy:
    '<path d="M6 4h12v4a6 6 0 0 1-5 5.9V18h3v3H8v-3h3v-4.1A6 6 0 0 1 6 8V4Z"/>',
  key:
    '<path d="M15 2a6 6 0 0 0-4.2 10.3L4 19.1V22h3l1-1v-2h2v-2h2l1.3-1.3A6 6 0 1 0 15 2Zm1.5 3a1.8 1.8 0 1 1 0 3.6 1.8 1.8 0 0 1 0-3.6Z"/>',
  tv:
    '<path d="M4 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Zm8 3.6v7.2l5.5-3.6L12 7.6ZM9 21h6v-2H9v2Z"/>'
};

/**
 * @param {keyof typeof PATHS} name
 * @param {string} className
 * @returns {string} SVG 标记；未知名称返回空串
 */
export function icon(name, className = 'icon') {
  const body = PATHS[name];
  if (!body) return '';

  return (
    `<svg class="${className}" viewBox="0 0 24 24" width="1em" height="1em" ` +
    `fill="currentColor" fill-rule="evenodd" aria-hidden="true" focusable="false">` +
    `${body}</svg>`
  );
}

export default icon;
