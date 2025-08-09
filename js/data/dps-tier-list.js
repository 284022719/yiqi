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
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_metamorphosis.jpg",
          color: "var(--class-warlock)"
        },
        {
          name: "冰霜 死亡骑士",
          class: "死亡骑士",
          spec: "冰霜",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_deathknight_frozenruneweapon.jpg",
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
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_shadowwordpain.jpg",
          color: "var(--class-priest)"
        },
        {
          name: "元素 萨满",
          class: "萨满祭司",
          spec: "元素",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_nature_lightning.jpg",
          color: "var(--class-shaman)"
        },
        {
          name: "湮灭 唤魔师",
          class: "唤魔师",
          spec: "湮灭",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_evoker_disintegrate.jpg",
          color: "var(--class-evoker)"
        },
        {
          name: "冰霜 法师",
          class: "法师",
          spec: "冰霜",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_frost_frostbolt02.jpg",
          color: "var(--class-mage)"
        },
        {
          name: "邪恶 死亡骑士",
          class: "死亡骑士",
          spec: "邪恶",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_deathknight_plaguestrike.jpg",
          color: "var(--class-deathknight)"
        },
        {
          name: "毁灭 术士",
          class: "术士",
          spec: "毁灭",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_shadow_rainoffire.jpg",
          color: "var(--class-warlock)"
        },
        {
          name: "奥术 法师",
          class: "法师",
          spec: "奥术",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_holy_magicalsentry.jpg",
          color: "var(--class-mage)"
        },
        {
          name: "增辉 唤魔师",
          class: "唤魔师",
          spec: "增辉",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_evoker_prescience.jpg",
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
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/monk_stance_drunkenox.jpg",
          color: "var(--class-monk)"
        },
        {
          name: "野兽控制 猎人",
          class: "猎人",
          spec: "野兽控制",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_hunter_bestialdiscipline.jpg",
          color: "var(--class-hunter)"
        },
        {
          name: "浩劫 恶魔猎手",
          class: "恶魔猎手",
          spec: "浩劫",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_demonhunter_specdps.jpg",
          color: "var(--class-demonhunter)"
        },
        {
          name: "火焰 法师",
          class: "法师",
          spec: "火焰",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_fire_firebolt02.jpg",
          color: "var(--class-mage)"
        },
        {
          name: "惩戒 圣骑士",
          class: "圣骑士",
          spec: "惩戒",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_holy_auraoflight.jpg",
          color: "var(--class-paladin)"
        },
        {
          name: "狂怒 战士",
          class: "战士",
          spec: "狂怒",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_warrior_innerrage.jpg",
          color: "var(--class-warrior)"
        },
        {
          name: "增强 萨满",
          class: "萨满祭司",
          spec: "增强",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_shaman_improvedstormstrike.jpg",
          color: "var(--class-shaman)"
        },
        {
          name: "生存 猎人",
          class: "猎人",
          spec: "生存",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_hunter_swiftstrike.jpg",
          color: "var(--class-hunter)"
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
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_rogue_deadlybrew.jpg",
          color: "var(--class-rogue)"
        },
        {
          name: "敏锐 潜行者",
          class: "潜行者",
          spec: "敏锐",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_stealth.jpg",
          color: "var(--class-rogue)"
        },
        {
          name: "狂徒 潜行者",
          class: "潜行者",
          spec: "狂徒",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_rogue_waylay.jpg",
          color: "var(--class-rogue)"
        },
        {
          name: "野性 德鲁伊",
          class: "德鲁伊",
          spec: "野性",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_druid_catform.jpg",
          color: "var(--class-druid)"
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
          name: "武器 战士",
          class: "战士",
          spec: "武器",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_warrior_savageblow.jpg",
          color: "var(--class-warrior)"
        }
      ]
    },
    "D": {
      name: "D Tier (较弱)",
      description: "较弱性能等级",
      color: "#FFB6C1", // 浅粉色
      specs: []
    },
    "F": {
      name: "F Tier (最弱)",
      description: "最弱性能等级",
      color: "#D3D3D3", // 浅灰色
      specs: []
    }
  }
};

export default dpsTierList;
