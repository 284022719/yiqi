/**
 * Mythic+ DPS Tier List Data - 基于Wowhead排名
 * 来源: https://www.wowhead.com/cn/guide/classes/tier-lists/dps-rankings-mythic-plus
 * 更新: 2025/08/03
 */

const mplusDpsTierList = {
  title: "大秘境DPS Rankings - Tier List for The War Within Season 3",
  source: "tettles",
  lastUpdated: "2025/08/03",
  sourceUrl: "https://www.wowhead.com/cn/guide/classes/tier-lists/dps-rankings-mythic-plus",
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
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_metamorphosis.jpg",
          color: "var(--class-warlock)"
        },
        {
          name: "狂怒 战士",
          class: "战士",
          spec: "狂怒",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_warrior_innerrage.jpg",
          color: "var(--class-warrior)"
        },
        {
          name: "冰霜 法师",
          class: "法师",
          spec: "冰霜",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_frost_frostbolt02.jpg",
          color: "var(--class-mage)"
        }
      ]
    },
    "A": {
      name: "A",
      description: "",
      color: "#FF6B6B", // 红色
      specs: [
        {
          name: "毁灭 术士",
          class: "术士",
          spec: "毁灭",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_rainoffire.jpg",
          color: "var(--class-warlock)"
        },
        {
          name: "武器 战士",
          class: "战士",
          spec: "武器",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_warrior_savageblow.jpg",
          color: "var(--class-warrior)"
        },
        {
          name: "奥术 法师",
          class: "法师",
          spec: "奥术",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_holy_magicalsentry.jpg",
          color: "var(--class-mage)"
        },
        {
          name: "射击 猎人",
          class: "猎人",
          spec: "射击",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_hunter_focusedaim.jpg",
          color: "var(--class-hunter)"
        },
        {
          name: "奇袭 潜行者",
          class: "潜行者",
          spec: "奇袭",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_rogue_ambush.jpg",
          color: "var(--class-rogue)"
        }
      ]
    },
    "B": {
      name: "B",
      description: "",
      color: "#4ECDC4", // 青色
      specs: [
        {
          name: "火焰 法师",
          class: "法师",
          spec: "火焰",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_fire_firebolt02.jpg",
          color: "var(--class-mage)"
        },
        {
          name: "野兽控制 猎人",
          class: "猎人",
          spec: "野兽控制",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_hunter_beasttaming.jpg",
          color: "var(--class-hunter)"
        },
        {
          name: "敏锐 潜行者",
          class: "潜行者",
          spec: "敏锐",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_stealth.jpg",
          color: "var(--class-rogue)"
        },
        {
          name: "惩戒 圣骑士",
          class: "圣骑士",
          spec: "惩戒",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_holy_auraoflight.jpg",
          color: "var(--class-paladin)"
        },
        {
          name: "平衡 德鲁伊",
          class: "德鲁伊",
          spec: "平衡",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_nature_starfall.jpg",
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
          name: "生存 猎人",
          class: "猎人",
          spec: "生存",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_hunter_swiftstrike.jpg",
          color: "var(--class-hunter)"
        },
        {
          name: "战斗 潜行者",
          class: "潜行者",
          spec: "战斗",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_rogue_combat.jpg",
          color: "var(--class-rogue)"
        },
        {
          name: "增强 萨满",
          class: "萨满祭司",
          spec: "增强",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_nature_lightning.jpg",
          color: "var(--class-shaman)"
        },
        {
          name: "野性战斗 德鲁伊",
          class: "德鲁伊",
          spec: "野性战斗",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_racial_bearform.jpg",
          color: "var(--class-druid)"
        }
      ]
    },
    "D": {
      name: "D",
      description: "",
      color: "#FFB6C1", // 浅粉色
      specs: [
        {
          name: "元素 萨满",
          class: "萨满祭司",
          spec: "元素",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_nature_lightning.jpg",
          color: "var(--class-shaman)"
        },
        {
          name: "风行者 武僧",
          class: "武僧",
          spec: "风行者",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/monk_stance_windwalker.jpg",
          color: "var(--class-monk)"
        }
      ]
    },
    "F": {
      name: "F",
      description: "",
      color: "#D3D3D3", // 浅灰色
      specs: []
    }
  }
};

export default mplusDpsTierList;

