/**
 * عميل API - axios مع JWT
 */
import axios from 'axios';
import { useAuthStore } from './auth';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: { 'Content-Type': 'application/json' },
});

// إضافة الـ token تلقائياً
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// التعامل مع انتهاء الجلسة
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// === Auth ===
export const authApi = {
  register: (data: { email: string; full_name: string; phone?: string; password: string }) =>
    api.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
  me: () => api.get('/users/me'),
};

// === MT5 ===
export const mt5Api = {
  connect: (data: { login: string; password: string; server: string; nickname?: string }) =>
    api.post('/mt5/connect', data),
  listAccounts: () => api.get('/mt5/accounts'),
  getInfo: (accountId: string) => api.get(`/mt5/${accountId}/info`),
  getPositions: (accountId: string) => api.get(`/mt5/${accountId}/positions`),
  trade: (accountId: string, data: any) => api.post(`/mt5/${accountId}/trade`, data),
  closePosition: (accountId: string, ticket: number) =>
    api.delete(`/mt5/${accountId}/positions/${ticket}`),
  getHistory: (accountId: string, days = 30) =>
    api.get(`/mt5/${accountId}/history?days=${days}`),
  disconnect: (accountId: string) => api.delete(`/mt5/${accountId}`),
};

// === Analytics ===
export const analyticsApi = {
  getPerformance: (accountId: string, days = 30) =>
    api.get(`/analytics/${accountId}/performance?days=${days}`),
};
