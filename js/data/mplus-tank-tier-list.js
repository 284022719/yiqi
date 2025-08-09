/**
 * Mythic+ Tank Tier List Data - 基于Wowhead排名
 * 来源: https://www.wowhead.com/cn/guide/classes/tier-lists/tank-rankings-mythic-plus
 * 更新: 2025/07/29
 */

const mplusTankTierList = {
  title: "大秘境Tank Rankings - Tier List for The War Within Season 3",
  source: "YoDaTV",
  lastUpdated: "2025/07/29",
  sourceUrl: "https://www.wowhead.com/cn/guide/classes/tier-lists/tank-rankings-mythic-plus",
  tiers: {
    "S": {
      name: "S",
      description: "",
      color: "#FFD700", // 金色
      specs: [
        {
          name: "防护 圣骑士",
          class: "圣骑士",
          spec: "防护",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/2adb8940a6fd426f82e59ef86cfa9cd0_2adb89.jpg",
          color: "var(--class-paladin)"
        },
        {
          name: "守护 德鲁伊",
          class: "德鲁伊",
          spec: "守护",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/940397278c923f5696831ec901cd6c55_940397.jpg",
          color: "var(--class-druid)"
        }
      ]
    },
    "A": {
      name: "A",
      description: "",
      color: "#FF6B6B", // 红色
      specs: [
        {
          name: "防护 战士",
          class: "战士",
          spec: "防护",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/54f0768bd97c00a19c73a54f42776847_54f076.jpg",
          color: "var(--class-warrior)"
        },
        {
          name: "鲜血 死亡骑士",
          class: "死亡骑士",
          spec: "鲜血",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/93e14423336ce899f03b6ad329348d51_93e144.jpg",
          color: "var(--class-deathknight)"
        },
        {
          name: "复仇 恶魔猎手",
          class: "恶魔猎手",
          spec: "复仇",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/c6157abd97efa41fd2ede909018b0775_c6157a.jpg",
          color: "var(--class-demonhunter)"
        }
      ]
    },
    "B": {
      name: "B",
      description: "",
      color: "#4ECDC4", // 青色
      specs: [
        {
          name: "酒仙 武僧",
          class: "武僧",
          spec: "酒仙",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/99a850159416c0fea5490c4c549e207e_99a850.jpg",
          color: "var(--class-monk)"
        }
      ]
    },
    "C": {
      name: "C",
      description: "",
      color: "#A8E6CF", // 浅绿色
      specs: []
    },
    "D": {
      name: "D",
      description: "",
      color: "#FFB6C1", // 浅粉色
      specs: []
    },
    "F": {
      name: "F",
      description: "",
      color: "#D3D3D3", // 浅灰色
      specs: []
    }
  }
};

export default mplusTankTierList;

