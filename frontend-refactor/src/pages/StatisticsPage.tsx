import { useState } from 'react'
import { useQuery } from 'react-query'
import { motion } from 'framer-motion'
import { 
  BarChart3, 
  Users, 
  TrendingUp, 
  Award, 
  Clock, 
  MapPin,
  Activity,
  Target,
  Zap,
  Crown
} from 'lucide-react'
import { statisticsApi } from '@/services/api'
import LoadingSpinner from '@/components/LoadingSpinner'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts'

const COLORS = [
  '#3B82F6', '#10B981', '#F59E0B', '#EF4444', 
  '#8B5CF6', '#06B6D4', '#84CC16', '#F97316',
  '#EC4899', '#6366F1', '#14B8A6', '#F43F5E'
]

export default function StatisticsPage() {
  const [activeTab, setActiveTab] = useState('overview')

  const { data: overview, isLoading: overviewLoading } = useQuery(
    'statistics-overview',
    statisticsApi.getOverview
  )

  const { data: classDistribution, isLoading: classLoading } = useQuery(
    'statistics-class-distribution',
    statisticsApi.getClassDistribution
  )

  const { data: realmDistribution, isLoading: realmLoading } = useQuery(
    'statistics-realm-distribution',
    statisticsApi.getRealmDistribution
  )

  const { data: mythicPlusStats, isLoading: mythicLoading } = useQuery(
    'statistics-mythic-plus-stats',
    statisticsApi.getMythicPlusStats
  )

  const isLoading = overviewLoading || classLoading || realmLoading || mythicLoading

  const tabs = [
    { id: 'overview', name: '总览', icon: BarChart3 },
    { id: 'classes', name: '职业分布', icon: Users },
    { id: 'realms', name: '服务器分布', icon: MapPin },
    { id: 'mythic', name: 'Mythic+统计', icon: Target },
  ]

  const formatNumber = (num: number) => {
    return num.toLocaleString()
  }

  const formatPercentage = (value: number, total: number) => {
    return ((value / total) * 100).toFixed(1)
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                数据统计
              </h1>
              <p className="mt-2 text-gray-600 dark:text-gray-300">
                公会成员数据分析和统计报告
              </p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
              <Activity className="h-5 w-5" />
              <span>实时更新</span>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-8">
          <nav className="flex space-x-8" aria-label="Tabs">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.name}</span>
                </button>
              )
            })}
          </nav>
        </div>

        {/* Content */}
        {isLoading ? (
          <div className="flex justify-center items-center py-12">
            <LoadingSpinner size="lg" />
          </div>
        ) : (
          <div className="space-y-8">
            {/* Overview Tab */}
            {activeTab === 'overview' && overview && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="space-y-8"
              >
                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <Users className="h-8 w-8 text-blue-500" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">总成员数</p>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white">
                          {formatNumber(overview.total_members)}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <Activity className="h-8 w-8 text-green-500" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">活跃成员</p>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white">
                          {formatNumber(overview.active_members)}
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {formatPercentage(overview.active_members, overview.total_members)}% 活跃率
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <Clock className="h-8 w-8 text-yellow-500" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">在线成员</p>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white">
                          {formatNumber(overview.online_members)}
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {formatPercentage(overview.online_members, overview.total_members)}% 在线率
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <Crown className="h-8 w-8 text-purple-500" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">职业种类</p>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white">
                          {formatNumber(overview.classes_count)}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Additional Stats */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                      平均数据
                    </h3>
                    <div className="space-y-4">
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">平均等级</span>
                        <span className="font-medium text-gray-900 dark:text-white">
                          {overview.average_level?.toFixed(1) || 'N/A'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">平均装等</span>
                        <span className="font-medium text-gray-900 dark:text-white">
                          {overview.average_item_level?.toFixed(1) || 'N/A'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">平均Mythic+评分</span>
                        <span className="font-medium text-gray-900 dark:text-white">
                          {overview.average_mythic_plus_score?.toFixed(1) || 'N/A'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">平均成就点数</span>
                        <span className="font-medium text-gray-900 dark:text-white">
                          {formatNumber(overview.average_achievement_points || 0)}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                      顶级玩家
                    </h3>
                    <div className="space-y-4">
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">最高等级</span>
                        <span className="font-medium text-gray-900 dark:text-white">
                          {overview.max_level || 'N/A'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">最高装等</span>
                        <span className="font-medium text-gray-900 dark:text-white">
                          {overview.max_item_level?.toFixed(1) || 'N/A'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">最高Mythic+评分</span>
                        <span className="font-medium text-gray-900 dark:text-white">
                          {overview.max_mythic_plus_score?.toFixed(1) || 'N/A'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">最高成就点数</span>
                        <span className="font-medium text-gray-900 dark:text-white">
                          {formatNumber(overview.max_achievement_points || 0)}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Class Distribution Tab */}
            {activeTab === 'classes' && classDistribution && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="space-y-8"
              >
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
                      职业分布
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={classDistribution}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="count"
                        >
                          {classDistribution.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
                      职业统计
                    </h3>
                    <div className="space-y-4">
                      {classDistribution.map((item, index) => (
                        <div key={item.class_name} className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <div 
                              className="w-4 h-4 rounded-full"
                              style={{ backgroundColor: COLORS[index % COLORS.length] }}
                            />
                            <span className="text-gray-900 dark:text-white">{item.class_name}</span>
                          </div>
                          <div className="text-right">
                            <div className="font-medium text-gray-900 dark:text-white">
                              {item.count}
                            </div>
                            <div className="text-sm text-gray-500 dark:text-gray-400">
                              {formatPercentage(item.count, overview?.total_members || 1)}%
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Realm Distribution Tab */}
            {activeTab === 'realms' && realmDistribution && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="space-y-8"
              >
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
                    服务器分布
                  </h3>
                  <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={realmDistribution}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="realm_name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#3B82F6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {realmDistribution.map((item, index) => (
                    <div key={item.realm_name} className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="font-medium text-gray-900 dark:text-white">{item.realm_name}</h4>
                          <p className="text-sm text-gray-500 dark:text-gray-400">
                            {formatPercentage(item.count, overview?.total_members || 1)}% 的成员
                          </p>
                        </div>
                        <div className="text-2xl font-bold text-gray-900 dark:text-white">
                          {item.count}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Mythic+ Stats Tab */}
            {activeTab === 'mythic' && mythicPlusStats && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="space-y-8"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <Target className="h-8 w-8 text-blue-500" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">平均评分</p>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white">
                          {mythicPlusStats.average_score?.toFixed(1) || 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <Zap className="h-8 w-8 text-yellow-500" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">最高评分</p>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white">
                          {mythicPlusStats.max_score?.toFixed(1) || 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <Award className="h-8 w-8 text-green-500" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">评分分布</p>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white">
                          {mythicPlusStats.score_distribution?.length || 0}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <TrendingUp className="h-8 w-8 text-purple-500" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">活跃玩家</p>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white">
                          {mythicPlusStats.active_players || 0}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {mythicPlusStats.score_distribution && (
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
                      评分分布趋势
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={mythicPlusStats.score_distribution}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="range" />
                        <YAxis />
                        <Tooltip />
                        <Line type="monotone" dataKey="count" stroke="#3B82F6" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </motion.div>
            )}
          </div>
        )}
      </div>
    </div>
  )
} 