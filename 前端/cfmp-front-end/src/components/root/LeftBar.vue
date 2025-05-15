<template>
  <div class="left-bar-container">
    <el-menu
      default-active="1"
      class="el-menu-vertical"
      background-color="#f5f7fa"
      text-color="#303133"
      active-text-color="#409EFF"
      router
        @open="handleOpen"
        @close="handleClose"
    >
      <el-menu-item index="user">
        <span slot="title">用户管理</span>
      </el-menu-item>
          <el-menu-item index="/root/complaint_product">
          <span>商品投诉</span>
        </el-menu-item>
      <el-menu-item index="/root/complaint_user">
          <span>用户投诉</span>
        </el-menu-item>


      <el-menu-item index="product">
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
  width: 100%;
  min-height: 100vh;
  background-color: #f5f7fa;
}
.el-menu-vertical {
  border-right: none;
}
.el-sub-menu{
  text-align: center;
}
.complaints{
  text-align: center;
}
.el-menu-item  {
  font-size: 20px;
  font-weight: bold;
  height: 80px;
  line-height: 56px;
  margin-right: 0;
  padding-right: 0;
}
.el-menu-item span{
  font-size: 25px;
  text-align: center;
  margin: 0 auto;
}


</style>