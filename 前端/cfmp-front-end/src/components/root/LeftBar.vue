<template>
  <div class="left-bar-container">
    <el-menu
      default-active="1"
      class="el-menu-vertical"
      background-color="#f5f7fa"
      text-color="#303133"
      active-text-color="#409EFF"
      router
    >
      <el-menu-item index="user">
        <i class="el-icon-user"></i>
        <span slot="title">用户管理</span>
      </el-menu-item>

      <el-menu-item index="complaint">
        <i class="el-icon-warning"></i>
        <span slot="title">投诉处理</span>
      </el-menu-item>

      <el-menu-item index="product">
        <i class="el-icon-goods"></i>
        <span slot="title">商品处理</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'LeftBar',
  data() {
    return {
      // 可以在此添加状态管理相关数据
    }
  }
}
</script>

<style scoped>
.left-bar-container {
  width: 200px;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.el-menu-vertical {
  border-right: none;
}

.el-menu-item {
  font-size: 20px;
  font-weight: bold;
  height: 80px;
  line-height: 56px;
}

.el-menu-item i {
  margin-right: 8px;
}
</style>