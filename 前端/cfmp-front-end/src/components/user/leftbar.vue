<template>
  <div class="left-bar">
    <!-- 导航菜单 -->
    <el-menu
      class="nav-menu"
      :default-active="activeMenu"
      @select="handleSelect"
      router
         @open="handleOpen"
        @close="handleClose"
    >
      <!-- 我的交易 -->
      <el-sub-menu index="1">
        <template #title>
          <span class="menu-title">我的交易</span>
        </template>
        <el-menu-item :index="path">我发布的</el-menu-item>
        <el-menu-item index="/user/mybought" v-if="isMyHome">我买到的</el-menu-item>
      </el-sub-menu>

      <el-menu-item  index="mycollection" v-if="isMyHome">我的收藏</el-menu-item>


      <!-- 账户设置 -->
      <el-sub-menu index="3"  v-if="isMyHome">
        <template #title>
          <span class="menu-title">账户设置</span>
        </template>
        <el-menu-item index="/user/setting">个人资料</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import {useRoute} from "vue-router";
const path = ref('/user/myrelease')
const route=useRoute()
const activeMenu = ref('1-1') // 默认激活菜单
defineProps({
  isMyHome: {
    type: Boolean,
    default: false
  },
})
onMounted(()=>{
  if(route.query.user_id) {
    path.value = '/user/myrelease?user_id=' + route.query.user_id
  }
})
const handleSelect = (index) => {
  console.log('选中菜单:', index)
  // 这里可以添加路由跳转逻辑
  // 例如：router.push({ path: 对应路径 })
}
</script>

<style scoped>
.left-bar {
  width: 240px;
  background: #fff;
  border-right: 1px solid #ebedf0;
}

.user-info {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.user-id {
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 14px;
}

.user-detail {
  color: #666;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.follow-btn {
  margin-left: 4px;
  padding: 4px 8px;
}

.nav-menu {
  border-right: none;
}

:deep(.el-sub-menu__title) {
  height: 48px;
  line-height: 48px;
}

:deep(.el-menu-item) {
  height: 40px;
  line-height: 40px;
  font-size: 14px;
}

.menu-title {
  font-size: 14px;
  color: #333;
}



/* 悬停效果 */
:deep(.el-menu-item:hover) {
  background-color: #f5f5f5;
}
</style>