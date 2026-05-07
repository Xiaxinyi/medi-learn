<template>
  <view class="container">
    <!-- 搜索栏 -->
    <view class="search-bar">
      <input
        class="search-input"
        v-model="keyword"
        placeholder="搜索手机号或昵称"
        @confirm="loadUsers"
      />
      <button class="search-btn" @click="loadUsers">搜索</button>
    </view>

    <!-- 筛选标签 -->
    <view class="filter-tabs">
      <text
        class="tab-item"
        :class="{ active: roleFilter === '' }"
        @click="setRoleFilter('')"
      >全部</text>
      <text
        class="tab-item"
        :class="{ active: roleFilter === 'user' }"
        @click="setRoleFilter('user')"
      >普通用户</text>
      <text
        class="tab-item"
        :class="{ active: roleFilter === 'admin' }"
        @click="setRoleFilter('admin')"
      >管理员</text>
    </view>

    <!-- 用户列表 -->
    <view class="user-list">
      <view class="user-item" v-for="user in users" :key="user.id">
        <view class="user-main">
          <text class="user-name">{{ user.nickname || '未设置昵称' }}</text>
          <text class="user-phone">{{ user.phone }}</text>
        </view>
        <view class="user-meta">
          <text class="role-tag" :class="user.role">{{ user.role === 'admin' ? '管理员' : '用户' }}</text>
          <text class="status-tag" :class="user.status === 1 ? 'normal' : 'disabled'">
            {{ user.status === 1 ? '正常' : '禁用' }}
          </text>
        </view>
        <view class="user-actions">
          <view class="action-btn" :class="{ disabled: savingUserId === user.id }" @click="toggleRole(user)">
            <text v-if="savingUserId === user.id" class="btn-loading">处理中...</text>
            <text v-else>{{ user.role === 'admin' ? '设为用户' : '设为管理' }}</text>
          </view>
          <view class="action-btn" :class="{ warn: user.status === 1, disabled: savingUserId === user.id }" @click="toggleStatus(user)">
            <text v-if="savingUserId === user.id" class="btn-loading">处理中...</text>
            <text v-else>{{ user.status === 1 ? '禁用' : '启用' }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view class="empty-state" v-if="users.length === 0 && !loading">
      <text>暂无用户数据</text>
    </view>

    <!-- 添加用户按钮 -->
    <button class="fab-btn" @click="showCreateModal = true">+</button>

    <!-- 创建用户弹窗 -->
    <view class="modal-mask" v-if="showCreateModal" @click="showCreateModal = false">
      <view class="modal-content" @click.stop>
        <text class="modal-title">创建用户</text>
        <view class="form-body">
          <view class="form-item">
            <text class="form-label">手机号</text>
            <input class="form-input" v-model="newUser.phone" placeholder="请输入手机号" maxlength="11" />
          </view>
          <view class="form-item">
            <text class="form-label">昵称</text>
            <input class="form-input" v-model="newUser.nickname" placeholder="请输入昵称" />
          </view>
          <view class="form-item">
            <text class="form-label">密码（可选）</text>
            <input class="form-input" v-model="newUser.password" placeholder="留空则无密码" password />
          </view>
          <view class="form-item">
            <text class="form-label">角色</text>
            <view class="radio-group">
              <label class="radio-item">
                <radio value="user" :checked="newUser.role === 'user'" @click="newUser.role = 'user'" />
                <text>普通用户</text>
              </label>
              <label class="radio-item">
                <radio value="admin" :checked="newUser.role === 'admin'" @click="newUser.role = 'admin'" />
                <text>管理员</text>
              </label>
            </view>
          </view>
        </view>
        <view class="modal-actions">
          <button class="modal-btn cancel" @click="showCreateModal = false">取消</button>
          <button class="modal-btn confirm" @click="createUser">确定</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { adminApi } from '@/api';

const users = ref<any[]>([]);
const loading = ref(false);
const savingUserId = ref<number | null>(null);
const keyword = ref('');
const roleFilter = ref('');
const showCreateModal = ref(false);
const newUser = ref({
  phone: '',
  nickname: '',
  password: '',
  role: 'user',
});

function requestDirect(url: string, method: string, data?: any): Promise<any> {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token');
    uni.request({
      url: (process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : 'https://medi-learn-backend.onrender.com') + url,
      method: method as any,
      data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
      },
      success: (res: any) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(res.data);
        }
      },
      fail: reject,
    });
  });
}

async function loadUsers() {
  loading.value = true;
  try {
    const params: any = {};
    if (roleFilter.value) params.role = roleFilter.value;
    if (keyword.value) params.keyword = keyword.value;
    const query = Object.entries(params)
      .filter(([, v]) => v !== undefined && v !== null)
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
      .join('&');
    const url = '/api/admin/users' + (query ? '?' + query : '');
    const res = await requestDirect(url, 'GET');
    users.value = res || [];
  } catch (e: any) {
    uni.showToast({ title: e.detail || e.message || '加载失败', icon: 'none' });
  } finally {
    loading.value = false;
  }
}

function setRoleFilter(role: string) {
  roleFilter.value = role;
  loadUsers();
}

async function toggleRole(user: any) {
  if (savingUserId.value) return;
  const newRole = user.role === 'admin' ? 'user' : 'admin';
  savingUserId.value = user.id;
  try {
    await requestDirect(`/api/admin/users/${user.id}/role`, 'PUT', { role: newRole });
    uni.showToast({ title: '修改成功', icon: 'success' });
    loadUsers();
  } catch (e: any) {
    uni.showToast({ title: e.detail || e.message || '操作失败', icon: 'none' });
  } finally {
    savingUserId.value = null;
  }
}

async function toggleStatus(user: any) {
  if (savingUserId.value) return;
  const newStatus = user.status === 1 ? 0 : 1;
  savingUserId.value = user.id;
  try {
    await requestDirect(`/api/admin/users/${user.id}/status`, 'PUT', { status: newStatus });
    uni.showToast({ title: '修改成功', icon: 'success' });
    loadUsers();
  } catch (e: any) {
    uni.showToast({ title: e.detail || e.message || '操作失败', icon: 'none' });
  } finally {
    savingUserId.value = null;
  }
}

async function createUser() {
  if (!newUser.value.phone || !newUser.value.nickname) {
    uni.showToast({ title: '请填写完整信息', icon: 'none' });
    return;
  }
  try {
    await requestDirect('/api/admin/users', 'POST', newUser.value);
    uni.showToast({ title: '创建成功', icon: 'success' });
    showCreateModal.value = false;
    newUser.value = { phone: '', nickname: '', password: '', role: 'user' };
    loadUsers();
  } catch (e: any) {
    uni.showToast({ title: e.detail || e.message || '创建失败', icon: 'none' });
  }
}

onMounted(() => {
  loadUsers();
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

.user-list {
  padding: 0 24rpx;

  .user-item {
    background: #fff;
    border-radius: 24rpx;
    padding: 32rpx;
    margin-bottom: 24rpx;

    .user-main {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16rpx;

      .user-name {
        font-size: 32rpx;
        font-weight: bold;
        color: #333;
      }

      .user-phone {
        font-size: 26rpx;
        color: #999;
      }
    }

    .user-meta {
      display: flex;
      gap: 16rpx;
      margin-bottom: 24rpx;

      .role-tag {
        padding: 6rpx 20rpx;
        border-radius: 8rpx;
        font-size: 22rpx;

        &.admin {
          background: #FFF8F0;
          color: #E67E22;
        }

        &.user {
          background: #F0F8FF;
          color: #4169E1;
        }
      }

      .status-tag {
        padding: 6rpx 20rpx;
        border-radius: 8rpx;
        font-size: 22rpx;

        &.normal {
          background: #F0FFF0;
          color: #2B9939;
        }

        &.disabled {
          background: #FFF0F0;
          color: #F44336;
        }
      }
    }

    .user-actions {
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

        &.disabled {
          opacity: 0.6;
          pointer-events: none;
        }

        .btn-loading {
          font-size: 24rpx;
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
    width: 80%;
    background: #fff;
    border-radius: 24rpx;
    padding: 48rpx;

    .modal-title {
      display: block;
      font-size: 36rpx;
      font-weight: bold;
      color: #333;
      text-align: center;
      margin-bottom: 32rpx;
    }

    .form-item {
      margin-bottom: 24rpx;

      .form-label {
        display: block;
        font-size: 28rpx;
        color: #333;
        margin-bottom: 12rpx;
      }

      .form-input {
        height: 80rpx;
        background: #f5f5f5;
        border-radius: 16rpx;
        padding: 0 24rpx;
        font-size: 28rpx;
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
    }

    .modal-actions {
      display: flex;
      gap: 24rpx;
      margin-top: 32rpx;

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
