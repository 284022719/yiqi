import { Link } from 'react-router-dom'
import { Heart, Github, Mail } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
      <div className="mx-auto max-w-7xl px-6 py-12 md:flex md:items-center md:justify-between lg:px-8">
        <div className="flex justify-center space-x-6 md:order-2">
          <a
            href="https://github.com/yiqi-guild"
            className="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
            target="_blank"
            rel="noopener noreferrer"
          >
            <span className="sr-only">GitHub</span>
            <Github className="h-6 w-6" />
          </a>
          <a
            href="mailto:contact@yiqi-guild.com"
            className="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
          >
            <span className="sr-only">Email</span>
            <Mail className="h-6 w-6" />
          </a>
        </div>
        <div className="mt-8 md:order-1 md:mt-0">
          <p className="text-center text-xs leading-5 text-gray-500 dark:text-gray-400">
            &copy; 2025 易骑公会. 用{' '}
            <Heart className="inline h-4 w-4 text-red-500" />{' '}
            制作
          </p>
          <div className="mt-2 flex justify-center space-x-6 text-xs text-gray-500 dark:text-gray-400">
            <Link to="/privacy" className="hover:text-gray-900 dark:hover:text-gray-300">
              隐私政策
            </Link>
            <Link to="/terms" className="hover:text-gray-900 dark:hover:text-gray-300">
              使用条款
            </Link>
            <Link to="/about" className="hover:text-gray-900 dark:hover:text-gray-300">
              关于我们
            </Link>
          </div>
        </div>
      </div>
    </footer>
  )
} 