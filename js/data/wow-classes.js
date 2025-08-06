/**
 * 魔兽世界职业数据 - 官方标准
 * 包含职业颜色、图标和相关信息
 */

const wowClasses = [
  {
    id: 1,
    name: "战士",
    slug: "warrior",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon1_3c105fbd.png",
    color: "var(--class-warrior)",
    textColor: "var(--class-text-light)"
  },
  {
    id: 2,
    name: "圣骑士",
    slug: "paladin",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon7_01967e0b.png",
    color: "var(--class-paladin)",
    textColor: "var(--class-text-dark)"
  },
  {
    id: 3,
    name: "猎人",
    slug: "hunter",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon2_fd85fd71.png",
    color: "var(--class-hunter)",
    textColor: "var(--class-text-dark)"
  },
  {
    id: 4,
    name: "潜行者",
    slug: "rogue",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon4_42d9e458.png",
    color: "var(--class-rogue)",
    textColor: "var(--class-text-dark)"
  },
  {
    id: 5,
    name: "牧师",
    slug: "priest",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon5_476eea68.png",
    color: "var(--class-priest)",
    textColor: "var(--class-text-dark)",
    borderColor: "#CCC" /* 白色背景需要边框 */
  },
  {
    id: 6,
    name: "术士",
    slug: "warlock",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon6_41af0807.png",
    color: "var(--class-warlock)",
    textColor: "var(--class-text-light)"
  },
  {
    id: 7,
    name: "法师",
    slug: "mage",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon3_60f4a6ff.png",
    color: "var(--class-mage)",
    textColor: "var(--class-text-dark)"
  },
  {
    id: 8,
    name: "武僧",
    slug: "monk",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon8_5c918d2b.png",
    color: "var(--class-monk)",
    textColor: "var(--class-text-dark)"
  },
  {
    id: 9,
    name: "死亡骑士",
    slug: "death-knight",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon10_8e08c037.png",
    color: "var(--class-deathknight)",
    textColor: "var(--class-text-light)"
  },
  {
    id: 10,
    name: "德鲁伊",
    slug: "druid",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon11_4e8f6962.jpg",
    color: "var(--class-druid)",
    textColor: "var(--class-text-light)"
  },
  {
    id: 11,
    name: "萨满祭司",
    slug: "shaman",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon8_6f9b9104.jpg",
    color: "var(--class-shaman)",
    textColor: "var(--class-text-light)"
  },
  {
    id: 12,
    name: "恶魔猎手",
    slug: "demon-hunter",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon12_62cd5877.jpg",
    color: "var(--class-demonhunter)",
    textColor: "var(--class-text-light)"
  },
  {
    id: 13,
    name: "唤魔师",
    slug: "evoker",
    icon: "https://wow.res.netease.com/pc/zt/20240820173221/assets/career-icon7_29a4039f.png",
    color: "var(--class-evoker)",
    textColor: "var(--class-text-light)"
  }
];

export default wowClasses;

/**
 * 获取职业信息
 */
export function getClassInfo(className) {
  if (typeof className === 'number') {
    return wowClasses.find(c => c.id === className);
  } else if (typeof className === 'string') {
    return wowClasses.find(c => c.slug === className || c.name === className);
  }
  return className;
}

/**
 * 获取职业颜色
 */
export function getClassColor(className) {
  const classInfo = getClassInfo(className);
  return classInfo ? classInfo.color : 'var(--color-text)';
}

/**
 * 获取职业的实际颜色值（十六进制）
 */
export function getClassColorHex(className) {
  const colorMap = {
    '战士': '#C69B6D',
    '圣骑士': '#F48CBA',
    '猎人': '#AAD372',
    '潜行者': '#FFF468',
    '牧师': '#FFFFFF',
    '术士': '#8788EE',
    '法师': '#3FC7EB',
    '武僧': '#00FF98',
    '死亡骑士': '#C41E3A',
    '德鲁伊': '#FF7C0A',
    '萨满祭司': '#0070DD',
    '恶魔猎手': '#A330C9',
    '唤魔师': '#33937F'
  };
  
  return colorMap[className] || '#FF6B35';
}

/**
 * 获取职业图标
 */
export function getClassIcon(className) {
  const classInfo = getClassInfo(className);
  return classInfo ? classInfo.icon : '';
}

/**
 * 获取职业表情符号图标
 */
export function getClassEmoji(className) {
  const emojiMap = {
    'warrior': '⚔️',
    'paladin': '🛡️',
    'hunter': '🏹',
    'rogue': '🗡️',
    'priest': '✝️',
    'death-knight': '💀',
    'shaman': '⚡',
    'mage': '🔮',
    'warlock': '🔥',
    'monk': '🥋',
    'druid': '🌿',
    'demon-hunter': '👁️',
    'evoker': '🐉'
  };
  
  const classInfo = getClassInfo(className);
  return classInfo ? emojiMap[classInfo.slug] || '⚔️' : '⚔️';
}

/**
 * 获取职业的文本颜色（根据背景色自动选择）
 */
export function getTextColor(backgroundColor) {
  const color = backgroundColor.replace('var(', '').replace(')', '');
  const hex = getComputedStyle(document.documentElement)
    .getPropertyValue(color).trim();
  
  // 计算亮度 (0-255)
  const r = parseInt(hex.substr(1, 2), 16);
  const g = parseInt(hex.substr(3, 2), 16);
  const b = parseInt(hex.substr(5, 2), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  
  return brightness > 125 ? "var(--class-text-dark)" : "var(--class-text-light)";
}

/**
 * 获取对比色（用于文本可读性）
 */
export function getContrastColor(hexColor) {
  const r = parseInt(hexColor.substr(1, 2), 16);
  const g = parseInt(hexColor.substr(3, 2), 16);
  const b = parseInt(hexColor.substr(5, 2), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 125 ? '#000' : '#FFF';
} 