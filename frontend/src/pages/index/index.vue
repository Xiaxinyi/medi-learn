<template>
  <view class="container">
    <!-- 头部Banner -->
    <view class="banner">
      <image class="banner-bg" src="/static/images/banner.png" mode="aspectFill" />
      <view class="banner-content">
        <text class="banner-title">中医学习</text>
        <text class="banner-subtitle">传承中医文化，探索草药奥秘</text>
      </view>
    </view>

    <!-- 快捷入口 -->
    <view class="quick-entry">
      <view class="entry-item" @click="navigateTo('/pages/herbs/list')">
        <view class="entry-icon herb-icon">🌿</view>
        <text class="entry-text">草药大全</text>
      </view>
      <view class="entry-item" @click="navigateTo('/pages/quiz/practice')">
        <view class="entry-icon quiz-icon">📝</view>
        <text class="entry-text">试题练习</text>
      </view>
      <view class="entry-item" @click="navigateTo('/pages/formulas/list')">
        <view class="entry-icon formula-icon">📖</view>
        <text class="entry-text">方剂学习</text>
      </view>
      <view class="entry-item" @click="navigateTo('/pages/wrongbook/list')">
        <view class="entry-icon wrong-icon">❌</view>
        <text class="entry-text">错题本</text>
      </view>
    </view>

    <!-- 学习统计卡片 -->
    <view class="stats-card" v-if="authStore.isLoggedIn">
      <view class="stats-header">
        <text class="stats-title">今日学习</text>
        <text class="stats-more" @click="navigateTo('/pages/profile/index')">更多 ></text>
      </view>
      <view class="stats-grid">
        <view class="stats-item">
          <text class="stats-num">{{ todayStats.herbs }}</text>
          <text class="stats-label">学习草药</text>
        </view>
        <view class="stats-item">
          <text class="stats-num">{{ todayStats.questions }}</text>
          <text class="stats-label">答题数量</text>
        </view>
        <view class="stats-item">
          <text class="stats-num">{{ todayStats.correct }}%</text>
          <text class="stats-label">正确率</text>
        </view>
        <view class="stats-item">
          <text class="stats-num">{{ todayStats.streak }}</text>
          <text class="stats-label">连续天数</text>
        </view>
      </view>
    </view>

    <!-- 推荐草药 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">推荐草药</text>
        <text class="section-more" @click="navigateTo('/pages/herbs/list')">全部 ></text>
      </view>
      <view class="herb-list">
        <view
          class="herb-item"
          v-for="herb in recommendedHerbs"
          :key="herb.id"
          @click="navigateTo(`/pages/herbs/detail?id=${herb.id}`)"
        >
          <image class="herb-image" :src="herb.images[0] || '/static/images/default-herb.png'" mode="aspectFill" />
          <view class="herb-info">
            <text class="herb-name">{{ herb.name }}</text>
            <view class="herb-tags">
              <text class="tag" v-for="attr in herb.attributes.slice(0, 3)" :key="attr.id" :style="{ backgroundColor: attr.color || '#e0e0e0' }">
                {{ attr.name }}
              </text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 每日一题 -->
    <view class="section" v-if="dailyQuestion">
      <view class="section-header">
        <text class="section-title">每日一题</text>
      </view>
      <view class="daily-question">
        <text class="question-content">{{ dailyQuestion.content }}</text>
        <view class="options">
          <view
            class="option-item"
            v-for="option in dailyQuestion.options"
            :key="option.id"
            @click="selectOption(option.id)"
          >
            <text class="option-key">{{ option.id }}</text>
            <text class="option-content">{{ option.content }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { herbApi, questionApi } from '@/api';
import type { Herb, Question } from '@/types';

const authStore = useAuthStore();

const todayStats = ref({ herbs: 0, questions: 0, correct: 0, streak: 0 });
const recommendedHerbs = ref<Herb[]>([]);
const dailyQuestion = ref<Question | null>(null);

function navigateTo(url: string) {
  uni.navigateTo({ url });
}

function selectOption(optionId: string) {
  uni.showToast({ title: `选择了 ${optionId}`, icon: 'none' });
}

async function loadData() {
  try {
    const herbsRes = await herbApi.list({ page_size: 6 });
    recommendedHerbs.value = herbsRes.items || [];
  } catch (e) {
    // 使用模拟数据
    recommendedHerbs.value = [
      { id: '1', name: '人参', images: [], attributes: [{ id: '1', name: '温', color: '#FF5722' }, { id: '2', name: '甘', color: '#8BC34A' }], efficacy: '大补元气', indications: '体虚欲脱', dosage: '3-9g', category: '补益药', isFavorite: false, notes: [], createdAt: Date.now() },
      { id: '2', name: '黄芪', images: [], attributes: [{ id: '3', name: '温', color: '#FF5722' }, { id: '4', name: '甘', color: '#8BC34A' }], efficacy: '补气升阳', indications: '气虚乏力', dosage: '9-30g', category: '补益药', isFavorite: false, notes: [], createdAt: Date.now() },
      { id: '3', name: '当归', images: [], attributes: [{ id: '5', name: '温', color: '#FF5722' }, { id: '6', name: '甘', color: '#8BC34A' }, { id: '7', name: '辛', color: '#9C27B0' }], efficacy: '补血活血', indications: '血虚萎黄', dosage: '6-12g', category: '补益药', isFavorite: false, notes: [], createdAt: Date.now() },
    ];
  }

  try {
    const questionsRes = await questionApi.random(1);
    dailyQuestion.value = questionsRes[0] || null;
  } catch (e) {
    dailyQuestion.value = {
      id: '1',
      type: 'single',
      content: '人参的主要功效是什么？',
      options: [
        { id: 'A', content: '清热解毒' },
        { id: 'B', content: '大补元气' },
        { id: 'C', content: '活血化瘀' },
        { id: 'D', content: '利尿消肿' },
      ],
      correctAnswers: ['B'],
      explanation: '人参性味甘、微苦，微温，归脾、肺、心、肾经，具有大补元气、复脉固脱、补脾益肺、生津养血、安神益智的功效。',
      difficulty: 'easy',
      tags: ['人参', '功效'],
    };
  }
}

onMounted(() => {
  loadData();
  if (authStore.isLoggedIn) {
    todayStats.value.streak = authStore.user?.streakDays || 0;
  }
});
</script>

<style lang="scss" scoped>
.container {
  padding-bottom: 40rpx;
}

.banner {
  position: relative;
  height: 320rpx;
  overflow: hidden;

  .banner-bg {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #2B9939, #1B7A2B);
  }

  .banner-content {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, rgba(43, 153, 57, 0.9), rgba(27, 122, 43, 0.9));
  }

  .banner-title {
    font-size: 48rpx;
    font-weight: bold;
    color: #fff;
    margin-bottom: 16rpx;
  }

  .banner-subtitle {
    font-size: 28rpx;
    color: rgba(255, 255, 255, 0.8);
  }
}

.quick-entry {
  display: flex;
  justify-content: space-around;
  padding: 32rpx;
  background: #fff;
  margin: -40rpx 24rpx 24rpx;
  border-radius: 24rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 1;

  .entry-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12rpx;
  }

  .entry-icon {
    width: 96rpx;
    height: 96rpx;
    border-radius: 24rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48rpx;
  }

  .herb-icon { background: #E8F5E9; }
  .quiz-icon { background: #FFF3E0; }
  .formula-icon { background: #E3F2FD; }
  .wrong-icon { background: #FFEBEE; }

  .entry-text {
    font-size: 24rpx;
    color: #333;
  }
}

.stats-card {
  background: #fff;
  margin: 0 24rpx 24rpx;
  border-radius: 24rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);

  .stats-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24rpx;
  }

  .stats-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
  }

  .stats-more {
    font-size: 24rpx;
    color: #2B9939;
  }

  .stats-grid {
    display: flex;
    justify-content: space-around;
  }

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

.section {
  background: #fff;
  margin: 0 24rpx 24rpx;
  border-radius: 24rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24rpx;
  }

  .section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
  }

  .section-more {
    font-size: 24rpx;
    color: #999;
  }
}

.herb-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.herb-item {
  display: flex;
  gap: 24rpx;
  padding: 20rpx;
  background: #f8f8f8;
  border-radius: 16rpx;

  .herb-image {
    width: 120rpx;
    height: 120rpx;
    border-radius: 12rpx;
    background: #e0e0e0;
  }

  .herb-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 12rpx;
  }

  .herb-name {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
  }

  .herb-tags {
    display: flex;
    gap: 12rpx;
    flex-wrap: wrap;
  }

  .tag {
    padding: 6rpx 16rpx;
    border-radius: 8rpx;
    font-size: 22rpx;
    color: #fff;
  }
}

.daily-question {
  .question-content {
    font-size: 30rpx;
    color: #333;
    line-height: 1.6;
    margin-bottom: 24rpx;
    display: block;
  }

  .options {
    display: flex;
    flex-direction: column;
    gap: 16rpx;
  }

  .option-item {
    display: flex;
    align-items: center;
    gap: 16rpx;
    padding: 24rpx;
    background: #f5f5f5;
    border-radius: 12rpx;

    .option-key {
      width: 48rpx;
      height: 48rpx;
      border-radius: 50%;
      background: #2B9939;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24rpx;
      font-weight: bold;
    }

    .option-content {
      font-size: 28rpx;
      color: #333;
    }
  }
}
</style>
