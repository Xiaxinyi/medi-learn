const BASE_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:8000'
  : 'https://medi-learn-backend.onrender.com';

interface RequestOptions {
  url: string;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  data?: any;
  params?: any;
  header?: Record<string, string>;
}

function buildUrl(url: string, params?: any): string {
  if (!params) return url;
  const query = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null)
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
    .join('&');
  return query ? `${url}?${query}` : url;
}

export function request<T = any>(options: RequestOptions): Promise<T> {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token');
    const header: Record<string, string> = {
      'Content-Type': 'application/json',
      ...options.header,
    };
    if (token) {
      header['Authorization'] = `Bearer ${token}`;
    }

    const url = buildUrl(`${BASE_URL}${options.url}`, options.params);

    uni.request({
      url,
      method: options.method || 'GET',
      data: options.data,
      header,
      success: (res: any) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          if (res.statusCode === 401) {
            uni.removeStorageSync('token');
            uni.showToast({ title: '登录已过期', icon: 'none' });
          }
          reject(res.data);
        }
      },
      fail: (err: any) => {
        uni.showToast({ title: '网络错误', icon: 'none' });
        reject(err);
      },
    });
  });
}

export const api = {
  get: <T = any>(url: string, params?: any) => request<T>({ url, method: 'GET', params }),
  post: <T = any>(url: string, data?: any, params?: any) => request<T>({ url, method: 'POST', data, params }),
  put: <T = any>(url: string, data?: any) => request<T>({ url, method: 'PUT', data }),
  del: <T = any>(url: string) => request<T>({ url, method: 'DELETE' }),
};
