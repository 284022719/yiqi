/**
 * Chart.js：渲染函数只写 container.innerHTML，因此可以用假容器直接断言输出。
 */
import { test, describe } from 'node:test';
import assert from 'node:assert/strict';

import { renderBarChart, renderPieChart } from '../../js/components/Chart.js';

/** 最小假容器：只提供 innerHTML 读写 */
function fakeContainer() {
  return { innerHTML: '' };
}

describe('renderBarChart', () => {
  test('空数据渲染空状态', () => {
    const el = fakeContainer();
    renderBarChart(el, [], { emptyText: '暂无职业数据' });
    assert.ok(el.innerHTML.includes('chart-empty'));
    assert.ok(el.innerHTML.includes('暂无职业数据'));
  });

  test('全 0 数据渲染空状态（避免除零）', () => {
    const el = fakeContainer();
    renderBarChart(el, [{ name: '战士', value: 0 }], {});
    assert.ok(el.innerHTML.includes('chart-empty'));
  });

  test('容器为 null 时静默返回', () => {
    assert.doesNotThrow(() => renderBarChart(null, [{ name: 'a', value: 1 }], {}));
  });

  test('按最大值计算百分比宽度', () => {
    const el = fakeContainer();
    renderBarChart(el, [{ name: '甲', value: 100 }, { name: '乙', value: 25 }], {});

    assert.ok(el.innerHTML.includes('width: 100.0%'));
    assert.ok(el.innerHTML.includes('width: 25.0%'));
    assert.equal((el.innerHTML.match(/class="chart-bar"/g) || []).length, 2);
  });

  test('颜色由 colorOf 决定，并用于描边与渐变', () => {
    const el = fakeContainer();
    renderBarChart(el, [{ name: '圣骑士', value: 5 }], { colorOf: () => '#F48CBA' });
    assert.ok(el.innerHTML.includes('#F48CBA'));
    assert.ok(el.innerHTML.includes('#F48CBA80'));
  });

  test('名称与文本被转义', () => {
    const el = fakeContainer();
    renderBarChart(el, [{ name: '<img src=x onerror=1>', value: 1 }], {});
    assert.ok(!el.innerHTML.includes('<img src=x'));
    assert.ok(el.innerHTML.includes('&lt;img'));
  });

  test('value 为字符串数字时也能计算', () => {
    const el = fakeContainer();
    renderBarChart(el, [{ name: '甲', value: '50' }], {});
    assert.ok(el.innerHTML.includes('width: 100.0%'));
  });
});

describe('renderPieChart', () => {
  const colorOf = (name) => (name === 'Horde' ? '#C41F3B' : '#0070DE');

  test('缺少 colorOf 时渲染空状态', () => {
    const el = fakeContainer();
    renderPieChart(el, [{ name: 'Horde', value: 1 }], {});
    assert.ok(el.innerHTML.includes('chart-empty'));
  });

  test('中心显示总数，图例显示占比', () => {
    const el = fakeContainer();
    renderPieChart(el, [{ name: 'Horde', value: 860 }, { name: 'Alliance', value: 105 }], { colorOf });

    assert.ok(el.innerHTML.includes('>965<'), '中心应显示总数 965');
    assert.ok(el.innerHTML.includes('89.1%'));
    assert.ok(el.innerHTML.includes('10.9%'));
    assert.equal((el.innerHTML.match(/<li>/g) || []).length, 2);
  });

  test('conic-gradient 角度累计到 360 度', () => {
    const el = fakeContainer();
    renderPieChart(el, [{ name: 'Horde', value: 50 }, { name: 'Alliance', value: 50 }], { colorOf });
    assert.ok(el.innerHTML.includes('0deg 180deg'));
    assert.ok(el.innerHTML.includes('180deg 360deg'));
  });

  test('labelOf 可替换显示名（如把 Horde 显示成部落）', () => {
    const el = fakeContainer();
    renderPieChart(el, [{ name: 'Horde', value: 1 }], {
      colorOf,
      labelOf: (item) => (item.name === 'Horde' ? '部落' : '联盟')
    });
    assert.ok(el.innerHTML.includes('部落'));
  });

  test('全 0 数据渲染空状态', () => {
    const el = fakeContainer();
    renderPieChart(el, [{ name: 'Horde', value: 0 }], { colorOf });
    assert.ok(el.innerHTML.includes('chart-empty'));
  });
});
