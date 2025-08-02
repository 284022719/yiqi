import { getClassColor } from '@/utils'

interface ClassBadgeProps {
  className: string
  size?: 'sm' | 'md' | 'lg'
  showText?: boolean
}

const classIcons: Record<string, string> = {
  'Death Knight': '💀',
  'Demon Hunter': '👁️',
  'Druid': '🌿',
  'Evoker': '🐉',
  'Hunter': '🏹',
  'Mage': '🔮',
  'Monk': '🍃',
  'Paladin': '⚔️',
  'Priest': '✝️',
  'Rogue': '🗡️',
  'Shaman': '⚡',
  'Warlock': '🔥',
  'Warrior': '🛡️',
}

export default function ClassBadge({ className, size = 'md', showText = true }: ClassBadgeProps) {
  const classColor = getClassColor(className)
  const icon = classIcons[className] || '❓'
  
  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1.5',
    lg: 'text-base px-4 py-2'
  }

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full font-medium ${classColor} ${sizeClasses[size]}`}>
      <span className="text-lg">{icon}</span>
      {showText && <span>{className}</span>}
    </span>
  )
} 