<template>
  <view class="container">
    <view class="formula-card">
      <view class="formula-header">
        <text class="formula-name">{{ formula.name }}</text>
        <text class="formula-category">{{ formula.category }}</text>
      </view>
      <text class="formula-source" v-if="formula.source">出自：{{ formula.source }}</text>
    </view>

    <view class="section-card">
      <view class="section-title">组成</view>
      <view class="herb-composition">
        <view
          class="herb-item"
          v-for="herb in formula.herbs"
          :key="herb.herbId"
          @click="goHerb(herb.herbId)"
        >
          <view class="herb-role" :class="herb.role">
            {{ roleText[herb.role] }}
          </view>
          <text class="herb-name">{{ herb.herbName }}</text>
          <text class="herb-dosage" v-if="herb.dosage">{{ herb.dosage }}</text>
        </view>
      </view>
    </view>

    <view class="section-card">
      <view class="section-title">主治</view>
      <text class="section-content">{{ formula.indications }}</text>
    </view>

    <view class="section-card" v-if="formula.usage">
      <view class="section-title">用法</view>
      <text class="section-content">{{ formula.usage }}</text>
    </view>

    <view class="section-card" v-if="formula.modifications">
      <view class="section-title">加减变化</view>
      <text class="section-content">{{ formula.modifications }}</text>
    </view>

    <view class="section-card" v-if="formula.precautions">
      <view class="section-title">注意事项</view>
      <text class="section-content warning">{{ formula.precautions }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { Formula } from '@/types';

const formulaId = ref('');

const roleText: Record<string, string> = {
  chief: '君',
  deputy: '臣',
  assistant: '佐',
  envoy: '使',
};

const formula = ref<Formula>({
  id: '',
  name: '',
  category: '',
  indications: '',
  herbs: [],
});

function goHerb(herbId: string) {
  uni.navigateTo({ url: `/pages/herbs/detail?id=${herbId}` });
}

onMounted(() => {
  const pages = getCurrentPages();
  const currentPage = pages[pages.length - 1];
  formulaId.value = currentPage.$page?.options?.id || '1';

  // 模拟数据
  formula.value = {
    id: formulaId.value,
    name: '四君子汤',
    source: '《太平惠民和剂局方》',
    category: '补益剂',
    indications: '益气健脾。主治脾胃气虚证。面色萎白，语声低微，气短乏力，食少便溏，舌淡苔白，脉虚弱。',
    usage: '水煎服。',
    modifications: '若呕吐者，加半夏以降逆止呕；胸膈痞满者，加枳壳、陈皮以行气宽胸。',
    precautions: '阴虚血热者慎用。',
    herbs: [
      { herbId: '1', herbName: '人参', dosage: '9g', role: 'chief' },
      { herbId: '2', herbName: '白术', dosage: '9g', role: 'deputy' },
      { herbId: '3', herbName: '茯苓', dosage: '9g', role: 'assistant' },
      { herbId: '4', herbName: '炙甘草', dosage: '6g', role: 'envoy' },
    ],
  };
});
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 40rpx;
}

.formula-card {
  background: linear-gradient(135deg, #2B9939, #1B7A2B);
  padding: 48rpx 32rpx;

  .formula-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;

    .formula-name {
      font-size: 40rpx;
      font-weight: bold;
      color: #fff;
    }

    .formula-category {
      font-size: 24rpx;
      color: #2B9939;
      padding: 8rpx 20rpx;
      background: rgba(255, 255, 255, 0.9);
      border-radius: 8rpx;
    }
  }

  .formula-source {
    font-size: 26rpx;
    color: rgba(255, 255, 255, 0.8);
  }
}

.section-card {
  background: #fff;
  margin: 24rpx;
  border-radius: 24rpx;
  padding: 32rpx;

  .section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    padding-left: 20rpx;
    border-left: 8rpx solid #2B9939;
  }

  .section-content {
    font-size: 28rpx;
    color: #666;
    line-height: 1.8;

    &.warning {
      color: #F44336;
    }
  }
}

.herb-composition {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;

  .herb-item {
    display: flex;
    align-items: center;
    gap: 12rpx;
    padding: 20rpx 24rpx;
    background: #f8f8f8;
    border-radius: 16rpx;

    .herb-role {
      width: 48rpx;
      height: 48rpx;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22rpx;
      font-weight: bold;
      color: #fff;

      &.chief { background: #F44336; }
      &.deputy { background: #FF9800; }
      &.assistant { background: #2196F3; }
      &.envoy { background: #4CAF50; }
    }

    .herb-name {
      font-size: 30rpx;
      color: #333;
    }

    .herb-dosage {
      font-size: 24rpx;
      color: #999;
    }
  }
}
</style>
