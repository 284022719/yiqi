import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { motion } from 'framer-motion'
import { 
  Play, 
  Pause, 
  RefreshCw, 
  Database, 
  Activity,
  Clock,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Settings,
  Download,
  Upload
} from 'lucide-react'
import { crawlerApi } from '@/services/api'
import LoadingSpinner from '@/components/LoadingSpinner'

interface CrawlHistory {
  id: number
  started_at: string
  completed_at: string
  status: 'completed' | 'failed' | 'running'
  members_processed: number
  errors: number
}

interface GuildInfo {
  guild_name: string
  realm: string
  faction: string
  total_members: number
  active_members: number
  online_members: number
  last_updated: string
}

export default function CrawlerPage() {
  const [isStarting, setIsStarting] = useState(false)
  const queryClient = useQueryClient()

  // 查询爬虫状态
  const { data: crawlerStatus, isLoading: statusLoading } = useQuery(
    'crawler-status',
    crawlerApi.getStatus
  )

  // 查询公会信息
  const { data: guildInfo, isLoading: guildInfoLoading } = useQuery(
    'guild-info',
    crawlerApi.getGuildInfo
  )

  // 查询爬虫历史
  const { data: crawlHistory, isLoading: historyLoading } = useQuery(
    'crawl-history',
    crawlerApi.getCrawlHistory
  )

  // 启动爬虫
  const startCrawlerMutation = useMutation(crawlerApi.startCrawler, {
    onSuccess: () => {
      queryClient.invalidateQueries('crawler-status')
      queryClient.invalidateQueries('guild-info')
      queryClient.invalidateQueries('crawl-history')
    }
  })

  // 同步数据
  const syncDataMutation = useMutation(crawlerApi.syncData, {
    onSuccess: () => {
      queryClient.invalidateQueries('members')
      queryClient.invalidateQueries('statistics')
      queryClient.invalidateQueries('guild-info')
    }
  })

  // 测试API
  const testApiMutation = useMutation(crawlerApi.testApi)

  const handleStartCrawler = async () => {
    setIsStarting(true)
    try {
      await startCrawlerMutation.mutateAsync()
    } finally {
      setIsStarting(false)
    }
  }

  const handleSyncData = async () => {
    if (confirm('确定要同步公会数据吗？这将覆盖现有数据。')) {
      await syncDataMutation.mutateAsync()
    }
  }

  const handleTestApi = async () => {
    await testApiMutation.mutateAsync()
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('zh-CN')
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900'
      case 'running': return 'text-blue-600 bg-blue-100 dark:text-blue-400 dark:bg-blue-900'
      case 'failed': return 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900'
      default: return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="h-4 w-4" />
      case 'running': return <Activity className="h-4 w-4" />
      case 'failed': return <XCircle className="h-4 w-4" />
      default: return <AlertTriangle className="h-4 w-4" />
    }
  }

  if (statusLoading || guildInfoLoading || historyLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                数据爬虫管理
              </h1>
              <p className="mt-2 text-gray-600 dark:text-gray-300">
                管理公会数据抓取和同步任务
              </p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
              <Database className="h-5 w-5" />
              <span>数据管理</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 控制面板 */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6"
            >
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
                控制面板
              </h2>

              <div className="space-y-4">
                <button
                  onClick={handleStartCrawler}
                  disabled={isStarting || startCrawlerMutation.isLoading}
                  className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isStarting || startCrawlerMutation.isLoading ? (
                    <RefreshCw className="h-4 w-4 animate-spin" />
                  ) : (
                    <Play className="h-4 w-4" />
                  )}
                  <span>启动爬虫</span>
                </button>

                <button
                  onClick={handleSyncData}
                  disabled={syncDataMutation.isLoading}
                  className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {syncDataMutation.isLoading ? (
                    <RefreshCw className="h-4 w-4 animate-spin" />
                  ) : (
                    <Upload className="h-4 w-4" />
                  )}
                  <span>同步数据</span>
                </button>

                <button
                  onClick={handleTestApi}
                  disabled={testApiMutation.isLoading}
                  className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {testApiMutation.isLoading ? (
                    <RefreshCw className="h-4 w-4 animate-spin" />
                  ) : (
                    <Settings className="h-4 w-4" />
                  )}
                  <span>测试API</span>
                </button>
              </div>

              {/* 状态信息 */}
              <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-600">
                <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-3">
                  当前状态
                </h3>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600 dark:text-gray-400">爬虫状态</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(crawlerStatus?.status || 'idle')}`}>
                      {crawlerStatus?.status === 'idle' ? '空闲' : 
                       crawlerStatus?.status === 'running' ? '运行中' : 
                       crawlerStatus?.status === 'completed' ? '已完成' : '未知'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600 dark:text-gray-400">最后运行</span>
                    <span className="text-gray-900 dark:text-white">
                      {crawlerStatus?.last_run ? formatDate(crawlerStatus.last_run) : '从未运行'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600 dark:text-gray-400">处理成员</span>
                    <span className="text-gray-900 dark:text-white">
                      {crawlerStatus?.total_members_crawled || 0}
                    </span>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>

          {/* 公会信息 */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6"
            >
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
                公会信息
              </h2>

              {guildInfo && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">公会名称</h3>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white">{guildInfo.guild_name}</p>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">服务器</h3>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white">{guildInfo.realm}</p>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">阵营</h3>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white">{guildInfo.faction}</p>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">总成员数</h3>
                      <p className="text-2xl font-bold text-gray-900 dark:text-white">{guildInfo.total_members}</p>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">活跃成员</h3>
                      <p className="text-2xl font-bold text-green-600 dark:text-green-400">{guildInfo.active_members}</p>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">在线成员</h3>
                      <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">{guildInfo.online_members}</p>
                    </div>
                  </div>
                </div>
              )}

              <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-600">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500 dark:text-gray-400">最后更新</span>
                  <span className="text-sm text-gray-900 dark:text-white">
                    {guildInfo?.last_updated ? formatDate(guildInfo.last_updated) : '未知'}
                  </span>
                </div>
              </div>
            </motion.div>
          </div>
        </div>

        {/* 爬虫历史 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6"
        >
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
            爬虫历史记录
          </h2>

          {crawlHistory?.history && crawlHistory.history.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      任务ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      开始时间
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      完成时间
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      状态
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      处理成员
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      错误数
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {crawlHistory.history.map((record: CrawlHistory) => (
                    <tr key={record.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                        #{record.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {formatDate(record.started_at)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {record.completed_at ? formatDate(record.completed_at) : '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(record.status)}`}>
                          {getStatusIcon(record.status)}
                          <span className="ml-1">
                            {record.status === 'completed' ? '已完成' : 
                             record.status === 'running' ? '运行中' : 
                             record.status === 'failed' ? '失败' : '未知'}
                          </span>
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                        {record.members_processed}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                        {record.errors}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8">
              <Database className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">暂无历史记录</h3>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                还没有执行过爬虫任务
              </p>
            </div>
          )}
        </motion.div>

        {/* 操作结果提示 */}
        {(startCrawlerMutation.isSuccess || syncDataMutation.isSuccess || testApiMutation.isSuccess) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg"
          >
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5" />
              <span>
                {startCrawlerMutation.isSuccess && '爬虫启动成功'}
                {syncDataMutation.isSuccess && '数据同步成功'}
                {testApiMutation.isSuccess && 'API测试成功'}
              </span>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
} 