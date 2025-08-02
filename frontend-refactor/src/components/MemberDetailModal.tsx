import { Fragment } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { X, Crown, Shield, Sword, Trophy, Clock, MapPin, Users } from 'lucide-react'
import { GuildMember } from '@/types'
import { getClassColor } from '@/utils'

interface MemberDetailModalProps {
  member: GuildMember | null
  isOpen: boolean
  onClose: () => void
}

export default function MemberDetailModal({ member, isOpen, onClose }: MemberDetailModalProps) {
  if (!member) return null

  const classColor = getClassColor(member.class_name)
  const factionColor = member.faction === 'Alliance' ? 'text-blue-600' : 'text-red-600'
  const factionIcon = member.faction === 'Alliance' ? '🦁' : '🐺'

  return (
    <Transition.Root show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white dark:bg-gray-800 px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-2xl sm:p-6">
                <div className="absolute right-0 top-0 pr-4 pt-4">
                  <button
                    type="button"
                    className="rounded-md bg-white dark:bg-gray-800 text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                    onClick={onClose}
                  >
                    <span className="sr-only">关闭</span>
                    <X className="h-6 w-6" aria-hidden="true" />
                  </button>
                </div>

                <div className="sm:flex sm:items-start">
                  <div className="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-700 sm:mx-0 sm:h-10 sm:w-10">
                    <span className="text-lg font-medium text-gray-700 dark:text-gray-300">
                      {member.name.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left w-full">
                    <Dialog.Title as="h3" className="text-lg font-semibold leading-6 text-gray-900 dark:text-white">
                      {member.name}
                    </Dialog.Title>
                    <div className="mt-2">
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {member.realm_name} • {member.faction} {factionIcon}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="mt-6">
                  {/* 基本信息 */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* 左侧信息 */}
                    <div className="space-y-4">
                      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                        <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                          <Crown className="h-4 w-4 mr-2" />
                          基本信息
                        </h4>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-500 dark:text-gray-400">等级</span>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">{member.level}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-500 dark:text-gray-400">职业</span>
                            <span className={`text-sm font-medium ${classColor}`}>{member.class_name}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-500 dark:text-gray-400">种族</span>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">{member.race_name}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-500 dark:text-gray-400">阵营</span>
                            <span className={`text-sm font-medium ${factionColor}`}>{member.faction}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-500 dark:text-gray-400">公会职位</span>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">{member.guild_rank}</span>
                          </div>
                        </div>
                      </div>

                      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                        <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                          <Shield className="h-4 w-4 mr-2" />
                          装备信息
                        </h4>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-500 dark:text-gray-400">平均装等</span>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">{member.average_item_level}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-500 dark:text-gray-400">坐骑数量</span>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">{member.mounts_count}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* 右侧信息 */}
                    <div className="space-y-4">
                      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                        <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                          <Sword className="h-4 w-4 mr-2" />
                          游戏数据
                        </h4>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-500 dark:text-gray-400">Mythic+评分</span>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">{member.mythic_plus_score.toFixed(1)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-500 dark:text-gray-400">成就点数</span>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">{member.achievement_points.toLocaleString()}</span>
                          </div>
                        </div>
                      </div>

                      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                        <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                          <Clock className="h-4 w-4 mr-2" />
                          在线状态
                        </h4>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-500 dark:text-gray-400">状态</span>
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              member.is_online 
                                ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                                : 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
                            }`}>
                              {member.is_online ? '在线' : '离线'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-500 dark:text-gray-400">最后在线</span>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">
                              {member.last_online_days > 0 ? `${member.last_online_days} 天前` : '今天'}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* 备注信息 */}
                  {member.note && (
                    <div className="mt-6 bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                      <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-2">备注</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">{member.note}</p>
                    </div>
                  )}

                  {/* 时间信息 */}
                  <div className="mt-6 bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                    <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                      <Trophy className="h-4 w-4 mr-2" />
                      时间信息
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-500 dark:text-gray-400">创建时间</span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          {new Date(member.created_at).toLocaleDateString('zh-CN')}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-500 dark:text-gray-400">更新时间</span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          {new Date(member.updated_at).toLocaleDateString('zh-CN')}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-6 sm:mt-4 sm:flex sm:flex-row-reverse">
                  <button
                    type="button"
                    className="inline-flex w-full justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 sm:ml-3 sm:w-auto"
                    onClick={onClose}
                  >
                    关闭
                  </button>
                  <button
                    type="button"
                    className="mt-3 inline-flex w-full justify-center rounded-md bg-white dark:bg-gray-700 px-3 py-2 text-sm font-semibold text-gray-900 dark:text-white shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600 sm:mt-0 sm:w-auto"
                    onClick={() => {
                      // TODO: 实现编辑功能
                      console.log('编辑成员:', member.id)
                    }}
                  >
                    编辑信息
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  )
} 