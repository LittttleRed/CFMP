<script setup>
  import vue from "../../assets/vue.svg";
</script>

<template>
  <div class="root-head">
    <div class="left">
      <h1 class="title">
        校园跳蚤市场管理系统
      </h1>
    </div>

  <div class="right">

    <el-col :span="12">
      <div class="demo-basic--circle">
        <div class="block">
          <el-avatar :size="75" :src=vue />
        </div>
      </div>
    </el-col>
      <a class="username">
      小红色的小红
    </a>
  </div>
</div>

</template>

<style scoped>
.root-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  background: yellow;
}
.username{
  font-size: 20px;
  font-weight: bold;
  margin: auto;
  padding-right: 10px;
  width: 200px;
}
 .left {
   margin-left: 80px;
   display: flex;
   flex-direction: row;
  }
  .right {
    display: flex;
    margin-right: 10px;
    flex-direction: row-reverse;
  }
  .title{
    font-size: 40px;
  }
</style>