import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  BookOpen, 
  Users, 
  Clock, 
  Target, 
  Shield, 
  Sword,
  Heart,
  Zap,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Info
} from 'lucide-react'

interface Boss {
  id: number
  name: string
  description: string
  difficulty: 'easy' | 'medium' | 'hard'
  health: string
  mechanics: string[]
  strategy: string
  tips: string[]
  loot: string[]
}

interface Raid {
  id: string
  name: string
  description: string
  bosses: Boss[]
  requirements: {
    level: number
    itemLevel: number
    players: number
  }
  rewards: string[]
}

const raids: Raid[] = [
  {
    id: 'h6',
    name: 'H6副本攻略',
    description: '挑战性十足的6人副本，需要团队配合和战术执行',
    requirements: {
      level: 70,
      itemLevel: 400,
      players: 6
    },
    rewards: [
      '史诗装备',
      '稀有坐骑',
      '成就点数',
      '公会声望'
    ],
    bosses: [
      {
        id: 1,
        name: '暗影领主',
        description: '掌控暗影力量的强大领主，能够召唤暗影生物协助战斗',
        difficulty: 'medium',
        health: '2,500,000',
        mechanics: [
          '暗影箭雨：对随机目标造成持续伤害',
          '暗影分身：召唤具有本体50%血量的分身',
          '暗影护盾：获得减伤效果，需要特定技能破除',
          '暗影爆发：在场地中心释放大范围AOE伤害'
        ],
        strategy: '团队需要分散站位避免暗影箭雨集中伤害，优先击杀暗影分身，在暗影护盾阶段集中火力破除护盾，暗影爆发时远离中心区域。',
        tips: [
          '治疗职业需要密切关注暗影箭雨的目标',
          'DPS职业优先击杀暗影分身',
          '坦克需要及时打断暗影护盾施法',
          '所有成员在暗影爆发前3秒开始撤离'
        ],
        loot: [
          '暗影之刃（武器）',
          '暗影护符（饰品）',
          '暗影长袍（布甲）'
        ]
      },
      {
        id: 2,
        name: '火焰巨兽',
        description: '来自熔岩深处的巨大生物，浑身燃烧着不灭的火焰',
        difficulty: 'hard',
        health: '3,800,000',
        mechanics: [
          '火焰吐息：对前方锥形区域造成巨额伤害',
          '熔岩喷发：在随机位置召唤熔岩池',
          '火焰护甲：增加防御力，但受到冰霜伤害时易伤',
          '烈焰风暴：全场持续火焰伤害，需要冰霜技能降温'
        ],
        strategy: '坦克需要背对团队承受火焰吐息，团队需要及时躲避熔岩池，在火焰护甲阶段使用冰霜技能造成易伤，烈焰风暴时持续使用冰霜技能降温。',
        tips: [
          '坦克必须背对团队，避免火焰吐息波及',
          '所有成员远离熔岩池，持续移动',
          '冰霜法师在火焰护甲阶段全力输出',
          '治疗职业在烈焰风暴时优先治疗'
        ],
        loot: [
          '烈焰之剑（武器）',
          '火焰之心（饰品）',
          '熔岩护甲（板甲）'
        ]
      },
      {
        id: 3,
        name: '时空守护者',
        description: '守护时空裂隙的神秘存在，能够操控时间和空间',
        difficulty: 'hard',
        health: '5,200,000',
        mechanics: [
          '时间减速：降低所有玩家的攻击和移动速度',
          '空间传送：随机传送玩家到不同位置',
          '时空裂隙：在场地中开启传送门，需要进入特定门',
          '时间回溯：重置BOSS血量到上一个阶段'
        ],
        strategy: '团队需要适应时间减速效果，被传送后快速归位，正确识别并进入时空裂隙，在时间回溯前尽可能造成最大伤害。',
        tips: [
          '使用加速技能抵消时间减速效果',
          '被传送后立即使用位移技能归位',
          '观察时空裂隙的颜色判断正确入口',
          '在时间回溯前保留爆发技能'
        ],
        loot: [
          '时空之杖（武器）',
          '时间沙漏（饰品）',
          '虚空长袍（布甲）'
        ]
      }
    ]
  },
  {
    id: 'h7',
    name: 'H7副本攻略',
    description: '最新推出的7人副本，难度极高，需要完美的团队配合',
    requirements: {
      level: 70,
      itemLevel: 420,
      players: 7
    },
    rewards: [
      '传说装备',
      '独特坐骑',
      '稀有称号',
      '公会荣誉'
    ],
    bosses: [
      {
        id: 1,
        name: '虚空女王',
        description: '来自虚空维度的强大存在，能够操控虚空能量',
        difficulty: 'hard',
        health: '4,500,000',
        mechanics: [
          '虚空箭：对目标造成虚空伤害并叠加易伤',
          '虚空传送：在场地中开启多个传送门',
          '虚空护盾：免疫所有伤害，需要虚空能量破除',
          '虚空风暴：全场持续虚空伤害，需要进入传送门躲避'
        ],
        strategy: '团队需要分散站位避免虚空箭集中，正确使用虚空传送门躲避虚空风暴，在虚空护盾阶段收集虚空能量破除护盾。',
        tips: [
          '被虚空箭命中后立即使用净化技能',
          '观察传送门的光效判断安全门',
          '虚空护盾阶段优先收集虚空能量',
          '治疗职业在虚空风暴时全力治疗'
        ],
        loot: [
          '虚空之刃（武器）',
          '虚空宝石（饰品）',
          '虚空护甲（皮甲）'
        ]
      },
      {
        id: 2,
        name: '混沌领主',
        description: '混沌力量的化身，能够随机释放各种元素技能',
        difficulty: 'hard',
        health: '6,800,000',
        mechanics: [
          '元素轮转：随机切换火、冰、雷、毒四种元素',
          '混沌爆发：释放当前元素的大范围技能',
          '元素护盾：获得当前元素的减伤效果',
          '混沌召唤：召唤对应元素的元素生物'
        ],
        strategy: '团队需要根据元素轮转调整战术，使用相克元素技能造成额外伤害，在混沌爆发时使用对应元素抗性技能，优先击杀混沌召唤的元素生物。',
        tips: [
          '观察BOSS身上的元素光环判断当前元素',
          '火元素时使用冰霜技能，冰元素时使用火焰技能',
          '雷元素时使用大地技能，毒元素时使用净化技能',
          '混沌爆发时使用对应元素抗性装备'
        ],
        loot: [
          '混沌之剑（武器）',
          '元素之心（饰品）',
          '混沌护甲（板甲）'
        ]
      },
      {
        id: 3,
        name: '永恒守护者',
        description: '守护永恒之力的终极BOSS，拥有多种致命技能',
        difficulty: 'hard',
        health: '8,500,000',
        mechanics: [
          '永恒之箭：对目标造成持续伤害，无法驱散',
          '时间静止：暂停所有玩家的行动',
          '空间撕裂：在场地中制造危险区域',
          '永恒护盾：获得无敌效果，需要特定条件破除',
          '终极审判：对全场造成致命伤害，需要完美配合'
        ],
        strategy: '团队需要承受永恒之箭的持续伤害，在时间静止时保持冷静，及时躲避空间撕裂，在永恒护盾阶段完成特定任务，终极审判时需要所有成员同时使用防护技能。',
        tips: [
          '治疗职业需要持续治疗永恒之箭的目标',
          '时间静止时保持冷静，不要慌乱',
          '空间撕裂时立即远离危险区域',
          '永恒护盾阶段需要团队协作完成任务',
          '终极审判前确保所有成员都有防护技能'
        ],
        loot: [
          '永恒之杖（武器）',
          '永恒之心（饰品）',
          '永恒护甲（布甲）',
          '永恒坐骑（坐骑）'
        ]
      }
    ]
  }
]

export default function GuidePage() {
  const [selectedRaid, setSelectedRaid] = useState<string>('h6')
  const [selectedBoss, setSelectedBoss] = useState<number | null>(null)

  const currentRaid = raids.find(raid => raid.id === selectedRaid)

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900'
      case 'medium': return 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900'
      case 'hard': return 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900'
      default: return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900'
    }
  }

  const getDifficultyIcon = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return <CheckCircle className="h-4 w-4" />
      case 'medium': return <AlertTriangle className="h-4 w-4" />
      case 'hard': return <XCircle className="h-4 w-4" />
      default: return <Info className="h-4 w-4" />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                副本攻略
              </h1>
              <p className="mt-2 text-gray-600 dark:text-gray-300">
                详细的副本攻略和BOSS机制说明
              </p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
              <BookOpen className="h-5 w-5" />
              <span>持续更新</span>
            </div>
          </div>
        </div>

        {/* Raid Selection */}
        <div className="mb-8">
          <div className="flex space-x-4">
            {raids.map((raid) => (
              <button
                key={raid.id}
                onClick={() => {
                  setSelectedRaid(raid.id)
                  setSelectedBoss(null)
                }}
                className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                  selectedRaid === raid.id
                    ? 'bg-primary-600 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-600'
                }`}
              >
                {raid.name}
              </button>
            ))}
          </div>
        </div>

        {currentRaid && (
          <div className="space-y-8">
            {/* Raid Overview */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6"
            >
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                {currentRaid.name}
              </h2>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                {currentRaid.description}
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="flex items-center space-x-3">
                  <Users className="h-6 w-6 text-blue-500" />
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">所需人数</p>
                    <p className="font-semibold text-gray-900 dark:text-white">{currentRaid.requirements.players}人</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Target className="h-6 w-6 text-green-500" />
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">等级要求</p>
                    <p className="font-semibold text-gray-900 dark:text-white">{currentRaid.requirements.level}级</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Shield className="h-6 w-6 text-purple-500" />
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">装等要求</p>
                    <p className="font-semibold text-gray-900 dark:text-white">{currentRaid.requirements.itemLevel}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Clock className="h-6 w-6 text-yellow-500" />
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">预计时间</p>
                    <p className="font-semibold text-gray-900 dark:text-white">45-90分钟</p>
                  </div>
                </div>
              </div>

              <div className="mt-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">副本奖励</h3>
                <div className="flex flex-wrap gap-2">
                  {currentRaid.rewards.map((reward, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 rounded-full text-sm"
                    >
                      {reward}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>

            {/* Boss List */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {currentRaid.bosses.map((boss, index) => (
                <motion.div
                  key={boss.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => setSelectedBoss(selectedBoss === boss.id ? null : boss.id)}
                >
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                          {boss.name}
                        </h3>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">
                          {boss.description}
                        </p>
                      </div>
                      <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(boss.difficulty)}`}>
                        {getDifficultyIcon(boss.difficulty)}
                        <span className="capitalize">
                          {boss.difficulty === 'easy' ? '简单' : boss.difficulty === 'medium' ? '中等' : '困难'}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4">
                      <div className="flex items-center space-x-1">
                        <Heart className="h-4 w-4" />
                        <span>血量: {boss.health}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Sword className="h-4 w-4" />
                        <span>机制: {boss.mechanics.length}个</span>
                      </div>
                    </div>

                    {/* Expanded Content */}
                    {selectedBoss === boss.id && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="space-y-4 pt-4 border-t border-gray-200 dark:border-gray-600"
                      >
                        <div>
                          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">主要机制</h4>
                          <ul className="space-y-1">
                            {boss.mechanics.map((mechanic, idx) => (
                              <li key={idx} className="text-sm text-gray-600 dark:text-gray-400 flex items-start space-x-2">
                                <span className="text-primary-600 mt-1">•</span>
                                <span>{mechanic}</span>
                              </li>
                            ))}
                          </ul>
                        </div>

                        <div>
                          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">战术策略</h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">{boss.strategy}</p>
                        </div>

                        <div>
                          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">关键提示</h4>
                          <ul className="space-y-1">
                            {boss.tips.map((tip, idx) => (
                              <li key={idx} className="text-sm text-gray-600 dark:text-gray-400 flex items-start space-x-2">
                                <Zap className="h-4 w-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                                <span>{tip}</span>
                              </li>
                            ))}
                          </ul>
                        </div>

                        <div>
                          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">掉落物品</h4>
                          <div className="flex flex-wrap gap-2">
                            {boss.loot.map((item, idx) => (
                              <span
                                key={idx}
                                className="px-2 py-1 bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 rounded text-xs"
                              >
                                {item}
                              </span>
                            ))}
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
} 