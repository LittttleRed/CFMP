<template>
  <div class="notification-container">
    <h2 class="title">通知中心</h2>
    <div class="scrollable-list">
    <div v-for="item in notifications" :key="item.id" class="notification-item">
      <!-- 左侧状态标识 -->
      <div class="status-indicator" :class="getStatusClass(item.type)">
        <el-icon v-if="item.type === 'urgent'"><Warning /></el-icon>
        <div v-else class="dot"></div>
      </div>

      <!-- 主要内容区域 -->
      <div class="content">
        <div class="header">
          <span class="time">{{ formatTime(item.created_at) }}</span>
          <span class="title">{{ item.title }}</span>
        </div>
        <div class="message">{{ item.content }}</div>
      </div>

      <!-- 右侧操作按钮 -->
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElButton, ElIcon } from 'element-plus'
import { Warning } from '@element-plus/icons-vue'
import {getMyMessage} from "@/api/user/index.js";
import {getToken} from "@/utils/user-utils.js";

// 模拟通知数据
const notifications = ref([
])
const getmessage=async () => {
  await getMyMessage(getToken()).then(res => {
    notifications.value = [...notifications.value,...res.results]
    notifications.value.forEach(item => {
      item.type="important"
    })
    console.log(notifications.value)
  })
}
getmessage()

// 时间格式化
const formatTime = (timeString) => {
return timeString.slice(0,10)+'  '+timeString.slice(11,19)
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
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  height: 860px; /* 根据实际需求调整高度 */
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

.scrollable-list {
  flex: 1; /* 占据剩余空间 */
  overflow-y: auto; /* 启用垂直滚动 */
  padding: 0 16px; /* 添加内边距 */
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
  font-size: 14px;
  font-weight: bold;
  white-space: nowrap;
  padding: 0px; /* 保持标题固定 */
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