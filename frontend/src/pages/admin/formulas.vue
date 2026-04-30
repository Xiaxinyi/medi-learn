<template>
  <view class="container">
    <view class="search-bar">
      <input class="search-input" v-model="keyword" placeholder="搜索方剂名称" @confirm="loadFormulas" />
      <button class="search-btn" @click="loadFormulas">搜索</button>
    </view>

    <view class="formula-list">
      <view class="formula-item" v-for="f in formulas" :key="f.id">
        <text class="formula-name">{{ f.name }}</text>
        <text class="formula-category">{{ f.category }}</text>
        <text class="formula-indications">{{ f.indications }}</text>
        <view class="formula-herbs" v-if="f.herbs && f.herbs.length">
          <text class="herb-tag" v-for="h in f.herbs" :key="h.herbId">{{ h.herbName }}({{ roleText(h.role) }})</text>
        </view>
        <view class="formula-actions">
          <button class="action-btn" @click="editFormula(f)">编辑</button>
          <button class="action-btn warn" @click="deleteFormula(f.id)">删除</button>
        </view>
      </view>
    </view>

    <view class="empty-state" v-if="formulas.length === 0 && !loading">
      <text>暂无方剂数据</text>
    </view>

    <button class="fab-btn" @click="showCreateModal = true">+</button>

    <view class="modal-mask" v-if="showCreateModal" @click="showCreateModal = false">
      <view class="modal-content" @click.stop>
        <text class="modal-title">{{ isEdit ? '编辑方剂' : '创建方剂' }}</text>
        <view class="form-body">
          <view class="form-item">
            <text class="form-label">方剂名称</text>
            <input class="form-input" v-model="form.name" placeholder="请输入方剂名称" />
          </view>
          <view class="form-item">
            <text class="form-label">来源</text>
            <input class="form-input" v-model="form.source" placeholder="如：伤寒论" />
          </view>
          <view class="form-item">
            <text class="form-label">分类</text>
            <input class="form-input" v-model="form.category" placeholder="如：解表剂" />
          </view>
          <view class="form-item">
            <text class="form-label">主治</text>
            <textarea class="form-textarea" v-model="form.indications" placeholder="请输入主治症状" />
          </view>
          <view class="form-item">
            <text class="form-label">用法</text>
            <textarea class="form-textarea" v-model="form.usage" placeholder="请输入用法用量" />
          </view>
          <view class="form-item">
            <text class="form-label">加减变化</text>
            <textarea class="form-textarea" v-model="form.modifications" placeholder="请输入加减变化" />
          </view>
          <view class="form-item">
            <text class="form-label">注意事项</text>
            <textarea class="form-textarea" v-model="form.precautions" placeholder="请输入注意事项" />
          </view>
          <view class="form-item">
            <text class="form-label">组成药材</text>
            <view v-for="(h, idx) in form.herbs" :key="idx" class="herb-input-row">
              <input class="form-input flex-1" v-model="h.herbName" placeholder="药材名" />
              <input class="form-input small" v-model="h.dosage" placeholder="用量" />
              <picker mode="selector" :range="roles" :value="roleIndex(h.role)" @change="(e: any) => onRoleChange(e, idx)">
                <view class="picker-small">{{ roleText(h.role) }}</view>
              </picker>
              <text class="delete-text" @click="removeHerb(idx)">删除</text>
            </view>
            <button class="add-herb-btn" @click="addHerb">+ 添加药材</button>
          </view>
        </view>
        <view class="modal-actions">
          <button class="modal-btn cancel" @click="showCreateModal = false">取消</button>
          <button class="modal-btn confirm" @click="submitFormula">确定</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { formulaApi } from '@/api';

const formulas = ref<any[]>([]);
const loading = ref(false);
const keyword = ref('');
const showCreateModal = ref(false);
const isEdit = ref(false);
const editId = ref('');

const roles = ['君药', '臣药', '佐药', '使药'];
const roleValues = ['chief', 'deputy', 'assistant', 'envoy'];

const form = reactive({
  name: '',
  source: '',
  category: '',
  indications: '',
  usage: '',
  modifications: '',
  precautions: '',
  herbs: [] as any[],
});

function roleText(role: string) {
  const map: Record<string, string> = { chief: '君药', deputy: '臣药', assistant: '佐药', envoy: '使药' };
  return map[role] || role;
}

function roleIndex(role: string) {
  return roleValues.indexOf(role);
}

function onRoleChange(e: any, idx: number) {
  form.herbs[idx].role = roleValues[e.detail.value];
}

function addHerb() {
  form.herbs.push({ herbId: '', herbName: '', dosage: '', role: 'chief' });
}

function removeHerb(idx: number) {
  form.herbs.splice(idx, 1);
}

async function loadFormulas() {
  loading.value = true;
  try {
    const params: any = {};
    if (keyword.value) params.search = keyword.value;
    const res = await formulaApi.list(params);
    formulas.value = res.items || [];
  } catch (e) {
    uni.showToast({ title: '加载失败', icon: 'none' });
  } finally {
    loading.value = false;
  }
}

function editFormula(f: any) {
  isEdit.value = true;
  editId.value = f.id;
  form.name = f.name || '';
  form.source = f.source || '';
  form.category = f.category || '';
  form.indications = f.indications || '';
  form.usage = f.usage || '';
  form.modifications = f.modifications || '';
  form.precautions = f.precautions || '';
  form.herbs = (f.herbs || []).map((h: any) => ({ ...h }));
  showCreateModal.value = true;
}

async function deleteFormula(id: string) {
  uni.showModal({
    title: '确认删除',
    content: '确定要删除这个方剂吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await formulaApi.delete(id);
          uni.showToast({ title: '删除成功', icon: 'success' });
          loadFormulas();
        } catch (e) {
          uni.showToast({ title: '删除失败', icon: 'none' });
        }
      }
    },
  });
}

function resetForm() {
  isEdit.value = false;
  editId.value = '';
  form.name = '';
  form.source = '';
  form.category = '';
  form.indications = '';
  form.usage = '';
  form.modifications = '';
  form.precautions = '';
  form.herbs = [];
}

async function submitFormula() {
  if (!form.name || !form.category || !form.indications) {
    uni.showToast({ title: '请填写必填项', icon: 'none' });
    return;
  }
  try {
    const payload = {
      name: form.name,
      source: form.source,
      category: form.category,
      indications: form.indications,
      usage: form.usage,
      modifications: form.modifications,
      precautions: form.precautions,
      herbs: form.herbs
        .filter((h) => h.herbName)
        .map((h, idx) => ({
          herb_id: h.herbId || null,
          herb_name: h.herbName,
          dosage: h.dosage,
          role: h.role,
          sort_order: idx,
        })),
    };
    if (isEdit.value) {
      await formulaApi.update(editId.value, payload);
    } else {
      await formulaApi.create(payload);
    }
    uni.showToast({ title: '保存成功', icon: 'success' });
    showCreateModal.value = false;
    resetForm();
    loadFormulas();
  } catch (e) {
    uni.showToast({ title: '保存失败', icon: 'none' });
  }
}

onMounted(() => {
  loadFormulas();
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

.formula-list {
  padding: 0 24rpx;

  .formula-item {
    background: #fff;
    border-radius: 24rpx;
    padding: 32rpx;
    margin-bottom: 24rpx;

    .formula-name {
      font-size: 32rpx;
      font-weight: bold;
      color: #333;
      display: block;
      margin-bottom: 12rpx;
    }

    .formula-category {
      display: inline-block;
      padding: 6rpx 20rpx;
      border-radius: 8rpx;
      font-size: 22rpx;
      background: #F0F8FF;
      color: #4169E1;
      margin-bottom: 12rpx;
    }

    .formula-indications {
      display: block;
      font-size: 26rpx;
      color: #666;
      margin-bottom: 16rpx;
      line-height: 1.6;
    }

    .formula-herbs {
      display: flex;
      flex-wrap: wrap;
      gap: 12rpx;
      margin-bottom: 24rpx;

      .herb-tag {
        padding: 6rpx 16rpx;
        border-radius: 8rpx;
        font-size: 22rpx;
        background: #F0FFF0;
        color: #2B9939;
      }
    }

    .formula-actions {
      display: flex;
      gap: 16rpx;

      .action-btn {
        flex: 1;
        height: 64rpx;
        background: #2B9939;
        color: #fff;
        border-radius: 16rpx;
        font-size: 26rpx;

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

      .form-input, .form-textarea, .picker-value, .picker-small {
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

      .picker-value, .picker-small {
        line-height: 80rpx;
        color: #999;
      }

      .picker-small {
        width: 120rpx;
        text-align: center;
        padding: 0;
      }

      .herb-input-row {
        display: flex;
        align-items: center;
        gap: 12rpx;
        margin-bottom: 12rpx;

        .flex-1 {
          flex: 1;
        }

        .small {
          width: 120rpx;
          padding: 0 12rpx;
        }

        .delete-text {
          font-size: 24rpx;
          color: #F44336;
        }
      }

      .add-herb-btn {
        width: 100%;
        height: 64rpx;
        background: #f5f5f5;
        color: #2B9939;
        border-radius: 16rpx;
        font-size: 26rpx;
        margin-top: 12rpx;
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
