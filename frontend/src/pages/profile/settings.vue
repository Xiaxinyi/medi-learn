<template>
  <view class="container">
    <view class="menu-list">
      <view class="menu-item" @click="editProfile">
        <text class="menu-icon">👤</text>
        <text class="menu-text">编辑资料</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item" @click="changePassword">
        <text class="menu-icon">🔒</text>
        <text class="menu-text">修改密码</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item" @click="clearCache">
        <text class="menu-icon">🗑️</text>
        <text class="menu-text">清除缓存</text>
        <text class="menu-arrow">></text>
      </view>
    </view>

    <view class="menu-list">
      <view class="menu-item" @click="showPrivacy">
        <text class="menu-icon">📋</text>
        <text class="menu-text">隐私政策</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item" @click="showTerms">
        <text class="menu-icon">📄</text>
        <text class="menu-text">用户协议</text>
        <text class="menu-arrow">></text>
      </view>
    </view>

    <view class="version-info">
      <text>版本 1.0.0</text>
    </view>
  </view>
</template>

<script setup lang="ts">
function editProfile() {
  uni.showToast({ title: '编辑资料', icon: 'none' });
}

function changePassword() {
  uni.showToast({ title: '修改密码', icon: 'none' });
}

function clearCache() {
  uni.showModal({
    title: '提示',
    content: '确定要清除缓存吗？',
    success: (res) => {
      if (res.confirm) {
        uni.clearStorageSync();
        uni.showToast({ title: '缓存已清除', icon: 'success' });
      }
    },
  });
}

function showPrivacy() {
  uni.showModal({
    title: '隐私政策',
    content: '我们重视您的隐私保护...',
    showCancel: false,
  });
}

function showTerms() {
  uni.showModal({
    title: '用户协议',
    content: '欢迎使用中医学习小程序...',
    showCancel: false,
  });
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 24rpx;
}

.menu-list {
  background: #fff;
  border-radius: 24rpx;
  overflow: hidden;
  margin-bottom: 24rpx;

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

.version-info {
  text-align: center;
  padding: 48rpx;
  font-size: 26rpx;
  color: #999;
}
</style>
