<template>
  <view class="container">
    <!-- 题目卡片 -->
    <view class="question-card" v-if="currentQuestion">
      <view class="question-header">
        <text class="question-type">{{ currentQuestion.type === 'single' ? '单选题' : '多选题' }}</text>
        <text class="question-progress">{{ currentIndex + 1 }}/{{ questions.length }}</text>
      </view>

      <text class="question-content">{{ currentQuestion.content }}</text>

      <view class="options-list">
        <view
          class="option-item"
          v-for="option in currentQuestion.options"
          :key="option.id"
          :class="{
            selected: selectedAnswers.includes(option.id),
            correct: showResult && currentQuestion.correctAnswers.includes(option.id),
            wrong: showResult && selectedAnswers.includes(option.id) && !currentQuestion.correctAnswers.includes(option.id),
          }"
          @click="selectOption(option.id)"
        >
          <text class="option-key">{{ option.id }}</text>
          <text class="option-content">{{ option.content }}</text>
        </view>
      </view>

      <!-- 答案解析 -->
      <view class="explanation" v-if="showResult">
        <view class="explanation-title">
          <text>答案解析</text>
          <text :class="isCorrect ? 'correct-text' : 'wrong-text'">
            {{ isCorrect ? '回答正确 ✓' : '回答错误 ✗' }}
          </text>
        </view>
        <text class="explanation-content">{{ currentQuestion.explanation }}</text>
        <text class="correct-answer">正确答案：{{ currentQuestion.correctAnswers.join('、') }}</text>
      </view>
    </view>

    <!-- 底部操作栏 -->
    <view class="bottom-bar">
      <button
        class="submit-btn"
        v-if="!showResult && selectedAnswers.length > 0"
        @click="submitAnswer"
      >
        提交答案
      </button>
      <button
        class="next-btn"
        v-if="showResult && currentIndex < questions.length - 1"
        @click="nextQuestion"
      >
        下一题
      </button>
      <button
        class="finish-btn"
        v-if="showResult && currentIndex === questions.length - 1"
        @click="finishPractice"
      >
        完成练习
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { questionApi } from '@/api';
import type { Question } from '@/types';

const questions = ref<Question[]>([]);
const currentIndex = ref(0);
const selectedAnswers = ref<string[]>([]);
const showResult = ref(false);
const isCorrect = ref(false);
const score = ref(0);

const currentQuestion = computed(() => questions.value[currentIndex.value] || null);

function selectOption(optionId: string) {
  if (showResult.value) return;

  if (currentQuestion.value?.type === 'single') {
    selectedAnswers.value = [optionId];
  } else {
    const index = selectedAnswers.value.indexOf(optionId);
    if (index > -1) {
      selectedAnswers.value.splice(index, 1);
    } else {
      selectedAnswers.value.push(optionId);
    }
  }
}

function submitAnswer() {
  if (!currentQuestion.value) return;

  const correct = currentQuestion.value.correctAnswers;
  const selected = selectedAnswers.value;

  if (currentQuestion.value.type === 'single') {
    isCorrect.value = selected.length === 1 && selected[0] === correct[0];
  } else {
    const allCorrect = correct.every(c => selected.includes(c));
    const noWrong = selected.every(s => correct.includes(s));
    isCorrect.value = allCorrect && noWrong;
  }

  if (isCorrect.value) {
    score.value += currentQuestion.value.type === 'single' ? 10 : 15;
  }

  showResult.value = true;
}

function nextQuestion() {
  currentIndex.value++;
  selectedAnswers.value = [];
  showResult.value = false;
  isCorrect.value = false;
}

function finishPractice() {
  uni.showModal({
    title: '练习完成',
    content: `本次练习得分：${score.value}分`,
    showCancel: false,
    success: () => {
      uni.navigateBack();
    },
  });
}

async function loadQuestions() {
  try {
    const res = await questionApi.random(10);
    questions.value = res;
  } catch (e) {
    questions.value = [
      {
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
      },
      {
        id: '2',
        type: 'multiple',
        content: '下列哪些是黄芪的功效？（多选）',
        options: [
          { id: 'A', content: '补气升阳' },
          { id: 'B', content: '固表止汗' },
          { id: 'C', content: '利水消肿' },
          { id: 'D', content: '托毒生肌' },
        ],
        correctAnswers: ['A', 'B', 'C', 'D'],
        explanation: '黄芪性味甘，微温，归脾、肺经，具有补气升阳、固表止汗、利水消肿、生津养血、行滞通痹、托毒排脓、敛疮生肌的功效。',
        difficulty: 'medium',
        tags: ['黄芪', '功效'],
      },
      {
        id: '3',
        type: 'single',
        content: '当归主治什么病症？',
        options: [
          { id: 'A', content: '风寒感冒' },
          { id: 'B', content: '血虚萎黄' },
          { id: 'C', content: '湿热黄疸' },
          { id: 'D', content: '咽喉肿痛' },
        ],
        correctAnswers: ['B'],
        explanation: '当归性味甘、辛，温，归肝、心、脾经，具有补血活血、调经止痛、润肠通便的功效，主治血虚萎黄、眩晕心悸、月经不调、经闭痛经等。',
        difficulty: 'easy',
        tags: ['当归', '主治'],
      },
    ];
  }
}

loadQuestions();
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 24rpx;
  padding-bottom: 160rpx;
}

.question-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 32rpx;

  .question-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 24rpx;

    .question-type {
      font-size: 26rpx;
      color: #2B9939;
      padding: 8rpx 20rpx;
      background: #E8F5E9;
      border-radius: 8rpx;
    }

    .question-progress {
      font-size: 26rpx;
      color: #999;
    }
  }

  .question-content {
    font-size: 32rpx;
    color: #333;
    line-height: 1.6;
    margin-bottom: 32rpx;
    display: block;
  }
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;

  .option-item {
    display: flex;
    align-items: center;
    gap: 20rpx;
    padding: 28rpx;
    background: #f8f8f8;
    border-radius: 16rpx;
    border: 2rpx solid transparent;

    &.selected {
      border-color: #2B9939;
      background: #E8F5E9;
    }

    &.correct {
      border-color: #4CAF50;
      background: #E8F5E9;
    }

    &.wrong {
      border-color: #F44336;
      background: #FFEBEE;
    }

    .option-key {
      width: 56rpx;
      height: 56rpx;
      border-radius: 50%;
      background: #e0e0e0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26rpx;
      font-weight: bold;
      color: #666;
      flex-shrink: 0;
    }

    .option-content {
      font-size: 28rpx;
      color: #333;
      line-height: 1.5;
    }
  }
}

.explanation {
  margin-top: 32rpx;
  padding: 24rpx;
  background: #FFF8E1;
  border-radius: 16rpx;

  .explanation-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;

    text:first-child {
      font-size: 30rpx;
      font-weight: bold;
      color: #333;
    }

    .correct-text {
      color: #4CAF50;
      font-size: 26rpx;
    }

    .wrong-text {
      color: #F44336;
      font-size: 26rpx;
    }
  }

  .explanation-content {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
    display: block;
    margin-bottom: 12rpx;
  }

  .correct-answer {
    font-size: 26rpx;
    color: #4CAF50;
    font-weight: bold;
  }
}

.bottom-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 24rpx 48rpx;
  background: #fff;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.06);

  .submit-btn, .next-btn, .finish-btn {
    height: 88rpx;
    line-height: 88rpx;
    border-radius: 44rpx;
    font-size: 32rpx;
    color: #fff;
  }

  .submit-btn {
    background: #2B9939;
  }

  .next-btn {
    background: #2196F3;
  }

  .finish-btn {
    background: #FF9800;
  }
}
</style>
