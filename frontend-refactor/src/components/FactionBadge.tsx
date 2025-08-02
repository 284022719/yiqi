interface FactionBadgeProps {
  faction: string
  size?: 'sm' | 'md' | 'lg'
  showText?: boolean
}

const factionConfig = {
  'Alliance': {
    icon: '🦁',
    color: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    borderColor: 'border-blue-200 dark:border-blue-700'
  },
  'Horde': {
    icon: '🐺',
    color: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    borderColor: 'border-red-200 dark:border-red-700'
  }
}

export default function FactionBadge({ faction, size = 'md', showText = true }: FactionBadgeProps) {
  const config = factionConfig[faction as keyof typeof factionConfig] || factionConfig['Horde']
  
  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1.5',
    lg: 'text-base px-4 py-2'
  }

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full font-medium border ${config.color} ${config.borderColor} ${sizeClasses[size]}`}>
      <span className="text-lg">{config.icon}</span>
      {showText && <span>{faction}</span>}
    </span>
  )
} 