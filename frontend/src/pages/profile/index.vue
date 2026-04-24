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
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const stats = ref({ herbs: 12, questions: 86, correctRate: 78, streak: 5 });

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

onMounted(() => {
  authStore.loadUserFromStorage();
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
  }
}

.logout-btn {
  margin: 48rpx 24rpx;
  height: 96rpx;
  line-height: 96rpx;
  background: #fff;
  color: #F44336;
  border-radius: 48rpx;
  font-size: 32rpx;
}
</style>
