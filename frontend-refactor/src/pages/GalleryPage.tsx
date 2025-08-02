import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Image, 
  Calendar, 
  Users, 
  MapPin, 
  Heart,
  Share2,
  Download,
  X
} from 'lucide-react'

interface GalleryItem {
  id: number
  title: string
  description: string
  imageUrl: string
  date: string
  location: string
  participants: number
  likes: number
  category: 'raid' | 'pvp' | 'social' | 'achievement'
}

// 模拟数据
const galleryData: GalleryItem[] = [
  {
    id: 1,
    title: 'H6首杀庆祝',
    description: '公会成功完成H6副本首杀，全体成员合影留念',
    imageUrl: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&h=600&fit=crop',
    date: '2024-01-15',
    location: '艾泽拉斯',
    participants: 25,
    likes: 42,
    category: 'raid'
  },
  {
    id: 2,
    title: 'PVP竞技场',
    description: '公会PVP战队在竞技场中的精彩表现',
    imageUrl: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&h=600&fit=crop',
    date: '2024-01-10',
    location: '竞技场',
    participants: 10,
    likes: 28,
    category: 'pvp'
  },
  {
    id: 3,
    title: '公会聚会',
    description: '线下公会聚会，增进成员间的友谊',
    imageUrl: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&h=600&fit=crop',
    date: '2024-01-05',
    location: '现实世界',
    participants: 15,
    likes: 35,
    category: 'social'
  },
  {
    id: 4,
    title: '成就解锁',
    description: '公会成员解锁稀有成就的激动时刻',
    imageUrl: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&h=600&fit=crop',
    date: '2024-01-01',
    location: '艾泽拉斯',
    participants: 8,
    likes: 19,
    category: 'achievement'
  },
  {
    id: 5,
    title: 'H7开荒',
    description: '公会开始H7副本开荒，团队配合默契',
    imageUrl: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&h=600&fit=crop',
    date: '2023-12-28',
    location: '艾泽拉斯',
    participants: 30,
    likes: 56,
    category: 'raid'
  },
  {
    id: 6,
    title: '世界BOSS战',
    description: '公会组织世界BOSS战，展现团队实力',
    imageUrl: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&h=600&fit=crop',
    date: '2023-12-25',
    location: '艾泽拉斯',
    participants: 40,
    likes: 67,
    category: 'raid'
  }
]

const categories = [
  { id: 'all', name: '全部', count: galleryData.length },
  { id: 'raid', name: '副本', count: galleryData.filter(item => item.category === 'raid').length },
  { id: 'pvp', name: 'PVP', count: galleryData.filter(item => item.category === 'pvp').length },
  { id: 'social', name: '社交', count: galleryData.filter(item => item.category === 'social').length },
  { id: 'achievement', name: '成就', count: galleryData.filter(item => item.category === 'achievement').length },
]

export default function GalleryPage() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedImage, setSelectedImage] = useState<GalleryItem | null>(null)

  const filteredData = selectedCategory === 'all' 
    ? galleryData 
    : galleryData.filter(item => item.category === selectedCategory)

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'raid': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
      case 'pvp': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
      case 'social': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      case 'achievement': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
    }
  }

  const getCategoryName = (category: string) => {
    switch (category) {
      case 'raid': return '副本'
      case 'pvp': return 'PVP'
      case 'social': return '社交'
      case 'achievement': return '成就'
      default: return '其他'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                公会画廊
              </h1>
              <p className="mt-2 text-gray-600 dark:text-gray-300">
                记录公会精彩瞬间和美好回忆
              </p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
              <Image className="h-5 w-5" />
              <span>{galleryData.length} 张照片</span>
            </div>
          </div>
        </div>

        {/* Category Filter */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  selectedCategory === category.id
                    ? 'bg-primary-600 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-600'
                }`}
              >
                {category.name} ({category.count})
              </button>
            ))}
          </div>
        </div>

        {/* Gallery Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <AnimatePresence>
            {filteredData.map((item, index) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => setSelectedImage(item)}
              >
                <div className="relative">
                  <img
                    src={item.imageUrl}
                    alt={item.title}
                    className="w-full h-48 object-cover"
                  />
                  <div className="absolute top-2 right-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(item.category)}`}>
                      {getCategoryName(item.category)}
                    </span>
                  </div>
                </div>
                <div className="p-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {item.title}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                    {item.description}
                  </p>
                  <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-1">
                        <Calendar className="h-4 w-4" />
                        <span>{formatDate(item.date)}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <MapPin className="h-4 w-4" />
                        <span>{item.location}</span>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="flex items-center space-x-1">
                        <Users className="h-4 w-4" />
                        <span>{item.participants}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Heart className="h-4 w-4" />
                        <span>{item.likes}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {/* Empty State */}
        {filteredData.length === 0 && (
          <div className="text-center py-12">
            <Image className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">暂无照片</h3>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              该分类下暂时没有照片
            </p>
          </div>
        )}
      </div>

      {/* Image Modal */}
      <AnimatePresence>
        {selectedImage && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-75"
            onClick={() => setSelectedImage(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="relative max-w-4xl max-h-full bg-white dark:bg-gray-800 rounded-lg overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="relative">
                <img
                  src={selectedImage.imageUrl}
                  alt={selectedImage.title}
                  className="w-full h-auto max-h-[70vh] object-contain"
                />
                <button
                  onClick={() => setSelectedImage(null)}
                  className="absolute top-4 right-4 p-2 bg-black bg-opacity-50 text-white rounded-full hover:bg-opacity-75 transition-colors"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                      {selectedImage.title}
                    </h2>
                    <p className="text-gray-600 dark:text-gray-400">
                      {selectedImage.description}
                    </p>
                  </div>
                  <div className="flex space-x-2">
                    <button className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors">
                      <Share2 className="h-5 w-5" />
                    </button>
                    <button className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors">
                      <Download className="h-5 w-5" />
                    </button>
                  </div>
                </div>
                <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
                  <div className="flex items-center space-x-6">
                    <div className="flex items-center space-x-1">
                      <Calendar className="h-4 w-4" />
                      <span>{formatDate(selectedImage.date)}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <MapPin className="h-4 w-4" />
                      <span>{selectedImage.location}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Users className="h-4 w-4" />
                      <span>{selectedImage.participants} 人参与</span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Heart className="h-4 w-4" />
                    <span>{selectedImage.likes} 个赞</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
} 