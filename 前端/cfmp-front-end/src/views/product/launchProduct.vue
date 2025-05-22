<template>
  <div class="publish-container">
    <!-- 头部标题 -->
    <div class="header">
      <h2>发闲置</h2>
    </div>

    <!-- 图片上传区域 -->
    <el-upload
      class="image-uploader"
      action="#"
      list-type="picture-card"
      :auto-upload="false"
      multiple
    >
      <el-icon><Plus /></el-icon>
      <template #tip>
        <div class="upload-tip">添加优质首图更吸引人~</div>
      </template>
    </el-upload>

    <!-- 商品描述区 -->
    <div class="form-section">
      <el-input
        v-model="description"
        type="textarea"
        :rows="4"
        placeholder="描述一下宝贝的品牌型号、货品来源..."
      >
        <template #append>
          <el-button type="text" class="ai-write">A帮你写</el-button>
        </template>
      </el-input>
    </div>

    <!-- 价格输入 -->
    <div class="form-section">
      <el-input v-model="price" placeholder="价格">
        <template #prepend>¥</template>
        <template #append>
          <el-icon><ArrowRight /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- 发货方式 -->
    <div class="form-section">
      <el-select v-model="shippingMethod" placeholder="发货方式">
        <el-option label="包邮" value="free" />
        <el-option label="自提" value="selfPickup" />
        <el-option label="到付" value="payOnDelivery" />
      </el-select>
    </div>

    <!-- 发布按钮 -->
    <div class="submit-section">
      <el-button type="primary" round class="submit-btn">发布</el-button>
    </div>
  </div>
</template>

<style scoped>
.publish-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background: #fff;
}

.header h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.image-uploader {
  margin-bottom: 20px;
}

.upload-tip {
  color: #999;
  font-size: 14px;
  text-align: center;
  margin-top: 10px;
}

.form-section {
  margin-bottom: 25px;
}

.ai-write {
  color: #ff5500;
  font-weight: bold;
}

.submit-section {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
}

.submit-btn {
  width: 200px;
  height: 45px;
  font-size: 16px;
  background: linear-gradient(135deg, #ff8800, #ff5500);
  border: none;
}
</style>