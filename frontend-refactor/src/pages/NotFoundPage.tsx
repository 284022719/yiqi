import { Link } from 'react-router-dom'
import { Home, ArrowLeft } from 'lucide-react'

export default function NotFoundPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
      <div className="text-center">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-gray-200 dark:text-gray-700">404</h1>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mt-4">
            页面未找到
          </h2>
          <p className="text-gray-600 dark:text-gray-300 mt-2">
            抱歉，您访问的页面不存在或已被移除。
          </p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/"
            className="btn-primary btn-md inline-flex items-center"
          >
            <Home className="mr-2 h-4 w-4" />
            返回首页
          </Link>
          <button
            onClick={() => window.history.back()}
            className="btn-outline btn-md inline-flex items-center"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            返回上页
          </button>
        </div>
      </div>
    </div>
  )
} 