<template>
  <Head class="head"/>
  <div class="main-container">
    <!-- 左侧用户列表 -->
    <user-list
      :selected-user="selectedUser"
      @user-selected="handleUserSelected"
      class="left-panel"
    />

    <!-- 右侧聊天区域 -->
    <chat-content
      v-if="selectedUser"
      :current-user="selectedUser"
      :messages="currentMessages"
      @send-message="handleNewMessage"
      class="right-panel"
    />

    <!-- 未选择用户时的提示 -->
    <div v-else class="empty-state">
      <div class="empty-content">
        <p class="empty-text">请从左侧选择聊天对象开始对话</p>
      </div>
    </div>
  </div>
</template>

<script>
import UserList from './chat.vue'
import ChatContent from './chatcontent.vue'
import Head from '../../components/Head.vue'
export default {
  components: {
    Head,
    UserList,
    ChatContent
  },
  data() {
    return {
      selectedUser: null,
      // 模拟不同用户的聊天记录
      allMessages: {
        1: [
          {
            content: '你好呀！',
            time: new Date(Date.now() - 3600000),
            isSelf: false
          },
          {
            content: '你好！有什么可以帮助你的？',
            time: new Date(),
            isSelf: true
          }
        ],
        2: [
          {
            content: '明天一起吃饭吗？',
            time: new Date(Date.now() - 7200000),
            isSelf: false
          }
        ]
      }
    }
  }
}
</script>

<style scoped>
.head{
  height:10vh
}
.main-container {
  display: flex;
  height: 90vh;
  background-color: #ffffff;
}

.left-panel {
  flex: 0 0 260px;
  border-right: 1px solid #e6e6e6;

}

.right-panel {
  flex: 1;
  min-width: 400px;
}

.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
}

.empty-content {
  text-align: center;
}

.empty-image {
  width: 200px;
  opacity: 0.6;
  margin-bottom: 20px;
}

.empty-text {
  color: #999;
  font-size: 16px;
}
</style>