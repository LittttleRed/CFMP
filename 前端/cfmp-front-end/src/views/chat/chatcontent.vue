<template>
  <div class="chat-container">
    <!-- 聊天内容区域 -->
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="message-item"
        :class="{ 'self-message': message.isSelf }"
      >
        <!-- 对方消息 -->
        <div v-if="!message.isSelf" class="other-message">
          <img :src="currentUser.avatar" class="avatar" alt="头像">
          <div class="message-content">
            <div class="message-bubble">
              {{ message.content }}
            </div>
            <span class="time">{{ formatTime(message.time) }}</span>
          </div>
        </div>

        <!-- 自己发送的消息 -->
        <div v-if="message.isSelf" class="self-message">
          <div class="message-content">
            <span class="time">{{ formatTime(message.time) }}</span>
            <div class="message-bubble">
              {{ message.content }}
            </div>
          </div>
          <img :src="selfAvatar" class="avatar" alt="我的头像">
        </div>
      </div>
    </div>

    <!-- 输入框区域 -->
    <div class="input-area">
      <div class="input-box">
        <textarea
          v-model="inputMessage"
          @keydown.enter.exact.prevent="sendMessage"
          @keydown.ctrl.enter.exact="newLine"
          placeholder="请输入内容"
          rows="1"
          ref="textarea"
        ></textarea>
      </div>
      <button class="send-button" @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, nextTick } from 'vue'
import {getHeadImg} from "@/utils/user-utils.js";
import {getUserById} from "@/api/user/index.js";
import { getUserId } from "@/utils/user-utils.js";
import { onMounted, onBeforeUnmount } from 'vue'
const props = defineProps({
  userId: {
    type: String,
    required: true
  }
}
)

const inputMessage = ref('')
const currentUser = ref({})
const selfAvatar = ref(getHeadImg())
const messagesContainer = ref(null)
const textarea = ref(null)
const ws = ref(null)
const wsConnected = ref(false)

const messages = ref([
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
])

const myUserId = getUserId() 
const targetUserId = props.userId


const getMyMessage= ()=>{

}

onMounted(() => {
  console.log('start')
  ws.value = new WebSocket('ws://localhost:8000/ws/chat/')
  ws.value.onopen = () => {
    wsConnected.value = true
    messages.value.push({ time: new Date(), content: 'WebSocket连接成功', isSelf: false })
    console.log('WebSocket连接成功')
  }
  ws.value.onclose = () => {
    wsConnected.value = false
    messages.value.push({ time: new Date(), content: 'WebSocket连接关闭', isSelf: false })
    console.log('WebSocket连接关闭')
  }
  ws.value.onerror = () => {
    wsConnected.value = false
    messages.value.push({ time: new Date(), content: 'WebSocket连接出错', isSelf: false })
    console.log('WebSocket连接出错')
  }
  ws.value.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      if (data.error) {
        messages.value.push({ time: new Date(), content: '错误: ' + data.error, isSelf: false })
      } else {
        messages.value.push({
          time: new Date(),
          content: data.content,
          isSelf: data.sender_id == myUserId // 注意类型一致
        })
        nextTick(scrollToBottom)
      }
    } catch {
      messages.value.push({ time: new Date(), content: event.data, isSelf: false })
    }
  }
})

onBeforeUnmount(() => {
  if (ws.value) ws.value.close()
})


const getUser = async () => {
  await getUserById(props.userId).then(response => {
    currentUser.value = response
  })
}

const sendMessage = () => {
  if (!inputMessage.value.trim()) return
  // 先本地显示
  messages.value.push({
    content: inputMessage.value,
    time: new Date(),
    isSelf: true
  })
  // 通过WebSocket发送
  console.log(ws.value, ws.value.readyState)
  if (ws.value && ws.value.readyState === 1) {
      ws.value.send(JSON.stringify({
      receiver_id: targetUserId,
      content: inputMessage.value
    }))
  }
  inputMessage.value = ''
  nextTick(() => {
    scrollToBottom()
    adjustTextareaHeight()
  })
}

const newLine = () => {
  inputMessage.value += '\n'
  adjustTextareaHeight()
}

const formatTime = (time) => {
  return `${time.getHours().toString().padStart(2, '0')}:${time.getMinutes().toString().padStart(2, '0')}`
}

const scrollToBottom = () => {
  const container = messagesContainer.value
  if (container) {
    container.scrollTop = container.scrollHeight
  }
}

const adjustTextareaHeight = () => {
  const ta = textarea.value
  if (ta) {
    ta.style.height = 'auto'
    ta.style.height = ta.scrollHeight + 'px'
  }
}

// 初始化滚动到底部
nextTick(() => {
  scrollToBottom()
})
</script>

<style scoped>
/* 原有样式保持不变 */
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 860px;
  background-color: #f0f0f0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  padding-bottom: 0;
}

.message-item {
  margin-bottom: 20px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 5px;
  margin: 0 10px;
}

.other-message {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
}

.self-message {
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
}

.message-content {
  max-width: 60%;
  display: flex;
  flex-direction: column;
}

.message-bubble {
  padding: 10px 15px;
  border-radius: 5px;
  position: relative;
  line-height: 1.5;
  word-break: break-word;
}

.other-message .message-bubble {
  background: white;
  border: 1px solid #e5e5e5;
}

.self-message .message-bubble {
  background: #95ec69;
  order: 1;
}

.time {
  font-size: 12px;
  color: #999;
  margin: 5px 8px;
}

.input-area {
  padding: 15px;
  background: white;
  border-top: 1px solid #e5e5e5;
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.input-box {
  flex: 1;
  display: flex;
  align-items: center;
}

textarea {
  flex: 1;
  border: 1px solid #e5e5e5;
  border-radius: 5px;
  padding: 10px;
  resize: none;
  max-height: 150px;
  font-family: inherit;
  font-size: 14px;
}

textarea:focus {
  outline: none;
  border-color: #07c160;
}

.send-button {
  background: #07c160;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.2s;
}

.send-button:hover {
  background: #06ad54;
}
</style>