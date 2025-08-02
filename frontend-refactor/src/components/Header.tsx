import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Sun, Moon } from 'lucide-react'
import { cn } from '@/utils'

const navigation = [
  { name: '首页', href: '/' },
  { name: '公会成员', href: '/members' },
  { name: '统计数据', href: '/statistics' },
  { name: '图片画廊', href: '/gallery' },
  { name: 'H6攻略', href: '/h6' },
  { name: 'H7攻略', href: '/h7' },
]

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [darkMode, setDarkMode] = useState(false)
  const location = useLocation()

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
    document.documentElement.classList.toggle('dark')
  }

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <nav className="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
        <div className="flex lg:flex-1">
          <Link to="/" className="-m-1.5 p-1.5">
            <span className="sr-only">易骑公会</span>
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">易</span>
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">易骑公会</span>
            </div>
          </Link>
        </div>
        
        <div className="flex lg:hidden">
          <button
            type="button"
            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700 dark:text-gray-300"
            onClick={() => setMobileMenuOpen(true)}
          >
            <span className="sr-only">打开主菜单</span>
            <Menu className="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
        
        <div className="hidden lg:flex lg:gap-x-12">
          {navigation.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className={cn(
                'text-sm font-semibold leading-6 transition-colors',
                location.pathname === item.href
                  ? 'text-primary-600 dark:text-primary-400'
                  : 'text-gray-900 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400'
              )}
            >
              {item.name}
            </Link>
          ))}
        </div>
        
        <div className="hidden lg:flex lg:flex-1 lg:justify-end lg:gap-x-4">
          <button
            onClick={toggleDarkMode}
            className="p-2 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>
        </div>
      </nav>
      
      {/* 移动端菜单 */}
      {mobileMenuOpen && (
        <div className="lg:hidden">
          <div className="fixed inset-0 z-50" />
          <div className="fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-white dark:bg-gray-800 px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
            <div className="flex items-center justify-between">
              <Link to="/" className="-m-1.5 p-1.5">
                <span className="sr-only">易骑公会</span>
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-lg flex items-center justify-center">
                    <span className="text-white font-bold text-sm">易</span>
                  </div>
                  <span className="text-xl font-bold text-gray-900 dark:text-white">易骑公会</span>
                </div>
              </Link>
              <button
                type="button"
                className="-m-2.5 rounded-md p-2.5 text-gray-700 dark:text-gray-300"
                onClick={() => setMobileMenuOpen(false)}
              >
                <span className="sr-only">关闭菜单</span>
                <X className="h-6 w-6" aria-hidden="true" />
              </button>
            </div>
            <div className="mt-6 flow-root">
              <div className="-my-6 divide-y divide-gray-500/10">
                <div className="space-y-2 py-6">
                  {navigation.map((item) => (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={cn(
                        '-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 transition-colors',
                        location.pathname === item.href
                          ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20'
                          : 'text-gray-900 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                      )}
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      {item.name}
                    </Link>
                  ))}
                </div>
                <div className="py-6">
                  <button
                    onClick={toggleDarkMode}
                    className="flex w-full items-center space-x-2 rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                  >
                    {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
                    <span>{darkMode ? '浅色模式' : '深色模式'}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </header>
  )
} 