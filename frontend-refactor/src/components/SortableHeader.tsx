import { ChevronUp, ChevronDown } from 'lucide-react'

interface SortableHeaderProps {
  label: string
  sortKey: string
  currentSort: string
  currentOrder: 'asc' | 'desc'
  onSort: (key: string) => void
}

export default function SortableHeader({ 
  label, 
  sortKey, 
  currentSort, 
  currentOrder, 
  onSort 
}: SortableHeaderProps) {
  const isActive = currentSort === sortKey

  return (
    <button
      onClick={() => onSort(sortKey)}
      className="group inline-flex items-center gap-1 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider hover:text-gray-700 dark:hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded"
    >
      {label}
      <div className="flex flex-col">
        <ChevronUp 
          className={`h-3 w-3 transition-colors ${
            isActive && currentOrder === 'asc' 
              ? 'text-primary-600 dark:text-primary-400' 
              : 'text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300'
          }`} 
        />
        <ChevronDown 
          className={`h-3 w-3 -mt-1 transition-colors ${
            isActive && currentOrder === 'desc' 
              ? 'text-primary-600 dark:text-primary-400' 
              : 'text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300'
          }`} 
        />
      </div>
    </button>
  )
} 