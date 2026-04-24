<template>
  <view class="container">
    <!-- 搜索栏 -->
    <view class="search-bar">
      <view class="search-input">
        <text class="search-icon">🔍</text>
        <input
          type="text"
          v-model="searchKeyword"
          placeholder="搜索草药名称、功效"
          confirm-type="search"
          @confirm="onSearch"
        />
      </view>
    </view>

    <!-- 分类筛选 -->
    <scroll-view class="category-scroll" scroll-x>
      <view class="category-list">
        <view
          class="category-item"
          :class="{ active: currentCategory === '' }"
          @click="selectCategory('')"
        >
          <text>全部</text>
        </view>
        <view
          class="category-item"
          v-for="cat in categories"
          :key="cat"
          :class="{ active: currentCategory === cat }"
          @click="selectCategory(cat)"
        >
          <text>{{ cat }}</text>
        </view>
      </view>
    </scroll-view>

    <!-- 草药列表 -->
    <scroll-view class="herb-scroll" scroll-y @scrolltolower="loadMore">
      <view class="herb-list">
        <view
          class="herb-card"
          v-for="herb in herbList"
          :key="herb.id"
          @click="goDetail(herb.id)"
        >
          <image
            class="herb-image"
            :src="herb.images[0] || '/static/images/default-herb.png'"
            mode="aspectFill"
          />
          <view class="herb-info">
            <view class="herb-header">
              <text class="herb-name">{{ herb.name }}</text>
              <text class="favorite-icon" @click.stop="toggleFavorite(herb)">
                {{ herb.isFavorite ? '★' : '☆' }}
              </text>
            </view>
            <view class="herb-tags">
              <text
                class="tag"
                v-for="attr in herb.attributes.slice(0, 4)"
                :key="attr.id"
                :style="{ backgroundColor: attr.color || '#e0e0e0' }"
              >
                {{ attr.name }}
              </text>
            </view>
            <text class="herb-efficacy">{{ herb.efficacy }}</text>
          </view>
        </view>
      </view>

      <view class="loading-more" v-if="loading">
        <text>加载中...</text>
      </view>
      <view class="no-more" v-if="!hasMore && herbList.length > 0">
        <text>没有更多了</text>
      </view>
    </scroll-view>

    <!-- 添加按钮 (admin) -->
    <view class="fab" v-if="authStore.isAdmin" @click="goAdd">
      <text class="fab-icon">+</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { herbApi } from '@/api';
import type { Herb } from '@/types';

const authStore = useAuthStore();

const searchKeyword = ref('');
const currentCategory = ref('');
const categories = ref(['解表药', '清热药', '补益药', '活血化瘀', '祛湿药', '理气药', '消食药', '驱虫药']);
const herbList = ref<Herb[]>([]);
const loading = ref(false);
const hasMore = ref(true);
const page = ref(1);

function selectCategory(cat: string) {
  currentCategory.value = cat;
  page.value = 1;
  hasMore.value = true;
  loadHerbs(true);
}

function onSearch() {
  page.value = 1;
  hasMore.value = true;
  loadHerbs(true);
}

async function loadHerbs(refresh = false) {
  if (loading.value) return;
  loading.value = true;

  try {
    const res = await herbApi.list({
      search: searchKeyword.value,
      category: currentCategory.value,
      page: page.value,
      page_size: 20,
    });

    if (refresh) {
      herbList.value = res.items || [];
    } else {
      herbList.value = [...herbList.value, ...(res.items || [])];
    }

    hasMore.value = herbList.value.length < res.total;
  } catch (e) {
    // 模拟数据
    herbList.value = [
      { id: '1', name: '人参', images: [], attributes: [{ id: '1', name: '温', color: '#FF5722' }, { id: '2', name: '甘', color: '#8BC34A' }], efficacy: '大补元气，复脉固脱', indications: '体虚欲脱', dosage: '3-9g', category: '补益药', isFavorite: false, notes: [], createdAt: Date.now() },
      { id: '2', name: '黄芪', images: [], attributes: [{ id: '3', name: '温', color: '#FF5722' }, { id: '4', name: '甘', color: '#8BC34A' }], efficacy: '补气升阳，固表止汗', indications: '气虚乏力', dosage: '9-30g', category: '补益药', isFavorite: true, notes: [], createdAt: Date.now() },
      { id: '3', name: '当归', images: [], attributes: [{ id: '5', name: '温', color: '#FF5722' }, { id: '6', name: '甘', color: '#8BC34A' }, { id: '7', name: '辛', color: '#9C27B0' }], efficacy: '补血活血，调经止痛', indications: '血虚萎黄', dosage: '6-12g', category: '补益药', isFavorite: false, notes: [], createdAt: Date.now() },
      { id: '4', name: '金银花', images: [], attributes: [{ id: '8', name: '寒', color: '#2196F3' }, { id: '9', name: '甘', color: '#8BC34A' }], efficacy: '清热解毒，疏散风热', indications: '痈肿疔疮', dosage: '6-15g', category: '清热药', isFavorite: false, notes: [], createdAt: Date.now() },
      { id: '5', name: '麻黄', images: [], attributes: [{ id: '10', name: '温', color: '#FF5722' }, { id: '11', name: '辛', color: '#9C27B0' }, { id: '12', name: '微苦', color: '#FF9800' }], efficacy: '发汗解表，宣肺平喘', indications: '风寒感冒', dosage: '2-10g', category: '解表药', isFavorite: false, notes: [], createdAt: Date.now() },
    ];
  } finally {
    loading.value = false;
  }
}

function loadMore() {
  if (!hasMore.value || loading.value) return;
  page.value++;
  loadHerbs();
}

function goDetail(id: string) {
  uni.navigateTo({ url: `/pages/herbs/detail?id=${id}` });
}

function goAdd() {
  uni.navigateTo({ url: '/pages/herbs/edit' });
}

function toggleFavorite(herb: Herb) {
  herb.isFavorite = !herb.isFavorite;
  uni.showToast({
    title: herb.isFavorite ? '已收藏' : '已取消收藏',
    icon: 'none',
  });
}

onMounted(() => {
  loadHerbs(true);
});
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

    .search-icon {
      font-size: 32rpx;
    }

    input {
      flex: 1;
      font-size: 28rpx;
    }
  }
}

.category-scroll {
  background: #fff;
  padding: 0 24rpx 24rpx;
  white-space: nowrap;

  .category-list {
    display: flex;
    gap: 16rpx;
  }

  .category-item {
    padding: 12rpx 28rpx;
    border-radius: 32rpx;
    background: #f5f5f5;
    font-size: 26rpx;
    color: #666;

    &.active {
      background: #2B9939;
      color: #fff;
    }
  }
}

.herb-scroll {
  flex: 1;
  padding: 24rpx;
}

.herb-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.herb-card {
  display: flex;
  background: #fff;
  border-radius: 24rpx;
  padding: 24rpx;
  gap: 24rpx;

  .herb-image {
    width: 160rpx;
    height: 160rpx;
    border-radius: 16rpx;
    background: #e0e0e0;
  }

  .herb-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .herb-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .herb-name {
    font-size: 34rpx;
    font-weight: bold;
    color: #333;
  }

  .favorite-icon {
    font-size: 40rpx;
    color: #FF9800;
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

  .herb-efficacy {
    font-size: 26rpx;
    color: #666;
    line-height: 1.4;
  }
}

.loading-more, .no-more {
  text-align: center;
  padding: 32rpx;
  font-size: 24rpx;
  color: #999;
}

.fab {
  position: fixed;
  right: 40rpx;
  bottom: 160rpx;
  width: 96rpx;
  height: 96rpx;
  border-radius: 50%;
  background: #2B9939;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 20rpx rgba(43, 153, 57, 0.4);

  .fab-icon {
    font-size: 48rpx;
    color: #fff;
  }
}
</style>
