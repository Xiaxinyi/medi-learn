<template>
  <view class="container">
    <view class="search-bar">
      <input class="search-input" v-model="keyword" placeholder="搜索题目内容" @confirm="loadQuestions" />
      <button class="search-btn" @click="loadQuestions">搜索</button>
    </view>

    <view class="filter-tabs">
      <text class="tab-item" :class="{ active: difficultyFilter === '' }" @click="setDifficultyFilter('')">全部</text>
      <text class="tab-item" :class="{ active: difficultyFilter === 'easy' }" @click="setDifficultyFilter('easy')">简单</text>
      <text class="tab-item" :class="{ active: difficultyFilter === 'medium' }" @click="setDifficultyFilter('medium')">中等</text>
      <text class="tab-item" :class="{ active: difficultyFilter === 'hard' }" @click="setDifficultyFilter('hard')">困难</text>
    </view>

    <view class="question-list">
      <view class="question-item" v-for="q in questions" :key="q.id">
        <text class="question-content">{{ q.content }}</text>
        <view class="question-meta">
          <text class="difficulty-tag" :class="q.difficulty">{{ difficultyText(q.difficulty) }}</text>
          <text class="type-tag">{{ q.type === 'single' ? '单选' : '多选' }}</text>
        </view>
        <view class="options-preview">
          <text v-for="(opt, idx) in q.options" :key="opt.id" class="option-text" :class="{ correct: opt.is_correct }">
            {{ ['A', 'B', 'C', 'D'][idx] }}. {{ opt.content }}
          </text>
        </view>
        <view class="question-actions">
          <button class="action-btn" @click="editQuestion(q)">编辑</button>
          <button class="action-btn warn" @click="deleteQuestion(q.id)">删除</button>
        </view>
      </view>
    </view>

    <view class="empty-state" v-if="questions.length === 0 && !loading">
      <text>暂无试题数据</text>
    </view>

    <button class="fab-btn" @click="openCreateModal">+</button>

    <view class="modal-mask" v-if="showCreateModal" @click="showCreateModal = false">
      <view class="modal-content" @click.stop>
        <text class="modal-title">{{ isEdit ? '编辑试题' : '创建试题' }}</text>
        <view class="form-body">
          <view class="form-item">
            <text class="form-label">题目内容</text>
            <view class="form-input-wrap">
              <textarea class="form-textarea flex-1" v-model="form.content" placeholder="请输入题目内容或知识点主题" />
              <button class="ai-btn" @click="generateByAI" :disabled="aiLoading || !form.content">
                {{ aiLoading ? '生成中...' : 'AI生成' }}
              </button>
            </view>
          </view>
          <view class="form-item">
            <text class="form-label">题型</text>
            <view class="radio-group">
              <label class="radio-item">
                <radio value="single" :checked="form.type === 'single'" @click="form.type = 'single'" />
                <text>单选题</text>
              </label>
              <label class="radio-item">
                <radio value="multiple" :checked="form.type === 'multiple'" @click="form.type = 'multiple'" />
                <text>多选题</text>
              </label>
            </view>
          </view>
          <view class="form-item">
            <text class="form-label">选项</text>
            <view v-for="(opt, idx) in form.options" :key="idx" class="option-input-row">
              <text class="option-label">{{ ['A', 'B', 'C', 'D'][idx] }}</text>
              <input class="form-input flex-1" v-model="opt.content" :placeholder="'选项' + ['A', 'B', 'C', 'D'][idx]" />
              <checkbox :checked="form.correctAnswers.includes(opt.id)" @click="toggleCorrect(opt.id)" />
            </view>
          </view>
          <view class="form-item">
            <text class="form-label">解析</text>
            <textarea class="form-textarea" v-model="form.explanation" placeholder="请输入答案解析" />
          </view>
          <view class="form-item">
            <text class="form-label">难度</text>
            <picker mode="selector" :range="difficulties" :value="difficultyIndex" @change="onDifficultyChange">
              <view class="picker-value">{{ form.difficulty ? difficultyText(form.difficulty) : '请选择难度' }}</view>
            </picker>
          </view>
          <view class="form-item">
            <text class="form-label">标签（用逗号分隔）</text>
            <input class="form-input" v-model="tagInput" placeholder="如：解表药,清热药" />
          </view>
        </view>
        <view class="modal-actions">
          <button class="modal-btn cancel" @click="showCreateModal = false">取消</button>
          <button class="modal-btn confirm" @click="submitQuestion">确定</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { questionApi } from '@/api';

const aiLoading = ref(false);

const questions = ref<any[]>([]);
const loading = ref(false);
const keyword = ref('');
const difficultyFilter = ref('');
const showCreateModal = ref(false);
const isEdit = ref(false);
const editId = ref('');

const difficulties = ['简单', '中等', '困难'];
const difficultyValues = ['easy', 'medium', 'hard'];
const difficultyIndex = ref(0);

const tagInput = ref('');

const form = reactive({
  type: 'single' as 'single' | 'multiple',
  content: '',
  options: [
    { id: 'A', content: '' },
    { id: 'B', content: '' },
    { id: 'C', content: '' },
    { id: 'D', content: '' },
  ],
  correctAnswers: [] as string[],
  explanation: '',
  difficulty: 'easy' as 'easy' | 'medium' | 'hard',
  tags: [] as string[],
});

function difficultyText(d: string) {
  const map: Record<string, string> = { easy: '简单', medium: '中等', hard: '困难' };
  return map[d] || d;
}

async function loadQuestions() {
  loading.value = true;
  try {
    const params: any = {};
    if (difficultyFilter.value) params.difficulty = difficultyFilter.value;
    if (keyword.value) params.search = keyword.value;
    const res = await questionApi.list(params);
    questions.value = res.items || [];
  } catch (e) {
    uni.showToast({ title: '加载失败', icon: 'none' });
  } finally {
    loading.value = false;
  }
}

function setDifficultyFilter(d: string) {
  difficultyFilter.value = d;
  loadQuestions();
}

function openCreateModal() {
  resetForm();
  showCreateModal.value = true;
}

function toggleCorrect(id: string) {
  const idx = form.correctAnswers.indexOf(id);
  if (idx > -1) {
    form.correctAnswers.splice(idx, 1);
  } else {
    if (form.type === 'single') {
      form.correctAnswers = [id];
    } else {
      form.correctAnswers.push(id);
    }
  }
}

function onDifficultyChange(e: any) {
  difficultyIndex.value = e.detail.value;
  form.difficulty = difficultyValues[e.detail.value] as any;
}

function editQuestion(q: any) {
  isEdit.value = true;
  editId.value = q.id;
  form.type = q.type;
  form.content = q.content;
  form.options = q.options.map((o: any, idx: number) => ({
    id: o.option_key || ['A', 'B', 'C', 'D'][idx],
    content: o.content,
  }));
  form.correctAnswers = q.options
    .filter((o: any) => o.is_correct)
    .map((o: any) => o.option_key);
  form.explanation = q.explanation || '';
  form.difficulty = q.difficulty;
  form.tags = q.tags || [];
  tagInput.value = form.tags.join(',');
  difficultyIndex.value = difficultyValues.indexOf(form.difficulty);
  showCreateModal.value = true;
}

async function deleteQuestion(id: string) {
  uni.showModal({
    title: '确认删除',
    content: '确定要删除这道试题吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await questionApi.delete(id);
          uni.showToast({ title: '删除成功', icon: 'success' });
          loadQuestions();
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
  form.type = 'single';
  form.content = '';
  form.options = [
    { id: 'A', content: '' },
    { id: 'B', content: '' },
    { id: 'C', content: '' },
    { id: 'D', content: '' },
  ];
  form.correctAnswers = [];
  form.explanation = '';
  form.difficulty = 'easy';
  form.tags = [];
  tagInput.value = '';
  difficultyIndex.value = 0;
}

async function generateByAI() {
  if (!form.content) {
    uni.showToast({ title: '请先输入题目内容或知识点主题', icon: 'none' });
    return;
  }
  aiLoading.value = true;
  try {
    const res = await questionApi.generate(form.content);
    if (res.content) form.content = res.content;
    if (res.type) form.type = res.type;
    if (res.options && Array.isArray(res.options)) {
      const keys = ['A', 'B', 'C', 'D'];
      form.options = keys.map((k, idx) => {
        const opt = res.options.find((o: any) => (o.option_key || o.key) === k);
        return {
          id: k,
          content: opt ? (opt.content || '') : '',
        };
      });
      form.correctAnswers = res.options
        .filter((o: any) => o.is_correct || o.isCorrect)
        .map((o: any) => o.option_key || o.key);
    }
    if (res.explanation) form.explanation = res.explanation;
    if (res.difficulty) {
      form.difficulty = res.difficulty;
      difficultyIndex.value = difficultyValues.indexOf(res.difficulty);
    }
    if (res.tags && Array.isArray(res.tags)) {
      form.tags = res.tags;
      tagInput.value = res.tags.join(',');
    }
    uni.showToast({ title: 'AI生成成功', icon: 'success' });
  } catch (e: any) {
    const msg = e?.detail || e?.message || '生成失败';
    uni.showToast({ title: msg, icon: 'none', duration: 3000 });
  } finally {
    aiLoading.value = false;
  }
}

async function submitQuestion() {
  if (!form.content || form.correctAnswers.length === 0) {
    uni.showToast({ title: '请填写题目并选择正确答案', icon: 'none' });
    return;
  }
  try {
    const payload = {
      type: form.type,
      content: form.content,
      options: form.options
        .filter((o) => o.content)
        .map((o, idx) => ({
          option_key: o.id,
          content: o.content,
          is_correct: form.correctAnswers.includes(o.id),
          sort_order: idx,
        })),
      explanation: form.explanation,
      difficulty: form.difficulty,
      tags: tagInput.value.split(',').map((s) => s.trim()).filter(Boolean),
    };
    if (isEdit.value) {
      await questionApi.update(editId.value, payload);
    } else {
      await questionApi.create(payload);
    }
    uni.showToast({ title: '保存成功', icon: 'success' });
    showCreateModal.value = false;
    resetForm();
    loadQuestions();
  } catch (e) {
    uni.showToast({ title: '保存失败', icon: 'none' });
  }
}

onMounted(() => {
  loadQuestions();
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
  background: #fff;
  padding: 0 24rpx 24rpx;
  gap: 16rpx;

  .tab-item {
    padding: 12rpx 32rpx;
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

.question-list {
  padding: 0 24rpx;

  .question-item {
    background: #fff;
    border-radius: 24rpx;
    padding: 32rpx;
    margin-bottom: 24rpx;

    .question-content {
      font-size: 30rpx;
      font-weight: bold;
      color: #333;
      display: block;
      margin-bottom: 16rpx;
    }

    .question-meta {
      display: flex;
      gap: 16rpx;
      margin-bottom: 16rpx;

      .difficulty-tag {
        padding: 6rpx 20rpx;
        border-radius: 8rpx;
        font-size: 22rpx;

        &.easy {
          background: #F0FFF0;
          color: #2B9939;
        }

        &.medium {
          background: #FFF8F0;
          color: #E67E22;
        }

        &.hard {
          background: #FFF0F0;
          color: #F44336;
        }
      }

      .type-tag {
        padding: 6rpx 20rpx;
        border-radius: 8rpx;
        font-size: 22rpx;
        background: #F0F8FF;
        color: #4169E1;
      }
    }

    .options-preview {
      margin-bottom: 24rpx;

      .option-text {
        display: block;
        font-size: 26rpx;
        color: #666;
        padding: 8rpx 0;

        &.correct {
          color: #2B9939;
          font-weight: bold;
        }
      }
    }

    .question-actions {
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

      .form-input-wrap {
        display: flex;
        gap: 16rpx;
        align-items: flex-start;

        .form-textarea {
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
          flex-shrink: 0;
          margin-top: 8rpx;

          &:disabled {
            background: #90CAF9;
          }
        }
      }

      .picker-value {
        line-height: 80rpx;
        color: #999;
      }

      .radio-group {
        display: flex;
        gap: 32rpx;

        .radio-item {
          display: flex;
          align-items: center;
          gap: 8rpx;
          font-size: 28rpx;
          color: #333;
        }
      }

      .option-input-row {
        display: flex;
        align-items: center;
        gap: 12rpx;
        margin-bottom: 12rpx;

        .option-label {
          font-size: 28rpx;
          color: #333;
          font-weight: bold;
          width: 40rpx;
        }

        .flex-1 {
          flex: 1;
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
