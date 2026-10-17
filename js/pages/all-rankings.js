/**
 * 排名总览页入口
 *
 * 原先内联在 pages/all-rankings.html 里；外链后页面不含内联脚本，
 * 才能启用严格的 Content-Security-Policy（script-src 'self'）。
 */

import dpsTierList from '../data/dps-tier-list.js';
import healerTierList from '../data/healer-tier-list.js';
import tankTierList from '../data/tank-tier-list.js';
import mplusDpsTierList from '../data/mplus-dps-tier-list.js';
import mplusHealerTierList from '../data/mplus-healer-tier-list.js';
import mplusTankTierList from '../data/mplus-tank-tier-list.js';

import { TierList } from '../components/TierList.js';
import { RankingNav } from '../components/ranking-nav.js';

function init() {
  new RankingNav('ranking-nav-container');

  // 团本
  new TierList('raid-dps-tier-list-container', dpsTierList, 'dps');
  new TierList('raid-healer-tier-list-container', healerTierList, 'healer');
  new TierList('raid-tank-tier-list-container', tankTierList, 'tank');

  // 大秘境
  new TierList('mplus-dps-tier-list-container', mplusDpsTierList, 'dps');
  new TierList('mplus-healer-tier-list-container', mplusHealerTierList, 'healer');
  new TierList('mplus-tank-tier-list-container', mplusTankTierList, 'tank');
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
