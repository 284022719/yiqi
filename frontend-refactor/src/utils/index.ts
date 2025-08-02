import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

// 合并CSS类名
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// 格式化数字
export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

// 格式化日期
export function formatDate(date: string | Date): string {
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// 格式化时间
export function formatDateTime(date: string | Date): string {
  const d = new Date(date)
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 获取职业颜色
export function getClassColor(className: string): string {
  const classColors: Record<string, string> = {
    'Death Knight': 'text-death-knight',
    'Demon Hunter': 'text-demon-hunter',
    'Druid': 'text-druid',
    'Evoker': 'text-evoker',
    'Hunter': 'text-hunter',
    'Mage': 'text-mage',
    'Monk': 'text-monk',
    'Paladin': 'text-paladin',
    'Priest': 'text-priest',
    'Rogue': 'text-rogue',
    'Shaman': 'text-shaman',
    'Warlock': 'text-warlock',
    'Warrior': 'text-warrior',
  }
  return classColors[className] || 'text-gray-600'
}

// 获取阵营颜色
export function getFactionColor(faction: string): string {
  return faction === 'Alliance' ? 'text-alliance' : 'text-horde'
}

// 获取在线状态文本
export function getOnlineStatusText(lastOnlineDays: number): string {
  if (lastOnlineDays === 0) return '在线'
  if (lastOnlineDays < 1) return '今天在线'
  if (lastOnlineDays < 7) return `${Math.floor(lastOnlineDays)}天前`
  if (lastOnlineDays < 30) return `${Math.floor(lastOnlineDays / 7)}周前`
  if (lastOnlineDays < 365) return `${Math.floor(lastOnlineDays / 30)}个月前`
  return `${Math.floor(lastOnlineDays / 365)}年前`
}

// 获取在线状态颜色
export function getOnlineStatusColor(lastOnlineDays: number): string {
  if (lastOnlineDays === 0) return 'text-green-500'
  if (lastOnlineDays < 1) return 'text-green-400'
  if (lastOnlineDays < 7) return 'text-yellow-500'
  if (lastOnlineDays < 30) return 'text-orange-500'
  return 'text-red-500'
}

// 防抖函数
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

// 节流函数
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

// 本地存储工具
export const storage = {
  get: <T>(key: string, defaultValue?: T): T | null => {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : defaultValue || null
    } catch {
      return defaultValue || null
    }
  },
  set: <T>(key: string, value: T): void => {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch {
      // 忽略错误
    }
  },
  remove: (key: string): void => {
    try {
      localStorage.removeItem(key)
    } catch {
      // 忽略错误
    }
  },
}

// 验证邮箱
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// 验证URL
export function isValidUrl(url: string): boolean {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

// 生成随机ID
export function generateId(): string {
  return Math.random().toString(36).substr(2, 9)
}

// 深拷贝对象
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj.getTime()) as unknown as T
  if (obj instanceof Array) return obj.map(item => deepClone(item)) as unknown as T
  if (typeof obj === 'object') {
    const clonedObj = {} as T
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key])
      }
    }
    return clonedObj
  }
  return obj
}

// 数组去重
export function uniqueArray<T>(array: T[], key?: keyof T): T[] {
  if (!key) {
    return [...new Set(array)]
  }
  const seen = new Set()
  return array.filter(item => {
    const value = item[key]
    if (seen.has(value)) {
      return false
    }
    seen.add(value)
    return true
  })
}

// 数组分组
export function groupBy<T>(array: T[], key: keyof T): Record<string, T[]> {
  return array.reduce((groups, item) => {
    const group = String(item[key])
    groups[group] = groups[group] || []
    groups[group].push(item)
    return groups
  }, {} as Record<string, T[]>)
}

// 数组排序
export function sortBy<T>(array: T[], key: keyof T, order: 'asc' | 'desc' = 'asc'): T[] {
  return [...array].sort((a, b) => {
    const aVal = a[key]
    const bVal = b[key]
    
    if (aVal < bVal) return order === 'asc' ? -1 : 1
    if (aVal > bVal) return order === 'asc' ? 1 : -1
    return 0
  })
} 