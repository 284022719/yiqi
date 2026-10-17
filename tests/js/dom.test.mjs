/**
 * core/dom.js 的最小测试：转义是防注入的最后一道，必须有回归保护。
 */
import { test, describe } from 'node:test';
import assert from 'node:assert/strict';

import { escapeAttr, escapeHtml, byId } from '../../js/core/dom.js';

describe('escapeHtml', () => {
  test('转义 HTML 元字符', () => {
    assert.equal(escapeHtml('<script>alert(1)</script>'), '&lt;script&gt;alert(1)&lt;/script&gt;');
  });

  test('转义引号与 &', () => {
    assert.equal(escapeHtml(`& " '`), '&amp; &quot; &#39;');
  });

  test('普通文本原样返回', () => {
    assert.equal(escapeHtml('一起公会'), '一起公会');
  });

  test('null / undefined 退化为空串', () => {
    assert.equal(escapeHtml(null), '');
    assert.equal(escapeHtml(undefined), '');
  });

  test('数字被转成字符串', () => {
    assert.equal(escapeHtml(965), '965');
  });
});

describe('escapeAttr', () => {
  test('与 escapeHtml 规则一致', () => {
    const value = `x" onmouseover="alert(1)`;
    assert.equal(escapeAttr(value), escapeHtml(value));
    assert.ok(!escapeAttr(value).includes('"'));
  });
});

describe('byId', () => {
  test('没有 document 时返回 null 而不是抛错', () => {
    // 本测试在 Node 下运行，没有 document —— byId 应安全降级
    assert.equal(byId('anything'), null);
  });
});
