<template>
  <view class="container">
    <!-- 图片轮播 -->
    <swiper class="image-swiper" indicator-dots circular>
      <swiper-item v-for="(img, index) in herb.images" :key="index">
        <image :src="img.image_url" mode="aspectFill" />
      </swiper-item>
      <swiper-item v-if="herb.images.length === 0">
        <image src="/static/images/default-herb.png" mode="aspectFill" />
      </swiper-item>
    </swiper>

    <!-- 基本信息 -->
    <view class="info-card">
      <view class="name-section">
        <text class="herb-name">{{ herb.name }}</text>
        <text class="latin-name" v-if="herb.latinName">{{ herb.latinName }}</text>
        <text class="favorite-btn" @click="toggleFavorite">
          {{ herb.isFavorite ? '★ 已收藏' : '☆ 收藏' }}
        </text>
      </view>

      <!-- 属性标签 -->
      <view class="attributes">
        <text
          class="attr-tag"
          v-for="attr in herb.attributes"
          :key="attr.id"
          :style="{ backgroundColor: attr.color || '#e0e0e0' }"
        >
          {{ attr.name }}
        </text>
      </view>

      <!-- 别名 -->
      <view class="aliases" v-if="herb.aliases && herb.aliases.length > 0">
        <text class="label">别名：</text>
        <text class="value">{{ herb.aliases.join('、') }}</text>
      </view>

      <!-- 分类 -->
      <view class="info-row">
        <text class="label">分类：</text>
        <text class="value">{{ herb.category }}</text>
      </view>

      <!-- 产地 -->
      <view class="info-row" v-if="herb.origin">
        <text class="label">产地：</text>
        <text class="value">{{ herb.origin }}</text>
      </view>
    </view>

    <!-- 功效主治 -->
    <view class="section-card">
      <view class="section-title">功效</view>
      <text class="section-content">{{ herb.efficacy }}</text>
    </view>

    <view class="section-card">
      <view class="section-title">主治</view>
      <text class="section-content">{{ herb.indications }}</text>
    </view>

    <view class="section-card">
      <view class="section-title">用法用量</view>
      <text class="section-content">{{ herb.dosage }}</text>
    </view>

    <view class="section-card" v-if="herb.contraindications">
      <view class="section-title">禁忌</view>
      <text class="section-content warning">{{ herb.contraindications }}</text>
    </view>

    <!-- 相关方剂 -->
    <view class="section-card" v-if="relatedFormulas.length > 0">
      <view class="section-title">相关方剂</view>
      <view class="formula-list">
        <view
          class="formula-item"
          v-for="formula in relatedFormulas"
          :key="formula.id"
          @click="goFormula(formula.id)"
        >
          <text class="formula-name">{{ formula.name }}</text>
          <text class="formula-category">{{ formula.category }}</text>
        </view>
      </view>
    </view>

    <!-- 个人笔记 -->
    <view class="section-card">
      <view class="section-title">我的笔记</view>
      <view class="notes-list">
        <view class="note-item" v-for="note in herb.notes" :key="note.id">
          <text class="note-content">{{ note.content }}</text>
          <text class="note-time">{{ formatDate(note.createdAt) }}</text>
        </view>
        <view class="empty-notes" v-if="herb.notes.length === 0">
          <text>暂无笔记，点击添加</text>
        </view>
      </view>
      <view class="add-note">
        <input
          type="text"
          v-model="newNote"
          placeholder="添加学习笔记..."
          confirm-type="done"
          @confirm="addNote"
        />
        <button class="add-btn" @click="addNote">添加</button>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { herbApi, formulaApi } from '@/api';
import type { Herb, Formula } from '@/types';

const herbId = ref('');
const herb = ref<Herb>({
  id: '',
  name: '',
  attributes: [],
  efficacy: '',
  indications: '',
  dosage: '',
  images: [],
  category: '',
  isFavorite: false,
  notes: [],
  createdAt: 0,
});
const relatedFormulas = ref<Formula[]>([]);
const newNote = ref('');

function toggleFavorite() {
  herb.value.isFavorite = !herb.value.isFavorite;
  uni.showToast({ title: herb.value.isFavorite ? '已收藏' : '已取消收藏', icon: 'none' });
}

function addNote() {
  if (!newNote.value.trim()) return;
  herb.value.notes.push({
    id: Date.now().toString(),
    content: newNote.value,
    createdAt: Date.now(),
  });
  newNote.value = '';
  uni.showToast({ title: '笔记添加成功', icon: 'success' });
}

function formatDate(timestamp: number) {
  const date = new Date(timestamp);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

function goFormula(id: string) {
  uni.navigateTo({ url: `/pages/formulas/detail?id=${id}` });
}

async function loadData() {
  try {
    const res = await herbApi.detail(herbId.value);
    herb.value = res;
  } catch (e) {
    uni.showToast({ title: '加载失败', icon: 'none' });
  }

  try {
    const formulasRes = await formulaApi.byHerb(herbId.value);
    relatedFormulas.value = formulasRes || [];
  } catch (e) {
    relatedFormulas.value = [
      { id: '1', name: '四君子汤', category: '补益剂', indications: '益气健脾', usage: '', herbs: [] },
      { id: '2', name: '生脉散', category: '补益剂', indications: '益气生津，敛阴止汗', usage: '', herbs: [] },
    ];
  }
}

onMounted(() => {
  const pages = getCurrentPages();
  const currentPage = pages[pages.length - 1];
  herbId.value = currentPage.$page?.options?.id || '1';
  loadData();
});
</script>

<style lang="scss" scoped>
.container {
  background: #f5f5f5;
  padding-bottom: 40rpx;
}

.image-swiper {
  height: 400rpx;

  image {
    width: 100%;
    height: 100%;
  }
}

.info-card {
  background: #fff;
  margin: -40rpx 24rpx 24rpx;
  border-radius: 24rpx;
  padding: 32rpx;
  position: relative;
  z-index: 1;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);

  .name-section {
    display: flex;
    align-items: center;
    gap: 16rpx;
    margin-bottom: 20rpx;
    flex-wrap: wrap;

    .herb-name {
      font-size: 40rpx;
      font-weight: bold;
      color: #333;
    }

    .latin-name {
      font-size: 24rpx;
      color: #999;
      font-style: italic;
    }

    .favorite-btn {
      margin-left: auto;
      font-size: 26rpx;
      color: #FF9800;
      padding: 8rpx 20rpx;
      background: #FFF8E1;
      border-radius: 24rpx;
    }
  }

  .attributes {
    display: flex;
    flex-wrap: wrap;
    gap: 12rpx;
    margin-bottom: 20rpx;

    .attr-tag {
      padding: 8rpx 20rpx;
      border-radius: 8rpx;
      font-size: 24rpx;
      color: #fff;
    }
  }

  .aliases, .info-row {
    display: flex;
    margin-bottom: 12rpx;

    .label {
      font-size: 26rpx;
      color: #999;
      min-width: 100rpx;
    }

    .value {
      font-size: 26rpx;
      color: #333;
    }
  }
}

.section-card {
  background: #fff;
  margin: 0 24rpx 24rpx;
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

.formula-list {
  .formula-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20rpx 0;
    border-bottom: 2rpx solid #f0f0f0;

    .formula-name {
      font-size: 30rpx;
      color: #333;
    }

    .formula-category {
      font-size: 24rpx;
      color: #2B9939;
      padding: 4rpx 16rpx;
      background: #E8F5E9;
      border-radius: 8rpx;
    }
  }
}

.notes-list {
  .note-item {
    padding: 20rpx 0;
    border-bottom: 2rpx solid #f0f0f0;

    .note-content {
      font-size: 28rpx;
      color: #333;
      line-height: 1.6;
      display: block;
    }

    .note-time {
      font-size: 22rpx;
      color: #999;
      margin-top: 8rpx;
      display: block;
    }
  }

  .empty-notes {
    text-align: center;
    padding: 40rpx;
    font-size: 26rpx;
    color: #999;
  }
}

.add-note {
  display: flex;
  gap: 16rpx;
  margin-top: 24rpx;

  input {
    flex: 1;
    height: 72rpx;
    background: #f5f5f5;
    border-radius: 12rpx;
    padding: 0 20rpx;
    font-size: 26rpx;
  }

  .add-btn {
    width: 120rpx;
    height: 72rpx;
    background: #2B9939;
    color: #fff;
    border-radius: 12rpx;
    font-size: 26rpx;
  }
}
</style>
