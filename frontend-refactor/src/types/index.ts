// 公会成员类型定义
export interface GuildMember {
  id: number
  name: string
  realm_name: string
  level: number
  class_name: string
  race_name: string
  faction: string
  mythic_plus_score: number
  achievement_points: number
  mounts_count: number
  average_item_level: number
  last_online_days: number
  is_online: boolean
  guild_rank: string
  note?: string
  created_at: string
  updated_at: string
}

// API响应类型
export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

// 分页响应类型
export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  size: number
  pages: number
}

// 统计信息类型
export interface Statistics {
  total_members: number
  active_members: number
  classes_count: number
  realms_count: number
  online_members: number
  top_mythic_players: GuildMember[]
  top_mount_collectors: GuildMember[]
  top_achievement_players: GuildMember[]
  // 平均数据
  average_level?: number
  average_item_level?: number
  average_mythic_plus_score?: number
  average_achievement_points?: number
  // 最高数据
  max_level?: number
  max_item_level?: number
  max_mythic_plus_score?: number
  max_achievement_points?: number
}

// 职业分布类型
export interface ClassDistribution {
  class_name: string
  count: number
  percentage: number
}

// 服务器分布类型
export interface RealmDistribution {
  realm_name: string
  count: number
  percentage: number
}

// 搜索响应类型
export interface SearchResponse {
  results: GuildMember[]
  total: number
  query: string
}

// 搜索参数类型
export interface SearchParams {
  q?: string
  class_name?: string
  realm_name?: string
  faction?: string
  min_level?: number
  max_level?: number
  min_mythic_score?: number
  page?: number
  size?: number
}

// 表单类型
export interface GuildMemberForm {
  name: string
  realm_name: string
  level: number
  class_name: string
  race_name: string
  faction: string
  mythic_plus_score?: number
  achievement_points?: number
  mounts_count?: number
  average_item_level?: number
  last_online_days?: number
  is_online?: boolean
  guild_rank?: string
  note?: string
}

// 导航项类型
export interface NavItem {
  label: string
  href: string
  icon?: React.ComponentType<{ className?: string }>
  children?: NavItem[]
}

// 主题类型
export type Theme = 'light' | 'dark' | 'system'

// 用户设置类型
export interface UserSettings {
  theme: Theme
  language: string
  notifications: boolean
}

// 错误类型
export interface ApiError {
  message: string
  status: number
  code?: string
  details?: any
}

// 加载状态类型
export type LoadingState = 'idle' | 'loading' | 'success' | 'error'

// 职业颜色映射
export interface ClassColors {
  [key: string]: string
}

// 阵营类型
export type Faction = 'Alliance' | 'Horde'

// 职业类型
export type ClassName = 
  | 'Death Knight' 
  | 'Demon Hunter' 
  | 'Druid' 
  | 'Evoker' 
  | 'Hunter' 
  | 'Mage' 
  | 'Monk' 
  | 'Paladin' 
  | 'Priest' 
  | 'Rogue' 
  | 'Shaman' 
  | 'Warlock' 
  | 'Warrior'

// 种族类型
export type RaceName = 
  | 'Human' 
  | 'Dwarf' 
  | 'Night Elf' 
  | 'Gnome' 
  | 'Draenei' 
  | 'Worgen' 
  | 'Pandaren' 
  | 'Void Elf' 
  | 'Lightforged Draenei' 
  | 'Dark Iron Dwarf' 
  | 'Kul Tiran' 
  | 'Mechagnome' 
  | 'Orc' 
  | 'Undead' 
  | 'Tauren' 
  | 'Troll' 
  | 'Blood Elf' 
  | 'Goblin' 
  | 'Highmountain Tauren' 
  | 'Nightborne' 
  | 'Mag\'har Orc' 
  | 'Zandalari Troll' 
  | 'Vulpera' 
  | 'Dracthyr'

// Mythic+统计类型
export interface MythicPlusStats {
  average_score?: number
  max_score?: number
  active_players: number
  score_distribution: ScoreDistribution[]
}

// 评分分布类型
export interface ScoreDistribution {
  range: string
  count: number
} 