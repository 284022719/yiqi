import { Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import Layout from '@/components/Layout'
import LoadingSpinner from '@/components/LoadingSpinner'

// 懒加载页面组件
const HomePage = lazy(() => import('@/pages/HomePage'))
const MembersPage = lazy(() => import('@/pages/MembersPage'))
const StatisticsPage = lazy(() => import('@/pages/StatisticsPage'))
const GalleryPage = lazy(() => import('@/pages/GalleryPage'))
const H6Page = lazy(() => import('@/pages/H6Page'))
const H7Page = lazy(() => import('@/pages/H7Page'))
const NotFoundPage = lazy(() => import('@/pages/NotFoundPage'))

function App() {
  return (
    <Layout>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/members" element={<MembersPage />} />
          <Route path="/statistics" element={<StatisticsPage />} />
          <Route path="/gallery" element={<GalleryPage />} />
          <Route path="/h6" element={<H6Page />} />
          <Route path="/h7" element={<H7Page />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </Layout>
  )
}

export default App 