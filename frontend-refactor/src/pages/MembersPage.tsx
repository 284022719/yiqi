import { useState, useEffect, useMemo } from 'react'
import { useQuery } from 'react-query'
import { Search, Filter, Users, AlertCircle } from 'lucide-react'
import { membersApi } from '@/services/api'
import LoadingSpinner from '@/components/LoadingSpinner'
import MemberDetailModal from '@/components/MemberDetailModal'
import ClassBadge from '@/components/ClassBadge'
import FactionBadge from '@/components/FactionBadge'
import OnlineStatusIndicator from '@/components/OnlineStatusIndicator'
import SortableHeader from '@/components/SortableHeader'
import { debounce } from '@/utils'
import { GuildMember } from '@/types'

export default function MembersPage() {
  const [page, setPage] = useState(1)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedClass, setSelectedClass] = useState('')
  const [selectedFaction, setSelectedFaction] = useState('')
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState('')
  const [selectedMember, setSelectedMember] = useState<GuildMember | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [sortBy, setSortBy] = useState('name')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc')

  // 防抖搜索
  useEffect(() => {
    const handler = debounce(() => {
      setDebouncedSearchTerm(searchTerm)
      setPage(1) // 重置到第一页
    }, 500)

    handler()
    return () => handler.cancel()
  }, [searchTerm])

  // 筛选变化时重置页码
  useEffect(() => {
    setPage(1)
  }, [selectedClass, selectedFaction])

  // 构建查询参数
  const queryParams = useMemo(() => ({
    page,
    size: 20,
    search: debouncedSearchTerm || undefined,
    class_name: selectedClass || undefined,
    faction: selectedFaction || undefined,
    sort_by: sortBy,
    sort_order: sortOrder,
  }), [page, debouncedSearchTerm, selectedClass, selectedFaction, sortBy, sortOrder])

  // 查询数据
  const { 
    data: membersData, 
    isLoading, 
    error,
    refetch 
  } = useQuery(
    ['members', queryParams],
    () => membersApi.getAll(queryParams),
    {
      keepPreviousData: true, // 保持之前的数据，避免闪烁
      staleTime: 30000, // 30秒内不重新请求
      retry: 3,
      refetchOnWindowFocus: false,
    }
  )

  // 使用真实数据
  const displayData = membersData

  // 处理搜索输入
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value)
  }

  // 处理职业筛选
  const handleClassChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedClass(e.target.value)
  }

  // 处理阵营筛选
  const handleFactionChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedFaction(e.target.value)
  }

  // 清除所有筛选
  const clearFilters = () => {
    setSearchTerm('')
    setSelectedClass('')
    setSelectedFaction('')
    setPage(1)
  }

  // 检查是否有活跃的筛选
  const hasActiveFilters = searchTerm || selectedClass || selectedFaction

  // 处理成员点击
  const handleMemberClick = (member: GuildMember) => {
    setSelectedMember(member)
    setIsModalOpen(true)
  }

  // 处理弹窗关闭
  const handleModalClose = () => {
    setIsModalOpen(false)
    setSelectedMember(null)
  }

  // 处理排序
  const handleSort = (key: string) => {
    if (sortBy === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(key)
      setSortOrder('asc')
    }
    setPage(1) // 重置到第一页
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                公会成员
              </h1>
              <p className="mt-2 text-gray-600 dark:text-gray-300">
                管理公会成员信息和数据
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
                <Users className="h-5 w-5" />
                <span>共 {membersData?.total || 0} 名成员</span>
              </div>
            </div>
          </div>
        </div>

        {/* Search and Filters */}
        <div className="mb-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="搜索成员姓名..."
                  value={searchTerm}
                  onChange={handleSearchChange}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <select
                value={selectedClass}
                onChange={handleClassChange}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="">所有职业</option>
                <option value="Death Knight">死亡骑士</option>
                <option value="Demon Hunter">恶魔猎手</option>
                <option value="Druid">德鲁伊</option>
                <option value="Evoker">唤魔师</option>
                <option value="Hunter">猎人</option>
                <option value="Mage">法师</option>
                <option value="Monk">武僧</option>
                <option value="Paladin">圣骑士</option>
                <option value="Priest">牧师</option>
                <option value="Rogue">潜行者</option>
                <option value="Shaman">萨满</option>
                <option value="Warlock">术士</option>
                <option value="Warrior">战士</option>
              </select>
              <select
                value={selectedFaction}
                onChange={handleFactionChange}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="">所有阵营</option>
                <option value="Alliance">联盟</option>
                <option value="Horde">部落</option>
              </select>
              {hasActiveFilters && (
                <button
                  onClick={clearFilters}
                  className="px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
                >
                  清除筛选
                </button>
              )}
            </div>
          </div>
          
          {/* 活跃筛选提示 */}
          {hasActiveFilters && (
            <div className="mt-3 flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
              <Filter className="h-4 w-4" />
              <span>
                筛选条件: 
                {searchTerm && <span className="ml-1 px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded">搜索: {searchTerm}</span>}
                {selectedClass && <span className="ml-1 px-2 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded">职业: {selectedClass}</span>}
                {selectedFaction && <span className="ml-1 px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 rounded">阵营: {selectedFaction}</span>}
              </span>
            </div>
          )}
        </div>

        {/* Members List */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          {isLoading ? (
            <div className="flex justify-center items-center py-12">
              <LoadingSpinner size="lg" />
            </div>
          ) : error ? (
            <div className="flex flex-col items-center justify-center py-12">
              <AlertCircle className="h-12 w-12 text-red-500 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                加载失败
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                {error instanceof Error ? error.message : '无法加载成员数据'}
              </p>
              <button
                onClick={() => refetch()}
                className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
              >
                重试
              </button>
            </div>
          ) : !displayData?.members || displayData.members.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12">
              <Users className="h-12 w-12 text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                {hasActiveFilters ? '没有找到匹配的成员' : '暂无成员数据'}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                {hasActiveFilters ? '请尝试调整搜索条件' : '请稍后再试'}
              </p>
              {hasActiveFilters && (
                <button
                  onClick={clearFilters}
                  className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
                >
                  清除筛选
                </button>
              )}
            </div>
          ) : (
            <>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead className="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th className="px-6 py-3 text-left">
                        <SortableHeader
                          label="成员信息"
                          sortKey="name"
                          currentSort={sortBy}
                          currentOrder={sortOrder}
                          onSort={handleSort}
                        />
                      </th>
                      <th className="px-6 py-3 text-left">
                        <SortableHeader
                          label="等级"
                          sortKey="level"
                          currentSort={sortBy}
                          currentOrder={sortOrder}
                          onSort={handleSort}
                        />
                      </th>
                      <th className="px-6 py-3 text-left">
                        <SortableHeader
                          label="Mythic+评分"
                          sortKey="mythic_plus_score"
                          currentSort={sortBy}
                          currentOrder={sortOrder}
                          onSort={handleSort}
                        />
                      </th>
                      <th className="px-6 py-3 text-left">
                        <SortableHeader
                          label="阵营"
                          sortKey="faction"
                          currentSort={sortBy}
                          currentOrder={sortOrder}
                          onSort={handleSort}
                        />
                      </th>
                      <th className="px-6 py-3 text-left">
                        <SortableHeader
                          label="成就点数"
                          sortKey="achievement_points"
                          currentSort={sortBy}
                          currentOrder={sortOrder}
                          onSort={handleSort}
                        />
                      </th>
                      <th className="px-6 py-3 text-left">
                        <SortableHeader
                          label="在线状态"
                          sortKey="last_online_days"
                          currentSort={sortBy}
                          currentOrder={sortOrder}
                          onSort={handleSort}
                        />
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                    {displayData.members.map((member) => (
                      <tr 
                        key={member.id} 
                        className="hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                        onClick={() => handleMemberClick(member)}
                      >
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="flex-shrink-0 h-10 w-10">
                              <div className="h-10 w-10 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center">
                                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                  {member.name.charAt(0).toUpperCase()}
                                </span>
                              </div>
                            </div>
                            <div className="ml-4">
                              <div className="text-sm font-medium text-gray-900 dark:text-white">
                                {member.name}
                              </div>
                              <div className="text-sm text-gray-500 dark:text-gray-400">
                                {member.realm_name}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900 dark:text-white">
                            {member.level}
                          </div>
                          <div className="mt-1">
                            <ClassBadge className={member.class_name} size="sm" showText={false} />
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900 dark:text-white">
                            {member.mythic_plus_score.toFixed(1)}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <FactionBadge faction={member.faction} size="sm" showText={false} />
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900 dark:text-white">
                            {member.achievement_points.toLocaleString()}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <OnlineStatusIndicator
                            isOnline={member.is_online}
                            lastOnlineDays={member.last_online_days}
                            size="sm"
                          />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Pagination */}
              {displayData && displayData.pages > 1 && (
                <div className="bg-white dark:bg-gray-800 px-4 py-3 flex items-center justify-between border-t border-gray-200 dark:border-gray-700 sm:px-6">
                  <div className="flex-1 flex justify-between sm:hidden">
                    <button
                      onClick={() => setPage(page - 1)}
                      disabled={page === 1}
                      className="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      上一页
                    </button>
                    <button
                      onClick={() => setPage(page + 1)}
                      disabled={page === displayData.pages}
                      className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      下一页
                    </button>
                  </div>
                  <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                    <div>
                      <p className="text-sm text-gray-700 dark:text-gray-300">
                        显示第 <span className="font-medium">{((page - 1) * 20) + 1}</span> 到{' '}
                        <span className="font-medium">
                          {Math.min(page * 20, displayData.total)}
                        </span> 条，
                        共 <span className="font-medium">{displayData.total}</span> 条记录
                      </p>
                    </div>
                    <div>
                      <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                        <button
                          onClick={() => setPage(page - 1)}
                          disabled={page === 1}
                          className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          上一页
                        </button>
                        <button
                          onClick={() => setPage(page + 1)}
                          disabled={page === displayData.pages}
                          className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          下一页
                        </button>
                      </nav>
                    </div>
                  </div>
                </div>
              )}
            </>
                     )}
         </div>
       </div>

       {/* 成员详情弹窗 */}
       <MemberDetailModal
         member={selectedMember}
         isOpen={isModalOpen}
         onClose={handleModalClose}
       />
     </div>
   )
 } 