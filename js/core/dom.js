/**
 * 轻量 DOM 工具
 */

/** HTML 转义，用于拼接文本节点 */
export function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  })[char]);
}

/** 属性值转义（与文本转义规则一致） */
export const escapeAttr = escapeHtml;

/**
 * 按 id 取元素：
 * - 找不到返回 null（不抛异常）
 * - 没有 document 的环境（Node 测试、将来的 SSR）安全降级为 null
 */
export function byId(id) {
  if (typeof document === 'undefined') return null;
  return document.getElementById(id);
}
