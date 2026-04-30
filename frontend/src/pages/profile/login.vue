<template>
  <view class="container">
    <view class="login-header">
      <image class="logo" src="/static/images/logo.png" mode="aspectFit" />
      <text class="title">中医学习</text>
      <text class="subtitle">登录后开始您的中医学习之旅</text>
    </view>

    <view class="login-form">
      <!-- 手机号登录 -->
      <view class="form-item">
        <text class="label">手机号</text>
        <input
          class="input"
          type="number"
          v-model="phone"
          placeholder="请输入手机号"
          maxlength="11"
        />
      </view>

      <view class="form-item">
        <text class="label">验证码</text>
        <view class="code-input">
          <input
            class="input"
            type="number"
            v-model="code"
            placeholder="请输入验证码"
            maxlength="8"
          />
          <button
            class="code-btn"
            :disabled="countdown > 0"
            @click="sendCode"
          >
            {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
          </button>
        </view>
      </view>

      <button class="login-btn" @click="login">登录</button>

      <view class="divider">
        <view class="line"></view>
        <text class="text">其他登录方式</text>
        <view class="line"></view>
      </view>

      <button class="wechat-btn" @click="loginWithWechat">
        <text class="wechat-icon">微信</text>
        <text>微信一键登录</text>
      </button>
    </view>

    <view class="agreement" @click="agreed = !agreed">
      <checkbox-group @change="onAgreementChange">
        <checkbox value="agreed" :checked="agreed" />
      </checkbox-group>
      <text class="agreement-text">
        我已阅读并同意
        <text class="link">《用户协议》</text>
        和
        <text class="link">《隐私政策》</text>
      </text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { authApi } from '@/api';

const authStore = useAuthStore();

const phone = ref('');
const code = ref('');
const countdown = ref(0);
const agreed = ref(false);

let timer: number | null = null;

function startCountdown() {
  countdown.value = 60;
  timer = setInterval(() => {
    countdown.value--;
    if (countdown.value <= 0) {
      clearInterval(timer!);
    }
  }, 1000);
}

async function sendCode() {
  if (!phone.value || phone.value.length !== 11) {
    uni.showToast({ title: '请输入正确的手机号', icon: 'none' });
    return;
  }
  try {
    await authApi.sendCode(phone.value);
    uni.showToast({ title: '验证码已发送', icon: 'success' });
    startCountdown();
  } catch (e) {
    uni.showToast({ title: '发送失败', icon: 'none' });
  }
}

async function login() {
  if (!agreed.value) {
    uni.showToast({ title: '请同意用户协议', icon: 'none' });
    return;
  }
  if (!phone.value || !code.value) {
    uni.showToast({ title: '请填写完整信息', icon: 'none' });
    return;
  }
  try {
    const res: any = await authApi.loginPhone(phone.value, code.value);
    authStore.setToken(res.access_token);
    authStore.setUser(res.user);
    uni.showToast({ title: '登录成功', icon: 'success' });
    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' });
    }, 1500);
  } catch (e) {
    uni.showToast({ title: '登录失败', icon: 'none' });
  }
}

function onAgreementChange(e: any) {
  agreed.value = e.detail.value.includes('agreed');
}

function loginWithWechat() {
  if (!agreed.value) {
    uni.showToast({ title: '请同意用户协议', icon: 'none' });
    return;
  }
  uni.showToast({ title: '微信登录暂未实现', icon: 'none' });
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #fff;
  padding: 60rpx 48rpx;
}

.login-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 80rpx;

  .logo {
    width: 160rpx;
    height: 160rpx;
    margin-bottom: 32rpx;
  }

  .title {
    font-size: 48rpx;
    font-weight: bold;
    color: #2B9939;
    margin-bottom: 16rpx;
  }

  .subtitle {
    font-size: 28rpx;
    color: #999;
  }
}

.login-form {
  .form-item {
    margin-bottom: 32rpx;

    .label {
      display: block;
      font-size: 28rpx;
      color: #333;
      margin-bottom: 16rpx;
    }

    .input {
      height: 88rpx;
      background: #f5f5f5;
      border-radius: 16rpx;
      padding: 0 24rpx;
      font-size: 28rpx;
    }
  }

  .code-input {
    display: flex;
    gap: 24rpx;

    .input {
      flex: 1;
    }

    .code-btn {
      width: 200rpx;
      height: 88rpx;
      background: #2B9939;
      color: #fff;
      border-radius: 16rpx;
      font-size: 24rpx;

      &[disabled] {
        background: #ccc;
      }
    }
  }

  .login-btn {
    height: 96rpx;
    background: #2B9939;
    color: #fff;
    border-radius: 48rpx;
    font-size: 32rpx;
    margin-top: 48rpx;
  }

  .divider {
    display: flex;
    align-items: center;
    margin: 48rpx 0;
    gap: 24rpx;

    .line {
      flex: 1;
      height: 2rpx;
      background: #e0e0e0;
    }

    .text {
      font-size: 24rpx;
      color: #999;
    }
  }

  .wechat-btn {
    height: 96rpx;
    background: #07C160;
    color: #fff;
    border-radius: 48rpx;
    font-size: 32rpx;
    gap: 16rpx;

    .wechat-icon {
      font-size: 32rpx;
    }
  }
}

.agreement {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 48rpx;
  gap: 8rpx;

  .agreement-text {
    font-size: 24rpx;
    color: #999;
  }

  .link {
    color: #2B9939;
  }
}
</style>
