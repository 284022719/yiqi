/**
 * 团本 DPS 天梯（排名数据）
 *
 * 专精图标与职业信息统一见 specs.js，此处只保留层级与元数据。
 * 来源: https://www.wowhead.com/cn/guide/classes/tier-lists/dps-rankings-raids
 * 更新: 2025/08/09
 */

const dpsTierList = {
  "title": "法力熔炉：欧米伽团队副本——地心之战第三赛季",
  "source": "Dratnos",
  "lastUpdated": "2025/08/09",
  "sourceUrl": "https://www.wowhead.com/cn/guide/classes/tier-lists/dps-rankings-raids",
  "tiers": {
    "S": {
      "name": "S",
      "description": "",
      "specs": [
        "warlock|恶魔学识",
        "death-knight|冰霜"
      ]
    },
    "A": {
      "name": "A",
      "description": "",
      "specs": [
        "priest|暗影",
        "shaman|元素",
        "evoker|湮灭",
        "mage|冰霜",
        "death-knight|邪恶",
        "warlock|毁灭",
        "mage|奥术",
        "evoker|增辉"
      ]
    },
    "B": {
      "name": "B",
      "description": "",
      "specs": [
        "monk|踏风",
        "hunter|野兽控制",
        "demon-hunter|浩劫",
        "mage|火焰",
        "paladin|惩戒",
        "warrior|狂怒",
        "shaman|增强",
        "hunter|生存",
        "hunter|射击",
        "rogue|奇袭",
        "rogue|敏锐",
        "rogue|狂徒",
        "druid|野性",
        "druid|平衡"
      ]
    },
    "C": {
      "name": "C",
      "description": "",
      "specs": [
        "warrior|武器"
      ]
    },
    "D": {
      "name": "D",
      "description": "",
      "specs": []
    },
    "F": {
      "name": "F",
      "description": "",
      "specs": []
    }
  }
};

export default dpsTierList;
