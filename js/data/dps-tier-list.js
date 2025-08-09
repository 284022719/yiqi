/**
 * DPS Tier List Data - 基于Wowhead排名
 * 来源: https://www.wowhead.com/cn/guide/classes/tier-lists/dps-rankings-raids
 * 更新: 2025/08/09
 */

const dpsTierList = {
  title: "法力熔炉：欧米伽团队副本——地心之战第三赛季",
  source: "Dratnos",
  lastUpdated: "2025/08/09",
  sourceUrl: "https://www.wowhead.com/cn/guide/classes/tier-lists/dps-rankings-raids",
  tiers: {
    "S": {
      name: "S",
      description: "",
      color: "#FFD700", // 金色
      specs: [
        {
          name: "恶魔学识 术士",
          class: "术士",
          spec: "恶魔学识",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/42f5345e9b5c3cd6edb63c04004aa867_42f534.jpg",
          color: "var(--class-warlock)"
        },
        {
          name: "冰霜 死亡骑士",
          class: "死亡骑士",
          spec: "冰霜",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/2b7fa60765598105fe8714cd47b6405e_2b7fa6.jpg",
          color: "var(--class-deathknight)"
        }
      ]
    },
    "A": {
      name: "A",
      description: "",
      color: "#FF6B6B", // 红色
      specs: [
        {
          name: "暗影 牧师",
          class: "牧师",
          spec: "暗影",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/e86d4559fb9ee96284288a2f4ed67868_e86d45.jpg",
          color: "var(--class-priest)"
        },
        {
          name: "元素 萨满",
          class: "萨满祭司",
          spec: "元素",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/2e4b3919918ba372713e02e59e358fd9_2e4b39.jpg",
          color: "var(--class-shaman)"
        },
        {
          name: "湮灭 唤魔师",
          class: "唤魔师",
          spec: "湮灭",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/bd47943092a9e8ff57cc2a91461daf97_bd4794.jpg",
          color: "var(--class-evoker)"
        },
        {
          name: "冰霜 法师",
          class: "法师",
          spec: "冰霜",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/9a58be7bc5eea5d52df7feb66ffb67a6_9a58be.jpg",
          color: "var(--class-mage)"
        },
        {
          name: "邪恶 死亡骑士",
          class: "死亡骑士",
          spec: "邪恶",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/636ddd899db73130b873ec1e07cb2584_636ddd.jpg",
          color: "var(--class-deathknight)"
        },
        {
          name: "毁灭 术士",
          class: "术士",
          spec: "毁灭",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/32b6067fcb4c8c38c964b7665776954c_32b606.jpg",
          color: "var(--class-warlock)"
        },
        {
          name: "奥术 法师",
          class: "法师",
          spec: "奥术",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/4f8c9a095a547e7da61df6d6e1f1a75a_4f8c9a.jpg",
          color: "var(--class-mage)"
        },
        {
          name: "增辉 唤魔师",
          class: "唤魔师",
          spec: "增辉",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/0c55f62f7732d30b2110f44e59d9bec5_0c55f6.jpg",
          color: "var(--class-evoker)"
        }
      ]
    },
    "B": {
      name: "B",
      description: "",
      color: "#4ECDC4", // 青色
      specs: [
        {
          name: "踏风 武僧",
          class: "武僧",
          spec: "踏风",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/be57b0a6c08c2f766bd0044b9e9b4990_be57b0.jpg",
          color: "var(--class-monk)"
        },
        {
          name: "野兽控制 猎人",
          class: "猎人",
          spec: "野兽控制",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/c7d857d7e0c0c38a2cc908c7c2e261fb_c7d857.jpg",
          color: "var(--class-hunter)"
        },
        {
          name: "浩劫 恶魔猎手",
          class: "恶魔猎手",
          spec: "浩劫",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/edb77caa99e888d3ecb32b5dfc25d966_edb77c.jpg",
          color: "var(--class-demonhunter)"
        },
        {
          name: "火焰 法师",
          class: "法师",
          spec: "火焰",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/1f61b047cb21a7354f2b2b7ce0c3301f_1f61b0.jpg",
          color: "var(--class-mage)"
        },
        {
          name: "惩戒 圣骑士",
          class: "圣骑士",
          spec: "惩戒",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/11cec7f4b5ae974eca164a551d538d71_11cec7.jpg",
          color: "var(--class-paladin)"
        },
        {
          name: "狂怒 战士",
          class: "战士",
          spec: "狂怒",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/afa8e89782ebfb64b60473b1f853d941_afa8e8.jpg",
          color: "var(--class-warrior)"
        },
        {
          name: "增强 萨满",
          class: "萨满祭司",
          spec: "增强",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/6785c9cc1b99763038e72089956b49a2_6785c9.jpg",
          color: "var(--class-shaman)"
        },
        {
          name: "生存 猎人",
          class: "猎人",
          spec: "生存",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/7f70ef89711ded9049777cdfd5358ef8_7f70ef.jpg",
          color: "var(--class-hunter)"
        },
        {
          name: "射击 猎人",
          class: "猎人",
          spec: "射击",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/412d71c51af5ebc79dd968776e7451ac_412d71.jpg",
          color: "var(--class-hunter)"
        },
        {
          name: "奇袭 潜行者",
          class: "潜行者",
          spec: "奇袭",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/e8ddea05465a3457484406f7c239108d_e8ddea.jpg",
          color: "var(--class-rogue)"
        },
        {
          name: "敏锐 潜行者",
          class: "潜行者",
          spec: "敏锐",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/4be369057c80dda7cca42c6d5493ec99_4be369.jpg",
          color: "var(--class-rogue)"
        },
        {
          name: "狂徒 潜行者",
          class: "潜行者",
          spec: "狂徒",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/a3bf7dcb57ccb8fa0335c6d9fad96e65_a3bf7d.jpg",
          color: "var(--class-rogue)"
        },
        {
          name: "野性 德鲁伊",
          class: "德鲁伊",
          spec: "野性",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/7f7356ac953aa62def91e30380b73b30_7f7356.jpg",
          color: "var(--class-druid)"
        },
        {
          name: "平衡 德鲁伊",
          class: "德鲁伊",
          spec: "平衡",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/eaf794df951998cc697f59d6ac57ebbe_eaf794.jpg",
          color: "var(--class-druid)"
        }
      ]
    },
    "C": {
      name: "C",
      description: "",
      color: "#A8E6CF", // 浅绿色
      specs: [
        {
          name: "武器 战士",
          class: "战士",
          spec: "武器",
          specIcon: "https://wow.res.netease.com/xt/manage/20241217/8042e893a92416b6db28c1f110aa6e1a_8042e8.jpg",
          color: "var(--class-warrior)"
        }
      ]
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

export default dpsTierList;
