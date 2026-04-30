<template>
  <view class="container">
    <!-- 用户信息卡片 -->
    <view class="user-card">
      <view class="user-info" @click="goLogin" v-if="!authStore.isLoggedIn">
        <view class="avatar-placeholder">
          <text>登录</text>
        </view>
        <view class="user-text">
          <text class="login-tip">点击登录/注册</text>
        </view>
      </view>
      <view class="user-info" v-else>
        <image class="avatar" :src="authStore.user?.avatarUrl || '/static/images/default-avatar.png'" mode="aspectFill" />
        <view class="user-text">
          <text class="nickname">{{ authStore.user?.nickname || '中医学习者' }}</text>
          <view class="level-badge" :style="{ backgroundColor: authStore.user?.levelColor || '#999' }">
            <text>Lv.{{ authStore.user?.level }} {{ authStore.user?.levelName }}</text>
          </view>
        </view>
        <view class="exp-bar">
          <view class="exp-progress" :style="{ width: `${authStore.user?.levelProgress || 0}%` }"></view>
          <text class="exp-text">{{ authStore.user?.experience }}/{{ authStore.user?.nextLevelExp }} EXP</text>
        </view>
      </view>
    </view>

    <!-- 学习统计 -->
    <view class="stats-grid" v-if="authStore.isLoggedIn">
      <view class="stats-item">
        <text class="stats-num">{{ stats.herbs }}</text>
        <text class="stats-label">学习草药</text>
      </view>
      <view class="stats-item">
        <text class="stats-num">{{ stats.questions }}</text>
        <text class="stats-label">答题数量</text>
      </view>
      <view class="stats-item">
        <text class="stats-num">{{ stats.correctRate }}%</text>
        <text class="stats-label">正确率</text>
      </view>
      <view class="stats-item">
        <text class="stats-num">{{ stats.streak }}</text>
        <text class="stats-label">连续天数</text>
      </view>
    </view>

    <!-- 管理员入口 -->
    <view class="menu-list" v-if="authStore.isAdmin">
      <view class="menu-item admin-item" @click="navigateTo('/pages/admin/users')">
        <text class="menu-icon">👤</text>
        <text class="menu-text">用户管理</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item admin-item" @click="navigateTo('/pages/admin/herbs')">
        <text class="menu-icon">🌿</text>
        <text class="menu-text">草药管理</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item admin-item" @click="navigateTo('/pages/admin/questions')">
        <text class="menu-icon">📝</text>
        <text class="menu-text">试题管理</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item admin-item" @click="navigateTo('/pages/admin/formulas')">
        <text class="menu-icon">📖</text>
        <text class="menu-text">方剂管理</text>
        <text class="menu-arrow">></text>
      </view>
    </view>

    <!-- 功能菜单 -->
    <view class="menu-list">
      <view class="menu-item" @click="navigateTo('/pages/herbs/list')">
        <text class="menu-icon">🌿</text>
        <text class="menu-text">我的收藏</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item" @click="navigateTo('/pages/wrongbook/list')">
        <text class="menu-icon">❌</text>
        <text class="menu-text">错题本</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item" @click="navigateTo('/pages/formulas/list')">
        <text class="menu-icon">📖</text>
        <text class="menu-text">方剂学习</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item" @click="navigateTo('/pages/feedback/index')">
        <text class="menu-icon">💬</text>
        <text class="menu-text">反馈建议</text>
        <text class="menu-arrow">></text>
      </view>
    </view>

    <!-- 设置菜单 -->
    <view class="menu-list">
      <view class="menu-item" @click="navigateTo('/pages/profile/settings')">
        <text class="menu-icon">⚙️</text>
        <text class="menu-text">设置</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item" @click="showAbout">
        <text class="menu-icon">ℹ️</text>
        <text class="menu-text">关于我们</text>
        <text class="menu-arrow">></text>
      </view>
    </view>

    <!-- 退出登录 -->
    <button class="logout-btn" v-if="authStore.isLoggedIn" @click="logout">退出登录</button>

    <!-- 调试面板 -->
    <view class="debug-panel" v-if="showDebug">
      <view class="debug-title" @click="debugExpanded = !debugExpanded">
        <text>调试面板</text>
        <text class="debug-arrow">{{ debugExpanded ? '▼' : '▶' }}</text>
      </view>
      <view v-if="debugExpanded" class="debug-body">
        <view class="debug-section">
          <text class="debug-label">用户信息</text>
          <text class="debug-item">id: {{ authStore.user?.id ?? '-' }}</text>
          <text class="debug-item">nickname: {{ authStore.user?.nickname ?? '-' }}</text>
          <text class="debug-item">role: {{ authStore.user?.role ?? '-' }}</text>
          <text class="debug-item">isAdmin: {{ authStore.isAdmin }}</text>
          <text class="debug-item">token: {{ authStore.token ? authStore.token.slice(0, 20) + '...' : '无' }}</text>
        </view>
        <view class="debug-section">
          <text class="debug-label">后端状态</text>
          <text class="debug-item" :class="{ 'debug-ok': backendStatus === '正常', 'debug-err': backendStatus !== '正常' }">
            {{ backendStatus }}
          </text>
        </view>
        <view class="debug-section">
          <text class="debug-label">本地存储</text>
          <text class="debug-item">user: {{ storedUser ? '有' : '无' }}</text>
          <text class="debug-item">token: {{ storedToken ? '有' : '无' }}</text>
        </view>
        <view class="debug-actions">
          <button class="debug-btn" @click="checkBackend">检测后端</button>
          <button class="debug-btn warn" @click="clearCache">清除缓存</button>
        </view>
      </view>
    </view>

    <!-- 点击版本号5次展开调试面板 -->
    <view class="version-tap" @click="onVersionTap">
      <text class="version-text">版本 1.0.0</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { authApi, statsApi, adminApi } from '@/api';

const authStore = useAuthStore();

const stats = ref({ herbs: 0, questions: 0, correctRate: 0, streak: 0 });

async function loadStats() {
  try {
    const res = await statsApi.overview();
    stats.value = {
      herbs: res.total_answered || 0,
      questions: res.correct_count || 0,
      correctRate: res.accuracy_rate || 0,
      streak: res.streak_days || 0,
    };
  } catch (e) {
    // 静默失败，保持默认值
  }
}

// 调试面板
const showDebug = ref(false);
const debugExpanded = ref(true);
const backendStatus = ref('未检测');
const storedUser = ref('');
const storedToken = ref('');
let versionTapCount = 0;
let versionTapTimer: any = null;

function goLogin() {
  uni.navigateTo({ url: '/pages/profile/login' });
}

function navigateTo(url: string) {
  uni.navigateTo({ url });
}

function showAbout() {
  uni.showModal({
    title: '关于中医学习',
    content: '版本：1.0.0\n传承中医文化，探索草药奥秘。',
    showCancel: false,
  });
}

function logout() {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        authStore.logout();
        uni.showToast({ title: '已退出登录', icon: 'success' });
      }
    },
  });
}

function loadStorageInfo() {
  storedUser.value = uni.getStorageSync('user') || '';
  storedToken.value = uni.getStorageSync('token') || '';
}

async function checkBackend() {
  backendStatus.value = '检测中...';
  try {
    await authApi.getProfile();
    backendStatus.value = '正常';
  } catch (e: any) {
    backendStatus.value = e.message || '异常';
  }
}

function clearCache() {
  uni.showModal({
    title: '确认清除',
    content: '确定要清除所有本地缓存吗？',
    success: (res) => {
      if (res.confirm) {
        uni.clearStorageSync();
        authStore.logout();
        uni.showToast({ title: '已清除', icon: 'success' });
        loadStorageInfo();
      }
    },
  });
}

function onVersionTap() {
  versionTapCount++;
  if (versionTapTimer) clearTimeout(versionTapTimer);
  versionTapTimer = setTimeout(() => {
    versionTapCount = 0;
  }, 2000);
  if (versionTapCount >= 5) {
    versionTapCount = 0;
    showDebug.value = !showDebug.value;
    if (showDebug.value) {
      loadStorageInfo();
      uni.showToast({ title: '调试面板已开启', icon: 'none' });
    }
  }
}

onMounted(() => {
  authStore.loadUserFromStorage();
  loadStorageInfo();
  loadStats();
});
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 40rpx;
}

.user-card {
  background: linear-gradient(135deg, #2B9939, #1B7A2B);
  padding: 60rpx 48rpx 48rpx;

  .user-info {
    display: flex;
    align-items: center;
    gap: 24rpx;
    position: relative;
  }

  .avatar-placeholder {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 32rpx;
  }

  .avatar {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    border: 4rpx solid rgba(255, 255, 255, 0.3);
  }

  .user-text {
    flex: 1;
  }

  .login-tip {
    font-size: 32rpx;
    color: #fff;
  }

  .nickname {
    font-size: 36rpx;
    font-weight: bold;
    color: #fff;
    display: block;
    margin-bottom: 12rpx;
  }

  .level-badge {
    display: inline-block;
    padding: 6rpx 20rpx;
    border-radius: 24rpx;
    font-size: 22rpx;
    color: #fff;
  }

  .exp-bar {
    position: absolute;
    bottom: -32rpx;
    left: 0;
    right: 0;
    height: 16rpx;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 8rpx;
    overflow: hidden;

    .exp-progress {
      height: 100%;
      background: #FFD700;
      border-radius: 8rpx;
      transition: width 0.3s;
    }

    .exp-text {
      position: absolute;
      top: 20rpx;
      right: 0;
      font-size: 20rpx;
      color: rgba(255, 255, 255, 0.8);
    }
  }
}

.stats-grid {
  display: flex;
  justify-content: space-around;
  background: #fff;
  margin: 48rpx 24rpx 24rpx;
  border-radius: 24rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);

  .stats-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8rpx;
  }

  .stats-num {
    font-size: 40rpx;
    font-weight: bold;
    color: #2B9939;
  }

  .stats-label {
    font-size: 24rpx;
    color: #999;
  }
}

.menu-list {
  background: #fff;
  margin: 0 24rpx 24rpx;
  border-radius: 24rpx;
  overflow: hidden;

  .menu-item {
    display: flex;
    align-items: center;
    padding: 32rpx;
    border-bottom: 2rpx solid #f5f5f5;

    &:last-child {
      border-bottom: none;
    }

    .menu-icon {
      font-size: 40rpx;
      margin-right: 20rpx;
    }

    .menu-text {
      flex: 1;
      font-size: 30rpx;
      color: #333;
    }

    .menu-arrow {
      font-size: 28rpx;
      color: #ccc;
    }

    &.admin-item {
      background: #FFF8F0;

      .menu-text {
        color: #E67E22;
        font-weight: bold;
      }
    }
  }
}

.logout-btn {
  margin: 48rpx 24rpx;
  height: 96rpx;
  background: #fff;
  color: #F44336;
  border-radius: 48rpx;
  font-size: 32rpx;
}

.version-tap {
  text-align: center;
  padding: 24rpx;

  .version-text {
    font-size: 24rpx;
    color: #bbb;
  }
}

.debug-panel {
  background: #fff;
  margin: 24rpx;
  border-radius: 24rpx;
  overflow: hidden;
  border: 2rpx solid #eee;

  .debug-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24rpx 32rpx;
    background: #fafafa;
    font-size: 28rpx;
    color: #666;
    font-weight: bold;

    .debug-arrow {
      font-size: 24rpx;
      color: #999;
    }
  }

  .debug-body {
    padding: 24rpx 32rpx;
  }

  .debug-section {
    margin-bottom: 20rpx;

    .debug-label {
      display: block;
      font-size: 26rpx;
      color: #333;
      font-weight: bold;
      margin-bottom: 8rpx;
    }

    .debug-item {
      display: block;
      font-size: 24rpx;
      color: #666;
      font-family: monospace;
      word-break: break-all;
      line-height: 1.6;

      &.debug-ok {
        color: #2B9939;
      }

      &.debug-err {
        color: #F44336;
      }
    }
  }

  .debug-actions {
    display: flex;
    gap: 24rpx;
    margin-top: 24rpx;

    .debug-btn {
      flex: 1;
      height: 72rpx;
      background: #2B9939;
      color: #fff;
      border-radius: 12rpx;
      font-size: 26rpx;

      &.warn {
        background: #F44336;
      }
    }
  }
}

.modal-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;

  .modal-content {
    width: 80%;
    background: #fff;
    border-radius: 24rpx;
    padding: 48rpx;

    .modal-title {
      display: block;
      font-size: 34rpx;
      font-weight: bold;
      color: #333;
      text-align: center;
      margin-bottom: 32rpx;
    }

    .modal-btn {
      width: 100%;
      height: 80rpx;
      border-radius: 16rpx;
      font-size: 30rpx;
      margin-top: 24rpx;

      &.cancel {
        background: #f5f5f5;
        color: #666;
      }
    }
  }

}
</style>
