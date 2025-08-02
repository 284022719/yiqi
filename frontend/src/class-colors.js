/**
 * 魔兽世界职业颜色配置
 * 基于官方classcolor文件的标准颜色
 */

const CLASS_COLORS = {
    // 中文职业名称 -> 十六进制颜色值
    '战士': '#C69B6D',
    '圣骑士': '#F48CBA',
    '猎人': '#AAD372',
    '潜行者': '#FFF468',
    '牧师': '#FFFFFF',
    '死亡骑士': '#C41E3A',
    '萨满祭司': '#0070DD',
    '法师': '#3FC7EB',
    '术士': '#8788EE',
    '武僧': '#00FF98',
    '德鲁伊': '#FF7C0A',
    '恶魔猎手': '#A330C9',
    '唤魔师': '#33937F',
    
    // 英文职业名称 -> 十六进制颜色值
    'Warrior': '#C69B6D',
    'Paladin': '#F48CBA',
    'Hunter': '#AAD372',
    'Rogue': '#FFF468',
    'Priest': '#FFFFFF',
    'Death Knight': '#C41E3A',
    'Shaman': '#0070DD',
    'Mage': '#3FC7EB',
    'Warlock': '#8788EE',
    'Monk': '#00FF98',
    'Druid': '#FF7C0A',
    'Demon Hunter': '#A330C9',
    'Evoker': '#33937F'
};

/**
 * 获取职业颜色
 * @param {string} className - 职业名称（中文或英文）
 * @returns {string} 十六进制颜色值，如果未找到则返回白色
 */
function getClassColor(className) {
    return CLASS_COLORS[className] || '#FFFFFF';
}

/**
 * 获取所有职业颜色
 * @returns {Object} 职业颜色对象
 */
function getAllClassColors() {
    return CLASS_COLORS;
}

// ES6模块导出
export { CLASS_COLORS, getClassColor, getAllClassColors };

// 为了向后兼容，也添加到全局对象
if (typeof window !== 'undefined') {
    window.CLASS_COLORS = CLASS_COLORS;
    window.getClassColor = getClassColor;
    window.getAllClassColors = getAllClassColors;
} 