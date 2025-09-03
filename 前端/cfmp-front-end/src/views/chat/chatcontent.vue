<template>
  <div class="chat-container">
    <!-- 聊天内容区域 -->
    <div class="chat-messages" ref="messagesContainer">
       <div v-if="isLoading" class="loading-indicator">
      <span class="loader"></span>
      加载中...
    </div>
    <div v-else-if="!canLoadMore" class="no-more-messages">
      —— 已经到达历史消息尽头 ——
    </div>
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
            <span class="time">{{ typeof message.time === 'string'?  message.time.slice(0,10)+' '+message.time.slice(11,19) : message.time.toISOString().slice(0,10)+'  '+message.time.toISOString().slice(11,19) }}</span>
          </div>
        </div>

        <!-- 自己发送的消息 -->
        <div v-if="message.isSelf" class="self-message">
          <div class="message-content">
            <span class="time">{{ typeof message.time === 'string'?  message.time.slice(0,10)+' '+message.time.slice(11,19) : message.time.toISOString().slice(0,10)+' '+message.time.toISOString().slice(11,19) }}</span>
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
import {getHistory, getUserById} from "@/api/user/index.js";
import { getUserId } from "@/utils/user-utils.js";
import { onMounted, onBeforeUnmount } from 'vue'
import { getToken } from '../../utils/user-utils';
import { watchEffect } from 'vue'

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

])

const myUserId = getUserId() 
const targetUserId = props.userId

// 新增状态
const currentPage = ref(1)
const totalPages = ref(1)
const isLoading = ref(false)
const canLoadMore = ref(true)
const isInitialLoad = ref(true)

const getAllHistory = async () => {
  if (!canLoadMore.value || isLoading.value) return

  isLoading.value = true
  try {
    const pageconfig = {
      page: currentPage.value,
      page_size: 20
    }

    const response = await getHistory(getToken(), targetUserId, pageconfig).catch(error => {canLoadMore.value = false})
    totalPages.value = response.total_pages

    if (response.results.length === 0) {
      canLoadMore.value = false
      return
    }

    // 记录原始滚动信息
    const prevScrollHeight = messagesContainer.value?.scrollHeight || 0
    const prevScrollTop = messagesContainer.value?.scrollTop || 0

    // 插入新消息到列表头部
    const newMessages = response.results.map(message => ({
      content: message.content,
      time: message.send_at,
      isSelf: message.sender == getUserId()
    })).reverse()

    messages.value = [...newMessages, ...messages.value]

    // 等待DOM更新
    await nextTick()

    // 调整滚动位置
    if (messagesContainer.value) {
      const newScrollHeight = messagesContainer.value.scrollHeight
      const heightDiff = newScrollHeight - prevScrollHeight
      messagesContainer.value.scrollTop = prevScrollTop + heightDiff
    }

    currentPage.value++

    // 首次加载后滚动到底部
    if (isInitialLoad.value) {
      scrollToBottom()
      isInitialLoad.value = false
    }
  } finally {
    isLoading.value = false
  }
}

// 修改滚动处理逻辑
const handleScroll = (() => {
  if (isInitialLoad.value) return

  const container = messagesContainer.value
  if (!container) return

  // 触发加载的阈值（距离顶部100px）
  if (container.scrollTop < 100 && canLoadMore.value) {
    loadMoreMessages()
  }
})


// 优化后的加载方法
const loadMoreMessages = async () => {
  if (isLoading.value) return

  // 记录当前滚动位置
  const prevScrollHeight = messagesContainer.value.scrollHeight

  await getAllHistory()

  // 保持滚动位置
  nextTick(() => {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight - prevScrollHeight
  })
}

// 在组件挂载时添加滚动监听
onMounted(() => {

  messagesContainer.value?.addEventListener('scroll', handleScroll)
})

// 在组件卸载时移除监听
onBeforeUnmount(() => {
  messagesContainer.value?.removeEventListener('scroll', handleScroll)
})
onMounted(async () => {
  await getAllHistory()  // 确保先加载历史消息
  console.log('start')
  // 创建WebSocket连接，通过查询参数传递用户UUID
  const currentUserUuid = getUserId(); // 获取当前用户UUID
  ws.value = new WebSocket(`ws://localhost:8000/ws/chat/?uuid=${currentUserUuid}`)
  
  // 设置连接打开时的回调
  ws.value.onopen = () => {
    console.log('WebSocket连接已建立')
    wsConnected.value = true
  }
  
  // 设置连接关闭时的回调
  ws.value.onclose = () => {
    console.log('WebSocket连接已关闭')
    wsConnected.value = false
  }
  
  // 设置错误处理
  ws.value.onerror = (error) => {
    console.error('WebSocket连接错误:', error)
    wsConnected.value = false
  }
  
  // 设置消息接收处理
  ws.value.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      if (data.error) {
        messages.value.push({time: new Date(), content: '错误: ' + data.error, isSelf: false})
      } else {
        messages.value.push({
          time: new Date(),
          content: data.content,
          isSelf: data.sender_id == myUserId // 注意类型一致
        })
        nextTick(scrollToBottom)
      }
    } catch {
      messages.value.push({time: new Date(), content: event.data, isSelf: false})
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
getUser()

const sendMessage = () => {
  if (!inputMessage.value.trim()) return
  
  // 保存消息内容用于发送
  const messageToSend = inputMessage.value.trim()
  
  // 立即清空输入框
  inputMessage.value = ''
  
  // 调整文本框高度到初始状态
  nextTick(() => {
    adjustTextareaHeight()
  })
  
  // 本地显示消息
  messages.value.push({
    content: messageToSend,
    time: new Date(),
    isSelf: true
  })
  
  // 通过WebSocket发送
  console.log(ws.value, ws.value.readyState)
  if (ws.value && ws.value.readyState === 1) {
    ws.value.send(JSON.stringify({
      receiver_id: targetUserId,
      content: messageToSend
    }))
  }
  
  nextTick(() => {
    scrollToBottom()
  })
}

const newLine = () => {
  inputMessage.value += '\n'
  adjustTextareaHeight()
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
    // 只有当有内容时才根据scrollHeight调整高度，否则保持默认高度
    if (inputMessage.value) {
      ta.style.height = ta.scrollHeight + 'px'
    }
  }
}

scrollToBottom()
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
  font-size: 18px;
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