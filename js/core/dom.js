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

/** 按 id 取元素，找不到时返回 null（不抛异常） */
export function byId(id) {
  return document.getElementById(id);
}
