/**
 * 数据层测试：职业表、专精注册表、6 份天梯数据的一致性。
 *
 * 这里最重要的一条是「天梯里的每个专精 id 都能解析」——
 * 它是之前 70 处图标引用收敛为注册表后最容易出错的地方。
 */
import { test, describe } from 'node:test';
import assert from 'node:assert/strict';

import wowClasses, { getClassInfo, getClassIcon } from '../../js/data/wow-classes.js';
import { SPECS, resolveSpec } from '../../js/data/specs.js';

import dpsTierList from '../../js/data/dps-tier-list.js';
import healerTierList from '../../js/data/healer-tier-list.js';
import tankTierList from '../../js/data/tank-tier-list.js';
import mplusDpsTierList from '../../js/data/mplus-dps-tier-list.js';
import mplusHealerTierList from '../../js/data/mplus-healer-tier-list.js';
import mplusTankTierList from '../../js/data/mplus-tank-tier-list.js';

const TIER_LISTS = {
  'dps-tier-list': dpsTierList,
  'healer-tier-list': healerTierList,
  'tank-tier-list': tankTierList,
  'mplus-dps-tier-list': mplusDpsTierList,
  'mplus-healer-tier-list': mplusHealerTierList,
  'mplus-tank-tier-list': mplusTankTierList
};

const TIER_ORDER = ['S', 'A', 'B', 'C', 'D', 'F'];

describe('wow-classes', () => {
  test('13 个职业，id/slug/name 唯一', () => {
    assert.equal(wowClasses.length, 13);
    assert.equal(new Set(wowClasses.map((c) => c.id)).size, 13);
    assert.equal(new Set(wowClasses.map((c) => c.slug)).size, 13);
    assert.equal(new Set(wowClasses.map((c) => c.name)).size, 13);
  });

  test('按中文名、slug、数字 id 都能查到同一职业', () => {
    const byName = getClassInfo('圣骑士');
    const bySlug = getClassInfo('paladin');
    const byId = getClassInfo(2);
    assert.equal(byName, bySlug);
    assert.equal(byName, byId);
  });

  test('未知职业返回 undefined', () => {
    assert.equal(getClassInfo('不存在的职业'), undefined);
  });

  test('职业颜色走 CSS 变量而不是硬编码 hex', () => {
    for (const cls of wowClasses) {
      assert.match(cls.color, /^var\(--class-/, `${cls.name} 的颜色应为 CSS 变量`);
    }
  });

  test('getClassIcon 返回图标地址', () => {
    assert.match(getClassIcon('战士'), /^https?:\/\//);
    assert.equal(getClassIcon('不存在的职业'), '');
  });
});

describe('specs 注册表', () => {
  test('条目数为 39 且 key 形如 className|专精名', () => {
    const keys = Object.keys(SPECS);
    assert.equal(keys.length, 39);
    for (const key of keys) {
      assert.match(key, /^[a-z-]+\|.+$/, `key 格式异常: ${key}`);
    }
  });

  test('resolveSpec 拼出显示名', () => {
    const spec = resolveSpec('paladin|防护');
    assert.equal(spec.class, '圣骑士');
    assert.equal(spec.spec, '防护');
    assert.equal(spec.name, '防护 圣骑士');
    assert.match(spec.icon, /^https?:\/\//);
  });

  test('未知 id 抛出明确错误', () => {
    assert.throws(() => resolveSpec('paladin|不存在'), /未知专精 id/);
  });

  test('每个专精都能在 wow-classes 里找到对应职业', () => {
    for (const [key, spec] of Object.entries(SPECS)) {
      assert.ok(getClassInfo(spec.class), `${key} 的职业「${spec.class}」不在职业表中`);
    }
  });
});

describe('天梯数据', () => {
  for (const [name, data] of Object.entries(TIER_LISTS)) {
    test(`${name}: 元信息完整`, () => {
      assert.ok(data.title && data.source && data.lastUpdated);
      assert.match(data.sourceUrl, /^https?:\/\//);
    });

    test(`${name}: 六个层级齐全`, () => {
      assert.deepEqual(Object.keys(data.tiers), TIER_ORDER);
    });

    test(`${name}: 所有专精 id 都能解析`, () => {
      for (const [tierKey, tier] of Object.entries(data.tiers)) {
        assert.ok(Array.isArray(tier.specs), `${tierKey} 的 specs 不是数组`);
        for (const id of tier.specs) {
          assert.doesNotThrow(() => resolveSpec(id), `${name} [${tierKey}] 无法解析 ${id}`);
        }
      }
    });

    test(`${name}: 同一层级内无重复专精`, () => {
      for (const [tierKey, tier] of Object.entries(data.tiers)) {
        assert.equal(new Set(tier.specs).size, tier.specs.length, `${tierKey} 存在重复`);
      }
    });
  }
});
