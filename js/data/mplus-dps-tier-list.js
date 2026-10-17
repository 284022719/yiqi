/**
 * 大秘境 DPS 天梯（排名数据）
 *
 * 专精图标与职业信息统一见 specs.js，此处只保留层级与元数据。
 * 来源: https://www.wowhead.com/cn/guide/classes/tier-lists/dps-rankings-mythic-plus
 * 更新: 2025/08/03
 */

const mplusDpsTierList = {
  "title": "大秘境DPS Rankings - Tier List for The War Within Season 3",
  "source": "tettles",
  "lastUpdated": "2025/08/03",
  "sourceUrl": "https://www.wowhead.com/cn/guide/classes/tier-lists/dps-rankings-mythic-plus",
  "tiers": {
    "S": {
      "name": "S",
      "description": "",
      "specs": [
        "warlock|恶魔学识",
        "warrior|狂怒",
        "mage|冰霜"
      ]
    },
    "A": {
      "name": "A",
      "description": "",
      "specs": [
        "warlock|毁灭",
        "warrior|武器",
        "mage|奥术",
        "hunter|射击",
        "rogue|奇袭"
      ]
    },
    "B": {
      "name": "B",
      "description": "",
      "specs": [
        "mage|火焰",
        "hunter|野兽控制",
        "rogue|敏锐",
        "paladin|惩戒",
        "druid|平衡"
      ]
    },
    "C": {
      "name": "C",
      "description": "",
      "specs": [
        "hunter|生存",
        "rogue|战斗",
        "shaman|增强",
        "druid|野性"
      ]
    },
    "D": {
      "name": "D",
      "description": "",
      "specs": [
        "shaman|元素",
        "monk|踏风"
      ]
    },
    "F": {
      "name": "F",
      "description": "",
      "specs": []
    }
  }
};

export default mplusDpsTierList;
