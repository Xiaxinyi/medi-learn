import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '@/types';

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string>(uni.getStorageSync('token') || '');
  const user = ref<User | null>(null);

  const isLoggedIn = computed(() => !!token.value);
  const isAdmin = computed(() => user.value?.role === 'admin');

  function setToken(newToken: string) {
    token.value = newToken;
    uni.setStorageSync('token', newToken);
  }

  function setUser(newUser: User) {
    user.value = newUser;
    uni.setStorageSync('user', JSON.stringify(newUser));
  }

  function logout() {
    token.value = '';
    user.value = null;
    uni.removeStorageSync('token');
    uni.removeStorageSync('user');
  }

  function loadUserFromStorage() {
    const stored = uni.getStorageSync('user');
    if (stored) {
      try {
        user.value = JSON.parse(stored);
      } catch {
        user.value = null;
      }
    }
  }

  return {
    token,
    user,
    isLoggedIn,
    isAdmin,
    setToken,
    setUser,
    logout,
    loadUserFromStorage,
  };
});
