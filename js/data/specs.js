/**
 * 专精注册表（唯一数据源）
 *
 * 6 份天梯数据文件此前各自重复声明了 class / spec / icon，
 * 共 70 处引用但只有 39 个唯一专精。这里统一收敛。
 *
 * key 规则: '<职业 slug>|<专精中文名>'
 */

export const SPECS = {
  'warrior|防护': {
    class: '战士',
    spec: '防护',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/54f0768bd97c00a19c73a54f42776847_54f076.jpg'
  },
  'warrior|狂怒': {
    class: '战士',
    spec: '狂怒',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/afa8e89782ebfb64b60473b1f853d941_afa8e8.jpg'
  },
  'warrior|武器': {
    class: '战士',
    spec: '武器',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/8042e893a92416b6db28c1f110aa6e1a_8042e8.jpg'
  },
  'paladin|惩戒': {
    class: '圣骑士',
    spec: '惩戒',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/11cec7f4b5ae974eca164a551d538d71_11cec7.jpg'
  },
  'paladin|防护': {
    class: '圣骑士',
    spec: '防护',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/2adb8940a6fd426f82e59ef86cfa9cd0_2adb89.jpg'
  },
  'paladin|神圣': {
    class: '圣骑士',
    spec: '神圣',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/4464e254ce933c0f255d00bc804f7689_4464e2.jpg'
  },
  'hunter|射击': {
    class: '猎人',
    spec: '射击',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/412d71c51af5ebc79dd968776e7451ac_412d71.jpg'
  },
  'hunter|生存': {
    class: '猎人',
    spec: '生存',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/7f70ef89711ded9049777cdfd5358ef8_7f70ef.jpg'
  },
  'hunter|野兽控制': {
    class: '猎人',
    spec: '野兽控制',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/c7d857d7e0c0c38a2cc908c7c2e261fb_c7d857.jpg'
  },
  'rogue|狂徒': {
    class: '潜行者',
    spec: '狂徒',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/a3bf7dcb57ccb8fa0335c6d9fad96e65_a3bf7d.jpg'
  },
  'rogue|敏锐': {
    class: '潜行者',
    spec: '敏锐',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/4be369057c80dda7cca42c6d5493ec99_4be369.jpg'
  },
  'rogue|奇袭': {
    class: '潜行者',
    spec: '奇袭',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/e8ddea05465a3457484406f7c239108d_e8ddea.jpg'
  },
  'rogue|战斗': {
    class: '潜行者',
    spec: '战斗',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/a3bf7dcb57ccb8fa0335c6d9fad96e65_a3bf7d.jpg'
  },
  'priest|暗影': {
    class: '牧师',
    spec: '暗影',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/e86d4559fb9ee96284288a2f4ed67868_e86d45.jpg'
  },
  'priest|戒律': {
    class: '牧师',
    spec: '戒律',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/9f798b42d0666c11589442707d9ed300_9f798b.jpg'
  },
  'priest|神圣': {
    class: '牧师',
    spec: '神圣',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/7276c129e44efe8bc92cfaa0e82c81e2_7276c1.jpg'
  },
  'warlock|恶魔学识': {
    class: '术士',
    spec: '恶魔学识',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/42f5345e9b5c3cd6edb63c04004aa867_42f534.jpg'
  },
  'warlock|毁灭': {
    class: '术士',
    spec: '毁灭',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/32b6067fcb4c8c38c964b7665776954c_32b606.jpg'
  },
  'mage|奥术': {
    class: '法师',
    spec: '奥术',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/4f8c9a095a547e7da61df6d6e1f1a75a_4f8c9a.jpg'
  },
  'mage|冰霜': {
    class: '法师',
    spec: '冰霜',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/9a58be7bc5eea5d52df7feb66ffb67a6_9a58be.jpg'
  },
  'mage|火焰': {
    class: '法师',
    spec: '火焰',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/1f61b047cb21a7354f2b2b7ce0c3301f_1f61b0.jpg'
  },
  'monk|酒仙': {
    class: '武僧',
    spec: '酒仙',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/99a850159416c0fea5490c4c549e207e_99a850.jpg'
  },
  'monk|踏风': {
    class: '武僧',
    spec: '踏风',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/be57b0a6c08c2f766bd0044b9e9b4990_be57b0.jpg'
  },
  'monk|织雾': {
    class: '武僧',
    spec: '织雾',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/3208b3c8e3a04278fa124e51f86cf875_3208b3.jpg'
  },
  'death-knight|冰霜': {
    class: '死亡骑士',
    spec: '冰霜',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/2b7fa60765598105fe8714cd47b6405e_2b7fa6.jpg'
  },
  'death-knight|鲜血': {
    class: '死亡骑士',
    spec: '鲜血',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/93e14423336ce899f03b6ad329348d51_93e144.jpg'
  },
  'death-knight|邪恶': {
    class: '死亡骑士',
    spec: '邪恶',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/636ddd899db73130b873ec1e07cb2584_636ddd.jpg'
  },
  'druid|恢复': {
    class: '德鲁伊',
    spec: '恢复',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/486ecac9f985afd0f038c245fb763518_486eca.jpg'
  },
  'druid|平衡': {
    class: '德鲁伊',
    spec: '平衡',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/eaf794df951998cc697f59d6ac57ebbe_eaf794.jpg'
  },
  'druid|守护': {
    class: '德鲁伊',
    spec: '守护',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/940397278c923f5696831ec901cd6c55_940397.jpg'
  },
  'druid|野性': {
    class: '德鲁伊',
    spec: '野性',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/7f7356ac953aa62def91e30380b73b30_7f7356.jpg'
  },
  'shaman|恢复': {
    class: '萨满祭司',
    spec: '恢复',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/c465705579a55fdc55de4f284753ddb6_c46570.jpg'
  },
  'shaman|元素': {
    class: '萨满祭司',
    spec: '元素',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/2e4b3919918ba372713e02e59e358fd9_2e4b39.jpg'
  },
  'shaman|增强': {
    class: '萨满祭司',
    spec: '增强',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/6785c9cc1b99763038e72089956b49a2_6785c9.jpg'
  },
  'demon-hunter|复仇': {
    class: '恶魔猎手',
    spec: '复仇',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/c6157abd97efa41fd2ede909018b0775_c6157a.jpg'
  },
  'demon-hunter|浩劫': {
    class: '恶魔猎手',
    spec: '浩劫',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/edb77caa99e888d3ecb32b5dfc25d966_edb77c.jpg'
  },
  'evoker|恩护': {
    class: '唤魔师',
    spec: '恩护',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/0fdbe22a0709fb3a50947a72e3313223_0fdbe2.jpg'
  },
  'evoker|湮灭': {
    class: '唤魔师',
    spec: '湮灭',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/bd47943092a9e8ff57cc2a91461daf97_bd4794.jpg'
  },
  'evoker|增辉': {
    class: '唤魔师',
    spec: '增辉',
    icon: 'https://wow.res.netease.com/xt/manage/20241217/0c55f62f7732d30b2110f44e59d9bec5_0c55f6.jpg'
  }
};

/**
 * 按 id 取专精信息。
 * @param {string} id 形如 'paladin|防护'
 * @returns {{class: string, spec: string, icon: string, name: string}}
 */
export function resolveSpec(id) {
  const spec = SPECS[id];
  if (!spec) {
    throw new Error(`未知专精 id: ${id}`);
  }
  return { ...spec, name: `${spec.spec} ${spec.class}` };
}

/** 由职业名与专精名拼出 id（供数据维护时使用） */
export function getSpecId(classSlugValue, specName) {
  return `${classSlugValue}|${specName}`;
}
