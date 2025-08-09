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
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_paladin_shieldofthetemplar.jpg",
          color: "var(--class-paladin)"
        },
        {
          name: "守护 德鲁伊",
          class: "德鲁伊",
          spec: "守护",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_racial_bearform.jpg",
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
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_warrior_defensivestance.jpg",
          color: "var(--class-warrior)"
        },
        {
          name: "鲜血 死亡骑士",
          class: "死亡骑士",
          spec: "鲜血",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/spell_deathknight_bloodpresence.jpg",
          color: "var(--class-deathknight)"
        },
        {
          name: "复仇 恶魔猎手",
          class: "恶魔猎手",
          spec: "复仇",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/ability_demonhunter_spectank.jpg",
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
          name: "酿酒 武僧",
          class: "武僧",
          spec: "酿酒",
          specIcon: "https://wow.zamimg.com/images/wow/icons/large/monk_stance_drunkenox.jpg",
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

