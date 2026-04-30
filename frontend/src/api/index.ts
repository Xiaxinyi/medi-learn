import { api } from '@/utils/request';
import type {
  User, Question, Herb, Formula, ExamResult,
  Feedback, LevelConfig, ExperienceLog, PageResult,
} from '@/types';

// 认证
export const authApi = {
  sendCode: (phone: string) => api.post('/api/auth/send-code', { phone }),
  loginPhone: (phone: string, code: string) => api.post('/api/auth/login-phone', { phone, code }),
  loginWechat: (code: string) => api.post('/api/auth/login-wechat', { code }),
  getProfile: () => api.get<User>('/api/auth/profile'),
};

// 草药
export const herbApi = {
  list: (params?: any) => api.get<PageResult<Herb>>('/api/herbs/', params),
  detail: (id: string) => api.get<Herb>(`/api/herbs/${id}`),
  create: (data: any) => api.post('/api/herbs', data),
  update: (id: string, data: any) => api.put(`/api/herbs/${id}`, data),
  delete: (id: string) => api.del(`/api/herbs/${id}`),
  favorite: (id: string) => api.post(`/api/herbs/${id}/favorite`),
  unfavorite: (id: string) => api.del(`/api/herbs/${id}/favorite`),
  generate: (name: string) => api.post('/api/herbs/generate', null, { name }),
};

// 题库
export const questionApi = {
  list: (params?: any) => api.get<PageResult<Question>>('/api/questions', params),
  detail: (id: string) => api.get<Question>(`/api/questions/${id}`),
  random: (count: number = 10) => api.get<Question[]>('/api/questions/random', { count }),
  create: (data: any) => api.post('/api/questions', data),
  update: (id: string, data: any) => api.put(`/api/questions/${id}`, data),
  delete: (id: string) => api.del(`/api/questions/${id}`),
};

// 考试
export const examApi = {
  generate: (data: any) => api.post('/api/exams/generate', data),
  submit: (data: any) => api.post('/api/exams/submit', data),
  results: () => api.get<ExamResult[]>('/api/exams/results'),
  practice: () => api.get<Question[]>('/api/exams/practice'),
};

// 方剂
export const formulaApi = {
  list: (params?: any) => api.get<PageResult<Formula>>('/api/formulas', params),
  detail: (id: string) => api.get<Formula>(`/api/formulas/${id}`),
  byHerb: (herbId: string) => api.get<Formula[]>(`/api/formulas/by-herb/${herbId}`),
  create: (data: any) => api.post('/api/formulas', data),
  update: (id: string, data: any) => api.put(`/api/formulas/${id}`, data),
  delete: (id: string) => api.del(`/api/formulas/${id}`),
};

// 反馈
export const feedbackApi = {
  create: (data: any) => api.post('/api/feedback', data),
  myList: () => api.get<Feedback[]>('/api/feedback/my'),
};

// 等级
export const levelApi = {
  list: () => api.get<LevelConfig[]>('/api/levels'),
  myLevel: () => api.get('/api/levels/my'),
  logs: () => api.get<ExperienceLog[]>('/api/levels/experience-logs'),
  leaderboard: () => api.get('/api/levels/leaderboard'),
};

// 统计
export const statsApi = {
  overview: () => api.get('/api/stats/overview'),
  daily: () => api.get('/api/stats/daily'),
  trend: () => api.get('/api/stats/trend'),
  accuracy: () => api.get('/api/stats/accuracy'),
};

// 管理员
export const adminApi = {
  listUsers: (params?: any) => api.get<any[]>('/api/admin/users', params),
  createUser: (data: any) => api.post('/api/admin/users', data),
  updateUserRole: (id: number, data: any) => api.put(`/api/admin/users/${id}/role`, data),
  updateUserStatus: (id: number, data: any) => api.put(`/api/admin/users/${id}/status`, data),

};

// 上传
export const uploadApi = {
  image: (filePath: string) => {
    return new Promise((resolve, reject) => {
      uni.uploadFile({
        url: 'http://localhost:8000/api/upload/image',
        filePath,
        name: 'file',
        header: {
          Authorization: `Bearer ${uni.getStorageSync('token')}`,
        },
        success: (res: any) => resolve(JSON.parse(res.data)),
        fail: reject,
      });
    });
  },
};
