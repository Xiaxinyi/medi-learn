<template>
  <view class="container">
    <view class="header">
      <view class="stat-card">
        <text class="stat-num">{{ wrongList.length }}</text>
        <text class="stat-label">错题总数</text>
      </view>
      <view class="stat-card">
        <text class="stat-num">{{ masteredCount }}</text>
        <text class="stat-label">已掌握</text>
      </view>
      <view class="stat-card">
        <text class="stat-num">{{ unmasteredCount }}</text>
        <text class="stat-label">待复习</text>
      </view>
    </view>

    <view class="filter-bar">
      <view
        class="filter-item"
        :class="{ active: filter === 'all' }"
        @click="filter = 'all'"
      >
        全部
      </view>
      <view
        class="filter-item"
        :class="{ active: filter === 'unmastered' }"
        @click="filter = 'unmastered'"
      >
        未掌握
      </view>
      <view
        class="filter-item"
        :class="{ active: filter === 'mastered' }"
        @click="filter = 'mastered'"
      >
        已掌握
      </view>
    </view>

    <scroll-view class="wrong-list" scroll-y>
      <view
        class="wrong-item"
        v-for="item in filteredList"
        :key="item.id"
      >
        <view class="question-content">{{ item.questionContent }}</view>
        <view class="answer-info">
          <text class="wrong-answer">你的答案：{{ item.userAnswers.join('、') }}</text>
          <text class="correct-answer">正确答案：{{ item.correctAnswers.join('、') }}</text>
        </view>
        <view class="wrong-count">
          <text>错误 {{ item.wrongCount }} 次</text>
          <text class="master-btn" v-if="!item.isMastered" @click="markMastered(item.id)">
            标记已掌握
          </text>
          <text class="mastered-tag" v-else>已掌握</text>
        </view>
      </view>

      <view class="empty" v-if="filteredList.length === 0">
        <text>暂无错题记录</text>
      </view>
    </scroll-view>

    <view class="bottom-bar">
      <button class="review-btn" @click="startReview">开始错题重练</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface WrongItem {
  id: string;
  questionId: string;
  questionContent: string;
  userAnswers: string[];
  correctAnswers: string[];
  wrongCount: number;
  isMastered: boolean;
}

const filter = ref<'all' | 'unmastered' | 'mastered'>('all');

const wrongList = ref<WrongItem[]>([
  {
    id: '1',
    questionId: '1',
    questionContent: '人参的主要功效是什么？',
    userAnswers: ['A'],
    correctAnswers: ['B'],
    wrongCount: 2,
    isMastered: false,
  },
  {
    id: '2',
    questionId: '2',
    questionContent: '下列哪些是黄芪的功效？',
    userAnswers: ['A', 'B'],
    correctAnswers: ['A', 'B', 'C', 'D'],
    wrongCount: 1,
    isMastered: false,
  },
  {
    id: '3',
    questionId: '3',
    questionContent: '当归主治什么病症？',
    userAnswers: ['A'],
    correctAnswers: ['B'],
    wrongCount: 3,
    isMastered: true,
  },
]);

const filteredList = computed(() => {
  if (filter.value === 'unmastered') {
    return wrongList.value.filter(item => !item.isMastered);
  }
  if (filter.value === 'mastered') {
    return wrongList.value.filter(item => item.isMastered);
  }
  return wrongList.value;
});

const masteredCount = computed(() => wrongList.value.filter(item => item.isMastered).length);
const unmasteredCount = computed(() => wrongList.value.filter(item => !item.isMastered).length);

function markMastered(id: string) {
  const item = wrongList.value.find(w => w.id === id);
  if (item) {
    item.isMastered = true;
    uni.showToast({ title: '已标记为掌握', icon: 'success' });
  }
}

function startReview() {
  const unmastered = wrongList.value.filter(item => !item.isMastered);
  if (unmastered.length === 0) {
    uni.showToast({ title: '没有待复习的错题', icon: 'none' });
    return;
  }
  uni.navigateTo({ url: '/pages/quiz/practice?mode=wrongbook' });
}
</script>

<style lang="scss" scoped>
.container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.header {
  display: flex;
  justify-content: space-around;
  background: linear-gradient(135deg, #2B9939, #1B7A2B);
  padding: 40rpx 24rpx;

  .stat-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8rpx;

    .stat-num {
      font-size: 48rpx;
      font-weight: bold;
      color: #fff;
    }

    .stat-label {
      font-size: 24rpx;
      color: rgba(255, 255, 255, 0.8);
    }
  }
}

.filter-bar {
  display: flex;
  background: #fff;
  padding: 20rpx 24rpx;
  gap: 24rpx;

  .filter-item {
    padding: 12rpx 28rpx;
    border-radius: 32rpx;
    font-size: 26rpx;
    color: #666;
    background: #f5f5f5;

    &.active {
      background: #2B9939;
      color: #fff;
    }
  }
}

.wrong-list {
  flex: 1;
  padding: 24rpx;
  overflow-y: auto;
}

.wrong-item {
  background: #fff;
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;

  .question-content {
    font-size: 30rpx;
    color: #333;
    line-height: 1.5;
    margin-bottom: 20rpx;
  }

  .answer-info {
    display: flex;
    flex-direction: column;
    gap: 8rpx;
    margin-bottom: 20rpx;

    .wrong-answer {
      font-size: 26rpx;
      color: #F44336;
    }

    .correct-answer {
      font-size: 26rpx;
      color: #4CAF50;
    }
  }

  .wrong-count {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 24rpx;
    color: #999;

    .master-btn {
      padding: 8rpx 20rpx;
      background: #E8F5E9;
      color: #2B9939;
      border-radius: 8rpx;
    }

    .mastered-tag {
      padding: 8rpx 20rpx;
      background: #f0f0f0;
      color: #999;
      border-radius: 8rpx;
    }
  }
}

.empty {
  text-align: center;
  padding: 80rpx;
  font-size: 28rpx;
  color: #999;
}

.bottom-bar {
  padding: 24rpx 48rpx;
  background: #fff;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.06);

  .review-btn {
    height: 88rpx;
    line-height: 88rpx;
    background: #2B9939;
    color: #fff;
    border-radius: 44rpx;
    font-size: 32rpx;
  }
}
</style>
