<template>
  <view class="container">
    <view class="result-card">
      <text class="result-title">练习完成</text>
      <view class="score-circle">
        <text class="score-num">{{ score }}</text>
        <text class="score-label">分</text>
      </view>
      <view class="stats-row">
        <view class="stats-item">
          <text class="stats-num">{{ total }}</text>
          <text class="stats-label">总题数</text>
        </view>
        <view class="stats-item">
          <text class="stats-num">{{ correct }}</text>
          <text class="stats-label">正确</text>
        </view>
        <view class="stats-item">
          <text class="stats-num">{{ accuracy }}%</text>
          <text class="stats-label">正确率</text>
        </view>
      </view>
    </view>

    <view class="action-btns">
      <button class="btn-primary" @click="goPractice">再来一次</button>
      <button class="btn-secondary" @click="goHome">返回首页</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

const score = ref(0);
const total = ref(0);
const correct = ref(0);

const accuracy = computed(() => {
  if (total.value === 0) return 0;
  return Math.round((correct.value / total.value) * 100);
});

onMounted(() => {
  const pages = getCurrentPages();
  const current = pages[pages.length - 1] as any;
  const query = current?.$page?.options || {};
  score.value = Number(query.score) || 0;
  total.value = Number(query.total) || 0;
  correct.value = Number(query.correct) || 0;
});

function goPractice() {
  uni.redirectTo({ url: '/pages/quiz/practice' });
}

function goHome() {
  uni.switchTab({ url: '/pages/index/index' });
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 48rpx 32rpx;
}

.result-card {
  background: #fff;
  border-radius: 32rpx;
  padding: 64rpx 48rpx;
  text-align: center;
  margin-bottom: 48rpx;

  .result-title {
    font-size: 40rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 48rpx;
  }

  .score-circle {
    width: 240rpx;
    height: 240rpx;
    border-radius: 50%;
    background: linear-gradient(135deg, #2B9939, #1B7A2B);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto 48rpx;

    .score-num {
      font-size: 72rpx;
      font-weight: bold;
      color: #fff;
    }

    .score-label {
      font-size: 28rpx;
      color: rgba(255, 255, 255, 0.8);
    }
  }

  .stats-row {
    display: flex;
    justify-content: space-around;

    .stats-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12rpx;

      .stats-num {
        font-size: 40rpx;
        font-weight: bold;
        color: #2B9939;
      }

      .stats-label {
        font-size: 26rpx;
        color: #999;
      }
    }
  }
}

.action-btns {
  display: flex;
  flex-direction: column;
  gap: 24rpx;

  .btn-primary, .btn-secondary {
    height: 96rpx;
    border-radius: 48rpx;
    font-size: 32rpx;
    border: none;
  }

  .btn-primary {
    background: #2B9939;
    color: #fff;
  }

  .btn-secondary {
    background: #fff;
    color: #666;
  }
}
</style>
