import { Wifi, WifiOff } from 'lucide-react'

interface OnlineStatusIndicatorProps {
  isOnline: boolean
  lastOnlineDays: number
  size?: 'sm' | 'md' | 'lg'
}

export default function OnlineStatusIndicator({ isOnline, lastOnlineDays, size = 'md' }: OnlineStatusIndicatorProps) {
  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1.5',
    lg: 'text-base px-4 py-2'
  }

  const getStatusText = () => {
    if (isOnline) return '在线'
    if (lastOnlineDays === 0) return '今天'
    if (lastOnlineDays === 1) return '昨天'
    if (lastOnlineDays < 7) return `${lastOnlineDays}天前`
    if (lastOnlineDays < 30) return `${Math.floor(lastOnlineDays / 7)}周前`
    return `${Math.floor(lastOnlineDays / 30)}月前`
  }

  const getStatusColor = () => {
    if (isOnline) {
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
    }
    if (lastOnlineDays <= 1) {
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
    }
    if (lastOnlineDays <= 7) {
      return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
    }
    return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
  }

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full font-medium ${getStatusColor()} ${sizeClasses[size]}`}>
      {isOnline ? (
        <Wifi className="h-3 w-3" />
      ) : (
        <WifiOff className="h-3 w-3" />
      )}
      <span>{getStatusText()}</span>
    </span>
  )
} 