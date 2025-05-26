<template>
  <div style="max-width: 500px; margin: 40px auto;">
    <h2>WebSocket 聊天测试</h2>
    <div style="margin-bottom: 16px;">
      <label>对方用户ID:</label>
      <input v-model="receiverId" type="text" style="width: 120px;" />
    </div>
    <div style="margin-bottom: 16px;">
      <label>消息内容：</label>
      <input v-model="message" type="text" style="width: 250px;" @keyup.enter="sendMessage" />
      <button @click="sendMessage" :disabled="!wsConnected || !receiverId || !message">发送</button>
    </div>
    <div style="margin-bottom: 16px;">
      <span v-if="wsConnected" style="color: green;">WebSocket已连接</span>
      <span v-else style="color: red;">WebSocket未连接</span>
    </div>
    <div style="border: 1px solid #eee; min-height: 120px; padding: 8px;">
      <div v-for="(msg, idx) in messages" :key="idx" style="margin-bottom: 8px;">
        <span style="color: #888;">[{{ msg.time }}]</span>
        <span :style="{ color: msg.isSelf ? '#409EFF' : '#67C23A' }">
          {{ msg.isSelf ? '我' : '对方' }}:
        </span>
        <span>{{ msg.content }}</span>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const wsUrl = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws/chat/'
const ws = ref(null)
const wsConnected = ref(false)
const receiverId = ref('')
const message = ref('')
const messages = ref([])

onMounted(() => {
  ws.value = new WebSocket(wsUrl)
  ws.value.onopen = () => {
    wsConnected.value = true
    messages.value.push({ time: now(), content: 'WebSocket连接成功', isSelf: false })
  }
  ws.value.onclose = () => {
    wsConnected.value = false
    messages.value.push({ time: now(), content: 'WebSocket连接关闭', isSelf: false })
  }
  ws.value.onerror = (e) => {
    wsConnected.value = false
    messages.value.push({ time: now(), content: 'WebSocket连接出错', isSelf: false })
  }
  ws.value.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      if (data.error) {
        messages.value.push({ time: now(), content: '错误: ' + data.error, isSelf: false })
      } else {
        messages.value.push({
          time: now(),
          content: data.content,
          isSelf: data.sender_id === window.__USER_ID__ // 你可以根据实际登录用户ID判断
        })
      }
    } catch {
      messages.value.push({ time: now(), content: event.data, isSelf: false })
    }
  }
})

onBeforeUnmount(() => {
  if (ws.value) ws.value.close()
})

function sendMessage() {
  if (!ws.value || ws.value.readyState !== 1 || !receiverId.value || !message.value) return
  ws.value.send(JSON.stringify({
    receiver_id: receiverId.value,
    content: message.value
  }))
  messages.value.push({ time: now(), content: message.value, isSelf: true })
  message.value = ''
}

function now() {
  const d = new Date()
  return `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`
}
</script>