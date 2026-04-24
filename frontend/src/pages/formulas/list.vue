<template>
  <view class="container">
    <view class="search-bar">
      <view class="search-input">
        <text class="search-icon">🔍</text>
        <input type="text" v-model="searchKeyword" placeholder="搜索方剂名称" confirm-type="search" @confirm="onSearch" />
      </view>
    </view>

    <scroll-view class="formula-scroll" scroll-y>
      <view class="formula-list">
        <view
          class="formula-card"
          v-for="formula in formulaList"
          :key="formula.id"
          @click="goDetail(formula.id)"
        >
          <view class="formula-header">
            <text class="formula-name">{{ formula.name }}</text>
            <text class="formula-category">{{ formula.category }}</text>
          </view>
          <text class="formula-source" v-if="formula.source">出自：{{ formula.source }}</text>
          <text class="formula-indications">{{ formula.indications }}</text>
          <view class="formula-herbs">
            <text class="herb-tag" v-for="(herb, index) in formula.herbs.slice(0, 5)" :key="index">
              {{ herb.herbName }}
            </text>
            <text v-if="formula.herbs.length > 5">...</text>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { Formula } from '@/types';

const searchKeyword = ref('');

const formulaList = ref<Formula[]>([
  {
    id: '1',
    name: '四君子汤',
    source: '《太平惠民和剂局方》',
    category: '补益剂',
    indications: '益气健脾。主治脾胃气虚证。',
    herbs: [
      { herbId: '1', herbName: '人参', role: 'chief' },
      { herbId: '2', herbName: '白术', role: 'deputy' },
      { herbId: '3', herbName: '茯苓', role: 'assistant' },
      { herbId: '4', herbName: '炙甘草', role: 'envoy' },
    ],
  },
  {
    id: '2',
    name: '生脉散',
    source: '《医学启源》',
    category: '补益剂',
    indications: '益气生津，敛阴止汗。',
    herbs: [
      { herbId: '1', herbName: '人参', role: 'chief' },
      { herbId: '5', herbName: '麦冬', role: 'deputy' },
      { herbId: '6', herbName: '五味子', role: 'assistant' },
    ],
  },
  {
    id: '3',
    name: '桂枝汤',
    source: '《伤寒论》',
    category: '解表剂',
    indications: '解肌发表，调和营卫。',
    herbs: [
      { herbId: '7', herbName: '桂枝', role: 'chief' },
      { herbId: '8', herbName: '白芍', role: 'deputy' },
      { herbId: '9', herbName: '生姜', role: 'assistant' },
      { herbId: '10', herbName: '大枣', role: 'assistant' },
      { herbId: '11', herbName: '炙甘草', role: 'envoy' },
    ],
  },
]);

function onSearch() {
  uni.showToast({ title: `搜索: ${searchKeyword.value}`, icon: 'none' });
}

function goDetail(id: string) {
  uni.navigateTo({ url: `/pages/formulas/detail?id=${id}` });
}
</script>

<style lang="scss" scoped>
.container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.search-bar {
  padding: 24rpx;
  background: #fff;

  .search-input {
    display: flex;
    align-items: center;
    background: #f5f5f5;
    border-radius: 36rpx;
    padding: 16rpx 24rpx;
    gap: 12rpx;

    input {
      flex: 1;
      font-size: 28rpx;
    }
  }
}

.formula-scroll {
  flex: 1;
  padding: 24rpx;
}

.formula-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.formula-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 32rpx;

  .formula-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;

    .formula-name {
      font-size: 34rpx;
      font-weight: bold;
      color: #333;
    }

    .formula-category {
      font-size: 24rpx;
      color: #2B9939;
      padding: 6rpx 16rpx;
      background: #E8F5E9;
      border-radius: 8rpx;
    }
  }

  .formula-source {
    font-size: 24rpx;
    color: #999;
    display: block;
    margin-bottom: 12rpx;
  }

  .formula-indications {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
    display: block;
    margin-bottom: 16rpx;
  }

  .formula-herbs {
    display: flex;
    flex-wrap: wrap;
    gap: 12rpx;

    .herb-tag {
      padding: 8rpx 16rpx;
      background: #f0f0f0;
      border-radius: 8rpx;
      font-size: 24rpx;
      color: #666;
    }
  }
}
</style>
