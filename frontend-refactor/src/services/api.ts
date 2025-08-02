import axios, { AxiosInstance, AxiosResponse } from 'axios'
import { 
  GuildMember, 
  Statistics, 
  ClassDistribution, 
  RealmDistribution, 
  SearchResponse, 
  SearchParams,
  PaginatedResponse,
  ApiError,
  MythicPlusStats
} from '@/types'

// 创建axios实例
const api: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token等
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error) => {
    const apiError: ApiError = {
      message: error.response?.data?.message || error.message || '网络错误',
      status: error.response?.status || 500,
      code: error.response?.data?.code,
      details: error.response?.data,
    }
    return Promise.reject(apiError)
  }
)

// 公会成员API
export const membersApi = {
  // 获取所有成员
  getAll: async (params: {
    page?: number
    size?: number
    search?: string
    class_name?: string
    faction?: string
  } = {}): Promise<PaginatedResponse<GuildMember>> => {
    const response = await api.get('/members', { params })
    return response.data
  },

  // 获取单个成员
  getById: async (id: number): Promise<GuildMember> => {
    const response = await api.get(`/members/${id}`)
    return response.data
  },

  // 按名称和服务器搜索成员
  getByNameAndRealm: async (name: string, realm: string): Promise<GuildMember> => {
    const response = await api.get(`/members/search/${name}/${realm}`)
    return response.data
  },

  // 创建成员
  create: async (member: Omit<GuildMember, 'id' | 'created_at' | 'updated_at'>): Promise<GuildMember> => {
    const response = await api.post('/members', member)
    return response.data
  },

  // 更新成员
  update: async (id: number, member: Partial<GuildMember>): Promise<GuildMember> => {
    const response = await api.put(`/members/${id}`, member)
    return response.data
  },

  // 删除成员
  delete: async (id: number): Promise<void> => {
    await api.delete(`/members/${id}`)
  },

  // 获取可用职业
  getClasses: async (): Promise<string[]> => {
    const response = await api.get('/members/classes')
    return response.data
  },

  // 获取可用服务器
  getRealms: async (): Promise<string[]> => {
    const response = await api.get('/members/realms')
    return response.data
  },
}

// 统计API
export const statisticsApi = {
  // 获取总览统计
  getOverview: async (): Promise<Statistics> => {
    const response = await api.get('/statistics/overview')
    return response.data
  },

  // 获取职业分布
  getClassDistribution: async (): Promise<ClassDistribution[]> => {
    const response = await api.get('/statistics/class-distribution')
    return response.data
  },

  // 获取服务器分布
  getRealmDistribution: async (): Promise<RealmDistribution[]> => {
    const response = await api.get('/statistics/realm-distribution')
    return response.data
  },

  // 获取等级分布
  getLevelDistribution: async (): Promise<any[]> => {
    const response = await api.get('/statistics/level-distribution')
    return response.data
  },

  // 获取Mythic+统计
  getMythicPlusStats: async (): Promise<MythicPlusStats> => {
    const response = await api.get('/statistics/mythic-plus-stats')
    return response.data
  },

  // 获取坐骑统计
  getMountStats: async (): Promise<any> => {
    const response = await api.get('/statistics/mount-stats')
    return response.data
  },

  // 获取在线统计
  getOnlineStats: async (): Promise<any> => {
    const response = await api.get('/statistics/online-stats')
    return response.data
  },
}

// 搜索API
export const searchApi = {
  // 成员搜索
  searchMembers: async (params: SearchParams): Promise<SearchResponse> => {
    const response = await api.get('/search/members', { params })
    return response.data
  },

  // 高级搜索
  advancedSearch: async (params: SearchParams): Promise<SearchResponse> => {
    const response = await api.get('/search/advanced', { params })
    return response.data
  },

  // 获取搜索建议
  getSuggestions: async (query: string): Promise<string[]> => {
    const response = await api.get('/search/suggestions', { params: { q: query } })
    return response.data
  },

  // 获取热门搜索
  getPopularSearches: async (): Promise<string[]> => {
    const response = await api.get('/search/popular-searches')
    return response.data
  },
}

// 爬虫API
export const crawlerApi = {
  // 更新单个成员数据
  updateMemberData: async (name: string, realm: string): Promise<void> => {
    await api.post('/crawler/update-member-data', { name, realm })
  },

  // 更新所有成员数据
  updateAllMembers: async (): Promise<void> => {
    await api.post('/crawler/update-all-members')
  },

  // 更新缺失数据
  updateMissingData: async (): Promise<void> => {
    await api.post('/crawler/update-missing-data')
  },
}

// 健康检查API
export const healthApi = {
  check: async (): Promise<{ status: string; timestamp: string }> => {
    const response = await api.get('/health')
    return response.data
  },
}

export default api 