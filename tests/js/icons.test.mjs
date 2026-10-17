/**
 * icons.js：图标集是纯字符串生成，适合直接断言。
 */
import { test, describe } from 'node:test';
import assert from 'node:assert/strict';

import { icon } from '../../js/core/icons.js';

const NAMES = ['sword', 'heart', 'shield', 'castle', 'bolt', 'trophy', 'key', 'tv'];

describe('icon', () => {
  test('每个图标都能生成 svg', () => {
    for (const name of NAMES) {
      const svg = icon(name);
      assert.ok(svg.startsWith('<svg'), `${name} 应以 <svg 开头`);
      assert.ok(svg.endsWith('</svg>'), `${name} 应以 </svg> 结尾`);
      assert.ok(svg.includes('viewBox="0 0 24 24"'), `${name} 缺少 viewBox`);
    }
  });

  test('颜色与尺寸交给 CSS：使用 currentColor 与 1em', () => {
    const svg = icon('shield');
    assert.ok(svg.includes('currentColor'));
    assert.ok(svg.includes('width="1em"') && svg.includes('height="1em"'));
  });

  test('对读屏软件隐藏（装饰性图标）', () => {
    assert.ok(icon('heart').includes('aria-hidden="true"'));
  });

  test('自定义 class 生效', () => {
    assert.ok(icon('key', 'my-icon').includes('class="my-icon"'));
  });

  test('未知名称返回空串而不是抛错', () => {
    assert.equal(icon('not-exist'), '');
    assert.equal(icon(), '');
  });

  test('不再包含 emoji（回归保护）', () => {
    for (const name of NAMES) {
      assert.ok(!/\p{Extended_Pictographic}/u.test(icon(name)), `${name} 仍含 emoji`);
    }
  });
});
