/**
 * 团本治疗天梯（排名数据）
 *
 * 专精图标与职业信息统一见 specs.js，此处只保留层级与元数据。
 * 来源: https://www.wowhead.com/cn/guide/classes/tier-lists/healer-rankings-raids
 * 更新: 2025/07/29
 */

const healerTierList = {
  "title": "法力熔炉：欧米伽团队副本——地心之战第三赛季",
  "source": "korimae",
  "lastUpdated": "2025/07/29",
  "sourceUrl": "https://www.wowhead.com/cn/guide/classes/tier-lists/healer-rankings-raids",
  "tiers": {
    "S": {
      "name": "S",
      "description": "",
      "specs": [
        "priest|神圣",
        "druid|恢复"
      ]
    },
    "A": {
      "name": "A",
      "description": "",
      "specs": [
        "shaman|恢复",
        "paladin|神圣",
        "monk|织雾"
      ]
    },
    "B": {
      "name": "B",
      "description": "",
      "specs": [
        "priest|戒律",
        "evoker|恩护"
      ]
    },
    "C": {
      "name": "C",
      "description": "",
      "specs": []
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

export default healerTierList;
