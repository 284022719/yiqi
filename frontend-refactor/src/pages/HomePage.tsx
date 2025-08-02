import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Users, 
  BarChart3, 
  Image, 
  BookOpen, 
  Trophy, 
  Shield,
  ArrowRight,
  Star
} from 'lucide-react'
import { useQuery } from 'react-query'
import { statisticsApi } from '@/services/api'
import LoadingSpinner from '@/components/LoadingSpinner'

const features = [
  {
    name: '公会成员管理',
    description: '查看和管理公会成员信息，包括等级、装备、成就等详细数据。',
    icon: Users,
    href: '/members',
    color: 'bg-blue-500',
  },
  {
    name: '数据统计分析',
    description: '全面的公会数据统计，包括职业分布、服务器分布、Mythic+排名等。',
    icon: BarChart3,
    href: '/statistics',
    color: 'bg-green-500',
  },
  {
    name: '图片画廊',
    description: '公会活动照片和精彩瞬间的展示平台。',
    icon: Image,
    href: '/gallery',
    color: 'bg-purple-500',
  },
  {
    name: 'H6攻略',
    description: '详细的H6副本攻略和团队配置指南。',
    icon: BookOpen,
    href: '/h6',
    color: 'bg-orange-500',
  },
  {
    name: 'H7攻略',
    description: '最新的H7副本攻略和战术分析。',
    icon: Shield,
    href: '/h7',
    color: 'bg-red-500',
  },
]

export default function HomePage() {
  const { data: statistics, isLoading, error } = useQuery('statistics-overview', statisticsApi.getOverview, {
    retry: 3,
    refetchOnWindowFocus: false,
    staleTime: 5 * 60 * 1000, // 5分钟缓存
  })

  // 使用真实数据
  const displayStatistics = statistics

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-primary-950 dark:via-gray-900 dark:to-secondary-950">
        <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl">
                欢迎来到{' '}
                <span className="text-gradient">易骑公会</span>
              </h1>
              <p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300">
                魔兽世界公会管理平台，提供成员管理、数据统计、攻略分享等全方位服务。
                让我们一起在艾泽拉斯大陆上书写属于我们的传奇！
              </p>
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <Link
                  to="/members"
                  className="btn-primary btn-lg"
                >
                  查看成员
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
                <Link
                  to="/statistics"
                  className="btn-outline btn-lg"
                >
                  数据统计
                </Link>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:max-w-none">
            <div className="text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
                公会概况
              </h2>
              <p className="mt-4 text-lg leading-8 text-gray-600 dark:text-gray-300">
                实时更新的公会数据统计
              </p>
            </div>
            
            {isLoading ? (
              <div className="mt-16 flex justify-center">
                <LoadingSpinner size="lg" />
              </div>
            ) : error ? (
              <div className="mt-16 flex justify-center">
                <div className="text-center">
                  <p className="text-red-600 dark:text-red-400">加载数据失败</p>
                  <p className="text-gray-600 dark:text-gray-400 text-sm mt-2">请检查网络连接</p>
                </div>
              </div>
            ) : displayStatistics ? (
              <dl className="mt-16 grid grid-cols-1 gap-0.5 overflow-hidden rounded-2xl text-center sm:grid-cols-2 lg:grid-cols-4">
                <div className="flex flex-col bg-white dark:bg-gray-800 p-8">
                  <dt className="text-sm font-semibold leading-6 text-gray-600 dark:text-gray-400">
                    总成员数
                  </dt>
                  <dd className="order-first text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
                    {displayStatistics.total_members}
                  </dd>
                </div>
                <div className="flex flex-col bg-white dark:bg-gray-800 p-8">
                  <dt className="text-sm font-semibold leading-6 text-gray-600 dark:text-gray-400">
                    活跃成员
                  </dt>
                  <dd className="order-first text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
                    {displayStatistics.active_members}
                  </dd>
                </div>
                <div className="flex flex-col bg-white dark:bg-gray-800 p-8">
                  <dt className="text-sm font-semibold leading-6 text-gray-600 dark:text-gray-400">
                    在线成员
                  </dt>
                  <dd className="order-first text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
                    {displayStatistics.online_members}
                  </dd>
                </div>
                <div className="flex flex-col bg-white dark:bg-gray-800 p-8">
                  <dt className="text-sm font-semibold leading-6 text-gray-600 dark:text-gray-400">
                    职业种类
                  </dt>
                  <dd className="order-first text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
                    {displayStatistics.classes_count}
                  </dd>
                </div>
              </dl>
            ) : (
              <div className="mt-16 flex justify-center">
                <div className="text-center">
                  <p className="text-gray-600 dark:text-gray-400">暂无数据</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:text-center">
            <h2 className="text-base font-semibold leading-7 text-primary-600 dark:text-primary-400">
              功能特色
            </h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              一切为了更好的公会体验
            </p>
            <p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300">
              我们提供全方位的公会管理工具，从成员管理到数据统计，从攻略分享到活动记录，
              让公会管理变得更加简单高效。
            </p>
          </div>
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
              {features.map((feature, index) => (
                <motion.div
                  key={feature.name}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="flex flex-col"
                >
                  <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900 dark:text-white">
                    <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${feature.color}`}>
                      <feature.icon className="h-6 w-6 text-white" aria-hidden="true" />
                    </div>
                    {feature.name}
                  </dt>
                  <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600 dark:text-gray-300">
                    <p className="flex-auto">{feature.description}</p>
                    <p className="mt-6">
                      <Link
                        to={feature.href}
                        className="text-sm font-semibold leading-6 text-primary-600 dark:text-primary-400 hover:text-primary-500 dark:hover:text-primary-300"
                      >
                        了解更多 <span aria-hidden="true">→</span>
                      </Link>
                    </p>
                  </dd>
                </motion.div>
              ))}
            </dl>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              准备好加入我们了吗？
            </h2>
            <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-600 dark:text-gray-300">
              加入易骑公会，与志同道合的伙伴一起征战艾泽拉斯，创造属于我们的传奇故事。
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                to="/members"
                className="btn-primary btn-lg"
              >
                查看成员列表
              </Link>
              <Link
                to="/statistics"
                className="btn-outline btn-lg"
              >
                查看统计数据
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
} 