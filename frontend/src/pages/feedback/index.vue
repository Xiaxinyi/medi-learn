<template>
  <view class="container">
    <view class="form-card">
      <view class="form-item">
        <text class="label required">反馈类型</text>
        <view class="type-selector">
          <view
            class="type-item"
            v-for="type in feedbackTypes"
            :key="type.value"
            :class="{ active: form.type === type.value }"
            @click="form.type = type.value"
          >
            {{ type.label }}
          </view>
        </view>
      </view>

      <view class="form-item">
        <text class="label required">标题</text>
        <input type="text" v-model="form.title" placeholder="请简要描述问题" />
      </view>

      <view class="form-item">
        <text class="label required">内容</text>
        <textarea v-model="form.content" placeholder="请详细描述您的问题或建议" />
      </view>

      <view class="form-item">
        <text class="label">联系方式</text>
        <input type="text" v-model="form.contact" placeholder="手机号或邮箱（选填）" />
      </view>

      <view class="form-item">
        <text class="label">附件图片</text>
        <view class="image-upload">
          <view class="image-item" v-for="(img, index) in form.images" :key="index">
            <image :src="img" mode="aspectFill" />
            <text class="delete-btn" @click="removeImage(index)">×</text>
          </view>
          <view class="upload-btn" @click="chooseImage" v-if="form.images.length < 6">
            <text>+</text>
          </view>
        </view>
      </view>
    </view>

    <button class="submit-btn" @click="submit">提交反馈</button>

    <!-- 我的反馈 -->
    <view class="my-feedback" v-if="myFeedback.length > 0">
      <view class="section-title">我的反馈</view>
      <view class="feedback-list">
        <view class="feedback-item" v-for="item in myFeedback" :key="item.id">
          <view class="feedback-header">
            <text class="feedback-type">{{ getTypeLabel(item.type) }}</text>
            <text class="feedback-status" :class="item.status">{{ getStatusLabel(item.status) }}</text>
          </view>
          <text class="feedback-title">{{ item.title }}</text>
          <text class="feedback-content">{{ item.content }}</text>
          <view class="admin-reply" v-if="item.adminReply">
            <text class="reply-label">管理员回复：</text>
            <text class="reply-content">{{ item.adminReply }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import type { Feedback } from '@/types';

const feedbackTypes = [
  { value: 'suggestion', label: '功能建议' },
  { value: 'bug', label: 'Bug反馈' },
  { value: 'complaint', label: '投诉' },
  { value: 'other', label: '其他' },
];

const form = reactive({
  type: 'suggestion' as string,
  title: '',
  content: '',
  contact: '',
  images: [] as string[],
});

const myFeedback = ref<Feedback[]>([
  {
    id: '1',
    userId: '1',
    type: 'suggestion',
    title: '希望增加更多草药图片',
    content: '目前草药图片较少，希望能增加高清图片。',
    status: 'resolved',
    adminReply: '感谢您的建议，我们会在下个版本增加更多图片资源。',
  },
]);

function chooseImage() {
  uni.chooseImage({
    count: 6 - form.images.length,
    success: (res: any) => {
      form.images.push(...res.tempFilePaths);
    },
  });
}

function removeImage(index: number) {
  form.images.splice(index, 1);
}

function getTypeLabel(type: string) {
  return feedbackTypes.find(t => t.value === type)?.label || type;
}

function getStatusLabel(status: string) {
  const map: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    resolved: '已解决',
    rejected: '已拒绝',
  };
  return map[status] || status;
}

function submit() {
  if (!form.title || !form.content) {
    uni.showToast({ title: '请填写完整信息', icon: 'none' });
    return;
  }

  uni.showToast({ title: '提交成功', icon: 'success' });
  form.title = '';
  form.content = '';
  form.contact = '';
  form.images = [];
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 24rpx;
  padding-bottom: 48rpx;
}

.form-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 32rpx;

  .form-item {
    margin-bottom: 32rpx;

    .label {
      display: block;
      font-size: 28rpx;
      color: #333;
      margin-bottom: 16rpx;

      &.required::after {
        content: ' *';
        color: #F44336;
      }
    }

    input, textarea {
      background: #f8f8f8;
      border-radius: 12rpx;
      padding: 20rpx 24rpx;
      font-size: 28rpx;
      color: #333;
    }

    textarea {
      height: 200rpx;
      width: 100%;
    }
  }
}

.type-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;

  .type-item {
    padding: 16rpx 32rpx;
    border-radius: 12rpx;
    background: #f0f0f0;
    font-size: 26rpx;
    color: #666;

    &.active {
      background: #2B9939;
      color: #fff;
    }
  }
}

.image-upload {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;

  .image-item {
    position: relative;
    width: 160rpx;
    height: 160rpx;

    image {
      width: 100%;
      height: 100%;
      border-radius: 12rpx;
    }

    .delete-btn {
      position: absolute;
      top: -10rpx;
      right: -10rpx;
      width: 40rpx;
      height: 40rpx;
      background: #F44336;
      color: #fff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28rpx;
    }
  }

  .upload-btn {
    width: 160rpx;
    height: 160rpx;
    border-radius: 12rpx;
    border: 2rpx dashed #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48rpx;
    color: #999;
  }
}

.submit-btn {
  height: 96rpx;
  background: #2B9939;
  color: #fff;
  border-radius: 48rpx;
  font-size: 32rpx;
  margin-top: 32rpx;
}

.my-feedback {
  margin-top: 48rpx;

  .section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
  }

  .feedback-list {
    display: flex;
    flex-direction: column;
    gap: 24rpx;
  }

  .feedback-item {
    background: #fff;
    border-radius: 24rpx;
    padding: 32rpx;

    .feedback-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 16rpx;

      .feedback-type {
        font-size: 24rpx;
        color: #2B9939;
        padding: 6rpx 16rpx;
        background: #E8F5E9;
        border-radius: 8rpx;
      }

      .feedback-status {
        font-size: 24rpx;
        padding: 6rpx 16rpx;
        border-radius: 8rpx;

        &.pending { background: #FFF3E0; color: #FF9800; }
        &.processing { background: #E3F2FD; color: #2196F3; }
        &.resolved { background: #E8F5E9; color: #4CAF50; }
        &.rejected { background: #FFEBEE; color: #F44336; }
      }
    }

    .feedback-title {
      font-size: 30rpx;
      font-weight: bold;
      color: #333;
      display: block;
      margin-bottom: 12rpx;
    }

    .feedback-content {
      font-size: 26rpx;
      color: #666;
      line-height: 1.5;
      display: block;
      margin-bottom: 16rpx;
    }

    .admin-reply {
      background: #f8f8f8;
      padding: 20rpx;
      border-radius: 12rpx;

      .reply-label {
        font-size: 24rpx;
        color: #2B9939;
        font-weight: bold;
        display: block;
        margin-bottom: 8rpx;
      }

      .reply-content {
        font-size: 26rpx;
        color: #666;
      }
    }
  }
}
</style>
