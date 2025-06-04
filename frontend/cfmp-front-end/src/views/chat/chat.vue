<template>
  <div class="user-list-container">
    <!-- 标题栏 -->
    <div class="list-header">
      <h2 class="title">消息</h2>
    </div>

    <!-- 用户列表 -->
    <div class="user-list">
      <div
        v-for="user in userList"
        :key="user.id"
        class="user-item"
        @click="selectUser(user)"
      >
        <!-- 用户头像 -->
        <div class="avatar">
          <img :src="user.avatar" alt="用户头像">
        </div>

        <!-- 用户信息 -->
        <div class="user-info">
          <div class="info-top">
            <span class="username">{{ user.name }}</span>
            <span class="time">{{ user.lastTime }}</span>
          </div>
          <div class="info-bottom">
            <p class="last-message">{{ user.lastMessage }}</p>
            <div v-if="user.unread > 0" class="unread-count">
              {{ user.unread > 99 ? '99+' : user.unread }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserList',
  data() {
    return {
      userList: [
        {
          id: 1,
          name: '张三',
          avatar: 'https://via.placeholder.com/50',
          lastMessage: '你好，最近怎么样？',
          lastTime: '10:30',
          unread: 2
        },
        {
          id: 2,
          name: '李四',
          avatar: 'https://via.placeholder.com/50',
          lastMessage: '明天一起吃饭吗？',
          lastTime: '昨天',
          unread: 0
        },
        // 可以继续添加更多测试用户
      ]
    }
  },
  methods: {
    selectUser(user) {
      // 处理用户选择事件
      console.log('Selected user:', user)
    }
  }
}
</script>

<style scoped>
.user-list-container {
  width: 260px;
  height: 100px;
  border-right: 1px solid #e6e6e6;
  background-color: #ffffff;
}

.list-header {
  padding: 20px;
  border-bottom: 1px solid #e6e6e6;
}

.title {
  margin: 0;
  font-size: 16px;
  font-weight: normal;
}

.user-list {
  height: calc(90vh - 61px);
  overflow-y: auto;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-item:hover {
  background-color: #f5f5f5;
}

.avatar {
  margin-right: 12px;
}

.avatar img {
  width: 45px;
  height: 45px;
  border-radius: 6px;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.info-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.username {
  font-size: 14px;
  color: #000;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.time {
  font-size: 12px;
  color: #999;
}

.info-bottom {
  display: flex;
  justify-content: space-between;
}

.last-message {
  margin: 0;
  font-size: 12px;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.unread-count {
  background-color: #f56c6c;
  color: white;
  font-size: 12px;
  min-width: 18px;
  height: 18px;
  line-height: 18px;
  border-radius: 9px;
  text-align: center;
  padding: 0 4px;
  margin-left: 8px;
}
</style>