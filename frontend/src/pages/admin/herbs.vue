<template>
  <view class="container">
    <view class="search-bar">
      <input class="search-input" v-model="keyword" placeholder="搜索草药名称" @confirm="loadHerbs" />
      <button class="search-btn" @click="loadHerbs">搜索</button>
    </view>

    <view class="filter-tabs">
      <text class="tab-item" :class="{ active: categoryFilter === '' }" @click="setCategoryFilter('')">全部</text>
      <text class="tab-item" :class="{ active: categoryFilter === cat }" v-for="cat in categories" :key="cat" @click="setCategoryFilter(cat)">{{ cat }}</text>
    </view>

    <view class="herb-list">
      <view class="herb-item" v-for="h in herbs" :key="h.id">
        <view class="herb-main">
          <text class="herb-name">{{ h.name }}</text>
          <text class="herb-category">{{ h.category }}</text>
        </view>
        <text class="herb-efficacy">{{ h.efficacy }}</text>
        <view class="herb-actions">
          <button class="action-btn" @click="editHerb(h)">编辑</button>
          <button class="action-btn warn" @click="deleteHerb(h.id)">删除</button>
        </view>
      </view>
    </view>

    <view class="empty-state" v-if="herbs.length === 0 && !loading">
      <text>暂无草药数据</text>
    </view>

    <button class="fab-btn" @click="openCreateModal">+</button>

    <view class="modal-mask" v-if="showCreateModal" @click="showCreateModal = false">
      <view class="modal-content" @click.stop>
        <text class="modal-title">{{ isEdit ? '编辑草药' : '创建草药' }}</text>
        <view class="form-body">
          <view class="form-item">
            <text class="form-label">名称</text>
            <view class="form-input-wrap">
              <input class="form-input" v-model="form.name" placeholder="请输入草药名称" />
              <button class="ai-btn" @click="generateByAI" :disabled="aiLoading || !form.name">
                {{ aiLoading ? '生成中...' : 'AI生成' }}
              </button>
            </view>
          </view>
          <view class="form-item">
            <text class="form-label">拉丁名</text>
            <input class="form-input" v-model="form.latinName" placeholder="请输入拉丁名" />
          </view>
          <view class="form-item">
            <text class="form-label">别名（用逗号分隔）</text>
            <input class="form-input" v-model="aliasInput" placeholder="如：棒槌,地精" />
          </view>
          <view class="form-item">
            <text class="form-label">分类</text>
            <picker mode="selector" :range="categories" :value="categoryIndex" @change="onCategoryChange">
              <view class="picker-value" :class="{ 'has-value': form.category }">{{ form.category || '请选择分类' }}</view>
            </picker>
          </view>
          <view class="form-item">
            <text class="form-label">功效</text>
            <textarea class="form-textarea" v-model="form.efficacy" placeholder="请输入功效" />
          </view>
          <view class="form-item">
            <text class="form-label">主治</text>
            <textarea class="form-textarea" v-model="form.indications" placeholder="请输入主治" />
          </view>
          <view class="form-item">
            <text class="form-label">用量</text>
            <input class="form-input" v-model="form.dosage" placeholder="如：3-9g" />
          </view>
          <view class="form-item">
            <text class="form-label">禁忌</text>
            <textarea class="form-textarea" v-model="form.contraindications" placeholder="请输入禁忌" />
          </view>
          <view class="form-item">
            <text class="form-label">产地</text>
            <input class="form-input" v-model="form.origin" placeholder="如：吉林、辽宁" />
          </view>
        </view>
        <view class="modal-actions">
          <button class="modal-btn cancel" @click="showCreateModal = false">取消</button>
          <button class="modal-btn confirm" @click="submitHerb">确定</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { herbApi } from '@/api';

const herbs = ref<any[]>([]);
const loading = ref(false);
const keyword = ref('');
const categoryFilter = ref('');
const showCreateModal = ref(false);
const isEdit = ref(false);
const editId = ref('');

const categories = ref(['解表药', '清热药', '泻下药', '祛风湿药', '化湿药', '利水渗湿药', '温里药', '理气药', '消食药', '驱虫药', '止血药', '活血化瘀药', '化痰止咳平喘药', '安神药', '平肝息风药', '开窍药', '补益药', '收涩药']);
const categoryIndex = ref(0);
const aliasInput = ref('');
const aiLoading = ref(false);

const form = reactive({
  name: '',
  latinName: '',
  aliases: [] as string[],
  category: '',
  efficacy: '',
  indications: '',
  dosage: '',
  contraindications: '',
  origin: '',
});

async function loadHerbs() {
  loading.value = true;
  try {
    const params: any = {};
    if (categoryFilter.value) params.category = categoryFilter.value;
    if (keyword.value) params.search = keyword.value;
    const res = await herbApi.list(params);
    herbs.value = res.items || [];
  } catch (e) {
    uni.showToast({ title: '加载失败', icon: 'none' });
  } finally {
    loading.value = false;
  }
}

function setCategoryFilter(cat: string) {
  categoryFilter.value = cat;
  loadHerbs();
}

function onCategoryChange(e: any) {
  categoryIndex.value = e.detail.value;
  form.category = categories.value[e.detail.value];
}

function editHerb(h: any) {
  isEdit.value = true;
  editId.value = h.id;
  form.name = h.name || '';
  form.latinName = h.latinName || '';
  form.aliases = h.aliases || [];
  aliasInput.value = (h.aliases || []).join(',');
  form.category = h.category || '';
  form.efficacy = h.efficacy || '';
  form.indications = h.indications || '';
  form.dosage = h.dosage || '';
  form.contraindications = h.contraindications || '';
  form.origin = h.origin || '';
  categoryIndex.value = categories.value.indexOf(form.category);
  showCreateModal.value = true;
}

function resetForm() {
  isEdit.value = false;
  editId.value = '';
  form.name = '';
  form.latinName = '';
  form.aliases = [];
  form.category = '';
  form.efficacy = '';
  form.indications = '';
  form.dosage = '';
  form.contraindications = '';
  form.origin = '';
  aliasInput.value = '';
  categoryIndex.value = 0;
}

function openCreateModal() {
  resetForm();
  showCreateModal.value = true;
}

async function deleteHerb(id: string) {
  uni.showModal({
    title: '确认删除',
    content: '确定要删除这个草药吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await herbApi.delete(id);
          uni.showToast({ title: '删除成功', icon: 'success' });
          loadHerbs();
        } catch (e) {
          uni.showToast({ title: '删除失败', icon: 'none' });
        }
      }
    },
  });
}

async function generateByAI() {
  if (!form.name) {
    uni.showToast({ title: '请先输入草药名称', icon: 'none' });
    return;
  }
  aiLoading.value = true;
  try {
    const res = await herbApi.generate(form.name);
    if (res.latin_name) form.latinName = res.latin_name;
    if (res.aliases) aliasInput.value = (res.aliases || []).join(',');
    if (res.category) {
      form.category = res.category;
      categoryIndex.value = categories.value.indexOf(res.category);
    }
    if (res.efficacy) form.efficacy = res.efficacy;
    if (res.indications) form.indications = res.indications;
    if (res.dosage) form.dosage = res.dosage;
    if (res.contraindications) form.contraindications = res.contraindications;
    if (res.origin) form.origin = res.origin;
    uni.showToast({ title: 'AI生成成功', icon: 'success' });
  } catch (e: any) {
    const msg = e?.detail || e?.message || '生成失败';
    uni.showToast({ title: msg, icon: 'none', duration: 3000 });
  } finally {
    aiLoading.value = false;
  }
}

async function submitHerb() {
  if (!form.name || !form.category) {
    uni.showToast({ title: '请填写名称和分类', icon: 'none' });
    return;
  }
  try {
    const payload = {
      name: form.name,
      latin_name: form.latinName,
      aliases: aliasInput.value.split(',').map((s) => s.trim()).filter(Boolean),
      category: form.category,
      efficacy: form.efficacy,
      indications: form.indications,
      dosage: form.dosage,
      contraindications: form.contraindications,
      origin: form.origin,
    };
    if (isEdit.value) {
      await herbApi.update(editId.value, payload);
    } else {
      await herbApi.create(payload);
    }
    uni.showToast({ title: '保存成功', icon: 'success' });
    showCreateModal.value = false;
    resetForm();
    loadHerbs();
  } catch (e: any) {
    const msg = e?.detail || e?.message || JSON.stringify(e).slice(0, 100);
    uni.showToast({ title: `保存失败: ${msg}`, icon: 'none', duration: 3000 });
  }
}

onMounted(() => {
  loadHerbs();
});
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 120rpx;
}

.search-bar {
  display: flex;
  gap: 16rpx;
  padding: 24rpx;
  background: #fff;

  .search-input {
    flex: 1;
    height: 72rpx;
    background: #f5f5f5;
    border-radius: 16rpx;
    padding: 0 24rpx;
    font-size: 28rpx;
  }

  .search-btn {
    width: 120rpx;
    height: 72rpx;
    background: #2B9939;
    color: #fff;
    border-radius: 16rpx;
    font-size: 28rpx;
  }
}

.filter-tabs {
  display: flex;
  flex-wrap: wrap;
  background: #fff;
  padding: 0 24rpx 24rpx;
  gap: 12rpx;

  .tab-item {
    padding: 10rpx 24rpx;
    border-radius: 32rpx;
    font-size: 24rpx;
    color: #666;
    background: #f5f5f5;

    &.active {
      background: #2B9939;
      color: #fff;
    }
  }
}

.herb-list {
  padding: 0 24rpx;

  .herb-item {
    background: #fff;
    border-radius: 24rpx;
    padding: 32rpx;
    margin-bottom: 24rpx;

    .herb-main {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12rpx;

      .herb-name {
        font-size: 32rpx;
        font-weight: bold;
        color: #333;
      }

      .herb-category {
        font-size: 24rpx;
        color: #2B9939;
        background: #F0FFF0;
        padding: 4rpx 16rpx;
        border-radius: 8rpx;
      }
    }

    .herb-efficacy {
      font-size: 26rpx;
      color: #666;
      display: block;
      margin-bottom: 20rpx;
      line-height: 1.5;
    }

    .herb-actions {
      display: flex;
      gap: 16rpx;

      .action-btn {
        flex: 1;
        height: 64rpx;
        background: #2B9939;
        color: #fff;
        border-radius: 16rpx;
        font-size: 26rpx;
        display: flex;
        align-items: center;
        justify-content: center;

        &.warn {
          background: #F44336;
        }
      }
    }
  }
}

.empty-state {
  text-align: center;
  padding: 120rpx 0;
  color: #999;
  font-size: 28rpx;

}

.fab-btn {
  position: fixed;
  right: 40rpx;
  bottom: 140rpx;
  width: 96rpx;
  height: 96rpx;
  border-radius: 50%;
  background: #2B9939;
  color: #fff;
  font-size: 44rpx;
  padding-bottom: 18rpx;
  box-shadow: 0 8rpx 24rpx rgba(43, 153, 57, 0.35);
  transition: transform 0.15s, box-shadow 0.15s;

  &:active {
    transform: scale(0.92);
    box-shadow: 0 4rpx 12rpx rgba(43, 153, 57, 0.25);
  }
}

.modal-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;

  .modal-content {
    width: 85%;
    max-height: 80vh;
    background: #fff;
    border-radius: 24rpx;
    display: flex;
    flex-direction: column;
    overflow: hidden;

    .modal-title {
      display: block;
      font-size: 36rpx;
      font-weight: bold;
      color: #333;
      text-align: center;
      padding: 48rpx 48rpx 32rpx;
      flex-shrink: 0;
    }

    .form-body {
      flex: 1;
      overflow-y: auto;
      padding: 0 48rpx;
    }

    .form-item {
      margin-bottom: 24rpx;

      .form-label {
        display: block;
        font-size: 28rpx;
        color: #333;
        margin-bottom: 12rpx;
      }

      .form-input-wrap {
        display: flex;
        gap: 16rpx;
        align-items: center;

        .form-input {
          flex: 1;
        }

        .ai-btn {
          width: 140rpx;
          height: 72rpx;
          background: #2196F3;
          color: #fff;
          border-radius: 16rpx;
          font-size: 26rpx;
          display: flex;
          align-items: center;
          justify-content: center;

          &:disabled {
            background: #90CAF9;
          }
        }
      }

      .form-input, .form-textarea, .picker-value {
        height: 80rpx;
        background: #f5f5f5;
        border-radius: 16rpx;
        padding: 0 24rpx;
        font-size: 28rpx;
      }

      .form-textarea {
        height: 160rpx;
        padding: 16rpx 24rpx;
        width: 100%;
      }

      .picker-value {
        line-height: 80rpx;
        color: #999;

        &.has-value {
          color: #333;
        }
      }
    }

    .modal-actions {
      display: flex;
      gap: 24rpx;
      padding: 24rpx 48rpx 48rpx;
      flex-shrink: 0;

      .modal-btn {
        flex: 1;
        height: 80rpx;
        border-radius: 16rpx;
        font-size: 30rpx;

        &.cancel {
          background: #f5f5f5;
          color: #666;
        }

        &.confirm {
          background: #2B9939;
          color: #fff;
        }
      }
    }
  }
}
</style>
