<template>
  <view class="container">
    <view class="form-card">
      <view class="form-item">
        <text class="label required">草药名称</text>
        <input type="text" v-model="form.name" placeholder="请输入草药名称" />
      </view>

      <view class="form-item">
        <text class="label">拉丁名</text>
        <input type="text" v-model="form.latinName" placeholder="请输入拉丁名" />
      </view>

      <view class="form-item">
        <text class="label">别名</text>
        <input type="text" v-model="aliasInput" placeholder="多个别名用顿号分隔" />
      </view>

      <view class="form-item">
        <text class="label required">分类</text>
        <picker mode="selector" :range="categories" :value="categoryIndex" @change="onCategoryChange">
          <view class="picker-value">{{ form.category || '请选择分类' }}</view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label">属性标签</text>
        <view class="tag-selector">
          <view
            class="tag-item"
            v-for="attr in allAttributes"
            :key="attr.id"
            :class="{ selected: selectedAttributes.includes(attr.id) }"
            :style="selectedAttributes.includes(attr.id) ? { backgroundColor: attr.color, color: '#fff' } : {}"
            @click="toggleAttribute(attr.id)"
          >
            {{ attr.name }}
          </view>
        </view>
      </view>

      <view class="form-item">
        <text class="label required">功效</text>
        <textarea v-model="form.efficacy" placeholder="请输入功效" />
      </view>

      <view class="form-item">
        <text class="label required">主治</text>
        <textarea v-model="form.indications" placeholder="请输入主治" />
      </view>

      <view class="form-item">
        <text class="label">用法用量</text>
        <input type="text" v-model="form.dosage" placeholder="请输入用法用量" />
      </view>

      <view class="form-item">
        <text class="label">禁忌</text>
        <textarea v-model="form.contraindications" placeholder="请输入禁忌" />
      </view>

      <view class="form-item">
        <text class="label">产地</text>
        <input type="text" v-model="form.origin" placeholder="请输入产地" />
      </view>

      <view class="form-item">
        <text class="label">图片</text>
        <view class="image-upload">
          <view class="image-item" v-for="(img, index) in form.images" :key="index">
            <image :src="img" mode="aspectFill" />
            <text class="delete-btn" @click="removeImage(index)">×</text>
          </view>
          <view class="upload-btn" @click="chooseImage" v-if="form.images.length < 9">
            <text>+</text>
          </view>
        </view>
      </view>
    </view>

    <button class="submit-btn" @click="submit">保存</button>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { herbApi } from '@/api';

const herbId = ref<string>('');
const isEdit = ref(false);

const categories = ['解表药', '清热药', '泻下药', '祛风湿药', '化湿药', '利水渗湿药', '温里药', '理气药', '消食药', '驱虫药', '止血药', '活血化瘀药', '化痰止咳平喘药', '安神药', '平肝息风药', '开窍药', '补益药', '收涩药', '涌吐药', '攻毒杀虫止痒药', '拔毒化腐生肌药'];
const categoryIndex = ref(0);

const allAttributes = ref([
  { id: '1', name: '寒', color: '#2196F3' },
  { id: '2', name: '热', color: '#F44336' },
  { id: '3', name: '温', color: '#FF5722' },
  { id: '4', name: '凉', color: '#00BCD4' },
  { id: '5', name: '平', color: '#9E9E9E' },
  { id: '6', name: '酸', color: '#E91E63' },
  { id: '7', name: '苦', color: '#795548' },
  { id: '8', name: '甘', color: '#8BC34A' },
  { id: '9', name: '辛', color: '#FF9800' },
  { id: '10', name: '咸', color: '#607D8B' },
  { id: '11', name: '升', color: '#E91E63' },
  { id: '12', name: '降', color: '#3F51B5' },
  { id: '13', name: '浮', color: '#FFEB3B' },
  { id: '14', name: '沉', color: '#673AB7' },
  { id: '15', name: '补', color: '#4CAF50' },
  { id: '16', name: '泻', color: '#F44336' },
  { id: '17', name: '散', color: '#00BCD4' },
  { id: '18', name: '收', color: '#9C27B0' },
  { id: '19', name: '燥', color: '#FF5722' },
  { id: '20', name: '润', color: '#2196F3' },
]);

const selectedAttributes = ref<string[]>([]);
const aliasInput = ref('');

const form = reactive({
  name: '',
  latinName: '',
  aliases: [] as string[],
  category: '',
  attributes: [] as string[],
  efficacy: '',
  indications: '',
  dosage: '',
  contraindications: '',
  origin: '',
  images: [] as string[],
});

function onCategoryChange(e: any) {
  categoryIndex.value = e.detail.value;
  form.category = categories[e.detail.value];
}

function toggleAttribute(id: string) {
  const index = selectedAttributes.value.indexOf(id);
  if (index > -1) {
    selectedAttributes.value.splice(index, 1);
  } else {
    selectedAttributes.value.push(id);
  }
}

function chooseImage() {
  uni.chooseImage({
    count: 9 - form.images.length,
    success: (res: any) => {
      form.images.push(...res.tempFilePaths);
    },
  });
}

function removeImage(index: number) {
  form.images.splice(index, 1);
}

async function submit() {
  if (!form.name || !form.efficacy || !form.indications) {
    uni.showToast({ title: '请填写必填项', icon: 'none' });
    return;
  }

  if (aliasInput.value) {
    form.aliases = aliasInput.value.split('、').map(s => s.trim()).filter(Boolean);
  }
  form.attributes = selectedAttributes.value;

  try {
    const payload = {
      name: form.name,
      latin_name: form.latinName,
      aliases: form.aliases,
      category: form.category,
      attributes: form.attributes,
      efficacy: form.efficacy,
      indications: form.indications,
      dosage: form.dosage,
      contraindications: form.contraindications,
      origin: form.origin,
      images: form.images,
    };
    if (isEdit.value) {
      await herbApi.update(herbId.value, payload);
    } else {
      await herbApi.create(payload);
    }
    uni.showToast({ title: '保存成功', icon: 'success' });
    setTimeout(() => {
      uni.navigateBack();
    }, 1500);
  } catch (e) {
    uni.showToast({ title: '保存失败', icon: 'none' });
  }
}

onMounted(() => {
  const pages = getCurrentPages();
  const current = pages[pages.length - 1] as any;
  if (current?.options?.id) {
    herbId.value = current.options.id;
    isEdit.value = true;
    herbApi.detail(herbId.value).then((res: any) => {
      form.name = res.name || '';
      form.latinName = res.latin_name || '';
      form.aliases = res.aliases || [];
      aliasInput.value = form.aliases.join('、');
      form.category = res.category || '';
      categoryIndex.value = categories.indexOf(form.category);
      form.efficacy = res.efficacy || '';
      form.indications = res.indications || '';
      form.dosage = res.dosage || '';
      form.contraindications = res.contraindications || '';
      form.origin = res.origin || '';
      form.images = res.images || [];
      selectedAttributes.value = res.attributes || [];
    }).catch(() => {
      uni.showToast({ title: '加载失败', icon: 'none' });
    });
  }
});
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

    input, textarea, .picker-value {
      background: #f8f8f8;
      border-radius: 12rpx;
      padding: 20rpx 24rpx;
      font-size: 28rpx;
      color: #333;
    }

    textarea {
      height: 160rpx;
      width: 100%;
    }

    .picker-value {
      color: #999;
    }
  }
}

.tag-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;

  .tag-item {
    padding: 12rpx 24rpx;
    border-radius: 12rpx;
    background: #f0f0f0;
    font-size: 26rpx;
    color: #666;
    border: 2rpx solid transparent;

    &.selected {
      border-color: #fff;
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
</style>
