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
          :key="option.option_key"
          :class="{
            selected: selectedAnswers.includes(option.option_key),
            correct: showResult && currentQuestion.correctAnswers.includes(option.option_key),
            wrong: showResult && selectedAnswers.includes(option.option_key) && !currentQuestion.correctAnswers.includes(option.option_key),
          }"
          @click="selectOption(option.option_key)"
        >
          <text class="option-key">{{ option.option_key }}</text>
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

    <!-- 空状态 -->
    <view class="empty-state" v-else>
      <text class="empty-text">暂无练习题</text>
      <text class="empty-subtext">您已完成所有题目，请稍后再来</text>
    </view>

    <!-- 底部操作栏 -->
    <view class="bottom-bar" v-if="currentQuestion">
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
import { examApi } from '@/api';
import type { Question } from '@/types';

const questions = ref<Question[]>([]);
const currentIndex = ref(0);
const selectedAnswers = ref<string[]>([]);
const showResult = ref(false);
const isCorrect = ref(false);
const score = ref(0);
const answersHistory = ref<{ questionId: string; answers: string[] }[]>([]);

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

  answersHistory.value.push({
    questionId: String(currentQuestion.value.id),
    answers: [...selected],
  });

  showResult.value = true;
}

function nextQuestion() {
  currentIndex.value++;
  selectedAnswers.value = [];
  showResult.value = false;
  isCorrect.value = false;
}

async function finishPractice() {
  try {
    await examApi.submit({
      answers: answersHistory.value.map(a => ({
        question_id: a.questionId,
        answers: a.answers,
      })),
    });
  } catch (e) {
    console.error('提交练习结果失败', e);
  }

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
    const res = await examApi.practice();
    questions.value = res;
  } catch (e) {
    uni.showToast({ title: '获取题目失败', icon: 'none' });
    questions.value = [];
  }
}

loadQuestions();
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 24rpx;
  padding-bottom: 280rpx;
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120rpx 48rpx;
  background: #fff;
  border-radius: 24rpx;
  margin-top: 48rpx;

  .empty-text {
    font-size: 32rpx;
    color: #333;
    font-weight: bold;
    margin-bottom: 16rpx;
  }

  .empty-subtext {
    font-size: 28rpx;
    color: #999;
  }
}

.bottom-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 100rpx;
  padding: 24rpx 48rpx;
  background: #fff;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.06);

  .submit-btn, .next-btn, .finish-btn {
    height: 88rpx;
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
