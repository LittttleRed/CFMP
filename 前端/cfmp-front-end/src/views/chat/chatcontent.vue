<template>
  <div class="chat-container">
    <!-- 聊天内容区域 -->
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(message, index) in formattedMessages"
        :key="message.id || index"
        class="message-item"
      >
        <!-- 消息内容 -->
        <div :class="['message-wrapper', message.isSelf ? 'self' : 'other']">
          <!-- 对方头像 -->
          <img v-if="!message.isSelf"
               :src="currentUser.avatar"
               class="avatar"
               alt="头像">

          <!-- 消息主体 -->
          <div class="message-body">
            <!-- 消息气泡 -->
            <div :class="['message-bubble', message.isSelf ? 'self' : 'other']">
              <div class="content">{{ message.content }}</div>
              <div class="meta">
                <span class="time">{{ formatMessageTime(message.timestamp) }}</span>
                <span v-if="message.isSelf" class="status">
                  <span v-if="message.status === 'sending'">🕗</span>
                  <span v-else-if="message.status === 'sent'">✓</span>
                  <span v-else-if="message.status === 'error'">⚠</span>
                </span>
              </div>
            </div>
          </div>

          <!-- 自己头像 -->
          <img v-if="message.isSelf"
               :src="selfAvatar"
               class="avatar"
               alt="我的头像">
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-area">
      <div class="input-box">
        <textarea
          v-model="inputMessage"
          @keydown.enter.exact.prevent="sendMessage"
          @keydown.ctrl.enter.exact="newLine"
          @input="adjustTextareaHeight"
          placeholder="输入消息..."
          rows="1"
          ref="textarea"
        ></textarea>
      </div>
      <button
        class="send-button"
        @click="sendMessage"
        :disabled="isSending"
      >
        {{ isSending ? '发送中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import {getHeadImg, getUserId} from "@/utils/user-utils.js"
// import { getUserById, getChatHistory, sendChatMessage } from "@/api/chat/index.js"

const props = defineProps({
  userId: {
    type: String,
    required: true
  }
})

// 状态管理
const inputMessage = ref('')
const messages = ref([])
const currentUser = ref({})
const selfAvatar = ref(getHeadImg())
const messagesContainer = ref(null)
const textarea = ref(null)
const ws = ref(null)
const isSending = ref(false)

// 格式化后的消息列表
const formattedMessages = computed(() => {
  return messages.value.map(msg => ({
    ...msg,
    isSelf: msg.sender === 'me' // 根据实际用户ID判断
  }))
})

// 初始化
onMounted(async () => {
  await loadUser()
  await loadHistory()
  initWebSocket()
  adjustTextareaHeight()
})

// 清理
onUnmounted(() => {
  if (ws.value) {
    ws.value.close()
  }
})

// 加载用户信息
const loadUser = async () => {
  // try {
  //   const response = await getUserById(props.userId)
  //   currentUser.value = response.data
  // } catch (error) {
  //   console.error('加载用户信息失败:', error)
  // }
}

// 加载历史消息
const loadHistory = async () => {
  try {
    // const response = await getChatHistory(props.userId)
    // messages.value = response.data.map(msg => ({
    //   ...msg,
    //   timestamp: new Date(msg.timestamp),
    //   status: 'sent'
    // }))
    scrollToBottom()
  } catch (error) {
    console.error('加载历史消息失败:', error)
  }
}

// 初始化WebSocket
const initWebSocket = () => {
  ws.value = new WebSocket(`wss://localhost:8000/ws/chat/${props.userId}/`)
  ws.value.onopen = () => {
    console.log('WebSocket连接已打开')
  }
  ws.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    handleReceivedMessage(data)
  }

  ws.value.onerror = (error) => {
    console.error('WebSocket错误:', error)
  }

  ws.value.onclose = () => {
    console.log('WebSocket连接关闭')
  }
}

// 处理接收消息
const handleReceivedMessage = (message) => {
  messages.value.push({
    ...message,
    timestamp: new Date(message.timestamp),
    status: 'sent'
  })
  scrollToBottom()
}

// 发送消息
const sendMessage = async () => {
  const content = inputMessage.value.trim()
  if (!content) return

  const tempId = Date.now() // 临时ID用于本地显示
  const newMessage = {
    id: tempId,
    content,
    timestamp: new Date(),
    sender: 'me',
    status: 'sending'
  }

  try {
    messages.value.push(newMessage)
    inputMessage.value = ''
    adjustTextareaHeight()
    scrollToBottom()

    // 通过WebSocket发送
    ws.value.send(JSON.stringify({
      receiver: props.userId,
      sender: getUserId(),
      content
    }))

    // 通过API保存到数据库
    // const response = await sendChatMessage({
    //   receiver: props.userId,
    //   sender: getUserId(),
    //   content
    // })

    // 更新消息状态
    const index = messages.value.findIndex(msg => msg.id === tempId)
    if (index !== -1) {
      messages.value[index] = {
        ...messages.value[index],
        id: response.data.id,
        status: 'sent'
      }
    }
  } catch (error) {
    console.error('发送消息失败:', error)
    const index = messages.value.findIndex(msg => msg.id === tempId)
    if (index !== -1) {
      messages.value[index].status = 'error'
    }
  } finally {
    isSending.value = false
  }
}

// 时间格式化
const formatMessageTime = (date) => {
  const now = new Date()
  const msgDate = new Date(date)

  if (now.toDateString() === msgDate.toDateString()) {
    return msgDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  const yesterday = new Date(now)
  yesterday.setDate(now.getDate() - 1)
  if (yesterday.toDateString() === msgDate.toDateString()) {
    return '昨天 ' + msgDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  return msgDate.toLocaleDateString() + ' ' + msgDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// 文本框高度调整
const adjustTextareaHeight = () => {
  nextTick(() => {
    if (textarea.value) {
      textarea.value.style.height = 'auto'
      textarea.value.style.height = `${Math.min(textarea.value.scrollHeight, 150)}px`
    }
  })
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 换行处理
const newLine = () => {
  inputMessage.value += '\n'
  adjustTextareaHeight()
}
</script>

<style scoped>
/* 容器样式 */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f0f2f5;
}

/* 消息区域 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: 0;
}

/* 消息项 */
.message-item {
  margin-bottom: 16px;
}

/* 消息包装器 */
.message-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  max-width: 80%;
}

.message-wrapper.self {
  flex-direction: row-reverse;
  margin-left: auto;
}

/* 头像 */
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  flex-shrink: 0;
}

/* 消息主体 */
.message-body {
  max-width: calc(100% - 92px);
}

/* 消息气泡 */
.message-bubble {
  position: relative;
  padding: 12px 16px;
  border-radius: 6px;
  line-height: 1.5;
  word-break: break-word;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.message-bubble.self {
  background: #95ec69;
  border-radius: 16px 16px 4px 16px;
}

.message-bubble.other {
  background: white;
  border-radius: 16px 16px 16px 4px;
  border: 1px solid #eee;
}

/* 消息元信息 */
.meta {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 4px;
  font-size: 12px;
  color: #666;
}

.message-bubble.self .meta {
  color: rgba(0, 0, 0, 0.6);
}

/* 输入区域 */
.input-area {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: white;
  border-top: 1px solid #eee;
}

.input-box {
  flex: 1;
  position: relative;
}

textarea {
  width: 100%;
  min-height: 40px;
  max-height: 150px;
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 20px;
  resize: none;
  font-size: 14px;
  line-height: 1.5;
  transition: border-color 0.2s;
}

textarea:focus {
  outline: none;
  border-color: #07c160;
  box-shadow: 0 0 0 2px rgba(7, 193, 96, 0.1);
}

.send-button {
  flex-shrink: 0;
  padding: 8px 24px;
  background: #07c160;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.2s;
}

.send-button:hover {
  background: #06ad54;
}

.send-button:disabled {
  background: #b2b2b2;
  cursor: not-allowed;
}
</style>