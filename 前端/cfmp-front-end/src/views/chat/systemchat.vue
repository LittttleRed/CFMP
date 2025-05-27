<template>
  <div class="notification-container">
    <h2 class="title">通知中心</h2>
    <div v-for="item in notifications" :key="item.id" class="notification-item">
      <!-- 左侧状态标识 -->
      <div class="status-indicator" :class="getStatusClass(item.type)">
        <el-icon v-if="item.type === 'urgent'"><Warning /></el-icon>
        <div v-else class="dot"></div>
      </div>

      <!-- 主要内容区域 -->
      <div class="content">
        <div class="header">
          <span class="time">{{ formatTime(item.time) }}</span>
          <span class="title">{{ item.title }}</span>
        </div>
        <div class="message">{{ item.message }}</div>
      </div>

      <!-- 右侧操作按钮 -->
      <el-button
        type="primary"
        size="small"
        class="action-btn"
        @click="handleAction(item)">
        {{ item.buttonText }}
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElButton, ElIcon } from 'element-plus'
import { Warning } from '@element-plus/icons-vue'

// 模拟通知数据
const notifications = ref([
  {
    id: 1,
    time: '2024-05-24 17:11',
    title: '0.01元得麦当劳甜筒！',
    message: '【你有个福利待领取】',
    type: 'normal',
    buttonText: '立即领'
  },
  {
    id: 2,
    time: '2024-05-24 12:20',
    title: '■ 运气爆棚，送你2元无门槛红包',
    message: '鱼鲤新升级！手气真好 送你2元无门槛红包...',
    type: 'important',
    buttonText: '立即领'
  },
  {
    id: 3,
    time: '2024-05-17 19:47',
    title: '● 别让福利溜走！',
    message: '您的权益即将失效，再不行动就晚了！',
    type: 'urgent',
    buttonText: '查看详情'
  },
    {
    id: 1,
    time: '2024-05-24 17:11',
    title: '0.01元得麦当劳甜筒！',
    message: '【你有个福利待领取】',
    type: 'normal',
    buttonText: '立即领'
  },
  {
    id: 2,
    time: '2024-05-24 12:20',
    title: '■ 运气爆棚，送你2元无门槛红包',
    message: '鱼鲤新升级！手气真好 送你2元无门槛红包...',
    type: 'important',
    buttonText: '立即领'
  },
  {
    id: 3,
    time: '2024-05-17 19:47',
    title: '● 别让福利溜走！',
    message: '您的权益即将失效，再不行动就晚了！',
    type: 'urgent',
    buttonText: '查看详情'
  },
    {
    id: 1,
    time: '2024-05-24 17:11',
    title: '0.01元得麦当劳甜筒！',
    message: '【你有个福利待领取】',
    type: 'normal',
    buttonText: '立即领'
  },
  {
    id: 2,
    time: '2024-05-24 12:20',
    title: '■ 运气爆棚，送你2元无门槛红包',
    message: '鱼鲤新升级！手气真好 送你2元无门槛红包...',
    type: 'important',
    buttonText: '立即领'
  },
  {
    id: 3,
    time: '2024-05-17 19:47',
    title: '● 别让福利溜走！',
    message: '您的权益即将失效，再不行动就晚了！',
    type: 'urgent',
    buttonText: '查看详情'
  },
])

// 时间格式化
const formatTime = (timeString) => {
  const date = new Date(timeString)
  return `${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 状态样式处理
const getStatusClass = (type) => {
  return {
    'urgent': type === 'urgent',
    'important': type === 'important',
    'normal': type === 'normal'
  }
}

// 按钮点击处理
const handleAction = (item) => {
  console.log('处理通知操作:', item)
  // 这里可以添加跳转逻辑或API调用
}
</script>

<style scoped>
.notification-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  margin-bottom: 12px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.status-indicator {
  width: 24px;
  height: 24px;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-indicator.urgent {
  color: #e6a23c;
}

.status-indicator.important .dot {
  width: 8px;
  height: 8px;
  background: #f56c6c;
  border-radius: 50%;
}

.status-indicator.normal .dot {
  width: 8px;
  height: 8px;
  background: #909399;
  border-radius: 50%;
}

.content {
  flex: 1;
  min-width: 0;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.time {
  color: #999;
  font-size: 12px;
}

.title {
  font-weight: bold;
  color: #333;
  margin-left: 8px;
}

.message {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.action-btn {
  margin-left: 16px;
  flex-shrink: 0;
}
</style>