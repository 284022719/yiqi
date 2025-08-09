/**
 * Healer Tier List Data - 基于Wowhead排名
 * 来源: https://www.wowhead.com/cn/guide/classes/tier-lists/healer-rankings-raids
 * 更新: 2025/07/29
 */

const healerTierList = {
  title: "法力熔炉：欧米伽团队副本——地心之战第三赛季",
  source: "korimae",
  lastUpdated: "2025/07/29",
  sourceUrl: "https://www.wowhead.com/cn/guide/classes/tier-lists/healer-rankings-raids",
  tiers: {
    "S": {
      name: "S",
      description: "",
      color: "#FFD700", // 金色
      specs: [
        {
          name: "神圣 牧师",
          class: "牧师",
          spec: "神圣",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/7276c129e44efe8bc92cfaa0e82c81e2_7276c1.jpg",
          color: "var(--class-priest)"
        },
        {
          name: "恢复 德鲁伊",
          class: "德鲁伊",
          spec: "恢复",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/486ecac9f985afd0f038c245fb763518_486eca.jpg",
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
          name: "恢复 萨满",
          class: "萨满祭司",
          spec: "恢复",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/c465705579a55fdc55de4f284753ddb6_c46570.jpg",
          color: "var(--class-shaman)"
        },
        {
          name: "神圣 圣骑士",
          class: "圣骑士",
          spec: "神圣",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/4464e254ce933c0f255d00bc804f7689_4464e2.jpg",
          color: "var(--class-paladin)"
        },
        {
          name: "织雾 武僧",
          class: "武僧",
          spec: "织雾",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/3208b3c8e3a04278fa124e51f86cf875_3208b3.jpg",
          color: "var(--class-monk)"
        }
      ]
    },
    "B": {
      name: "B",
      description: "",
      color: "#4ECDC4", // 青色
      specs: [
        {
          name: "戒律 牧师",
          class: "牧师",
          spec: "戒律",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/9f798b42d0666c11589442707d9ed300_9f798b.jpg",
          color: "var(--class-priest)"
        },
        {
          name: "恩护 唤魔师",
          class: "唤魔师",
          spec: "恩护",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/0fdbe22a0709fb3a50947a72e3313223_0fdbe2.jpg",
          color: "var(--class-evoker)"
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

export default healerTierList;

