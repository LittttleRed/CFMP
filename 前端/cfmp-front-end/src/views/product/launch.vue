<template>
  <Head></Head>
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
      @change="handleFileChange"
      :on-remove="handleFileChange"
    >
      <el-icon style="font-size: 50px">+</el-icon>
      <template #tip>
        <div class="upload-tip">添加优质首图更吸引人~</div>
      </template>
    </el-upload>

    <!-- 商品描述区 -->
    <div class="form-section">
      <el-input
        v-model="title"
        type="textarea"
        :rows="1"
        placeholder="请输入展示的标题"
        style="margin-bottom: 10px"
         show-word-limit
          maxlength="100"
      >
      </el-input>
      <el-input
        v-model="description"
        type="textarea"
        :rows="4"
        placeholder="描述一下宝贝的品牌型号、货品来源..."
         show-word-limit
        maxlength="500"
      >
      </el-input>
    </div>
    <div class="form-section">
  <el-select
    v-model="selectedCategories"
    multiple
    filterable
    default-first-option
    placeholder="选择商品分类"
    style="width: 100%"
  >
    <el-option
      v-for="category in categoryList"
      :key="category"
      :label="category"
      :value="category"
    />
  </el-select>
  <div class="selected-tags" v-if="selectedCategories.length">
    <el-tag
      v-for="(tag, index) in selectedCategories"
      :key="index"
      style="margin: 4px"
      closable
      @close="removeCategory(index)"
    >
      {{ tag }}
    </el-tag>
  </div>
</div>

    <!-- 价格输入 -->
    <div class="form-section">
      <el-input v-model="price" placeholder="价格">
        <template #prepend>¥</template>
        <template #append>
        </template>
      </el-input>
    </div>
    <!-- 发布按钮 -->
    <div class="submit-section">
      <el-button type="primary" round class="submit-btn" @click="launch">发布</el-button>
    </div>
  </div>
</template>
<script setup>
import {ref} from "vue";
import {ElMessage} from "element-plus";
import {getHeadImg, getToken, getUserId, getUserName} from "../../utils/user-utils.js";
import {addProduct, getAllCategory} from "../../api/product/index.js";
import {useRoute, useRouter} from "vue-router";
import Head from "../../components/Head.vue";

const description = ref('')
const price = ref('')
const shippingMethod = ref('')
const imgList = ref([])
const title = ref('')
const router = useRouter()
const selectedCategories = ref([])
const categoryList = ref(['书籍教材', '电子数码', '服饰鞋包', '生活百货', '美妆个护', '运动户外', '其他'])
const catagoryNumber = ref([])
// 删除分类
const getCategoryList = async () => {
  console.log(categoryList.value)
  categoryList.value=await getAllCategory()
  catagoryNumber.value=categoryList.value.map(item=>item.category_id)
  categoryList.value=categoryList.value.map(item=>item.name)
  console.log(categoryList.value)
}
getCategoryList()
const removeCategory = (index) => {
  selectedCategories.value.splice(index, 1)
}
const handleFileChange=(file, fileList) => {
  console.log(fileList)
  imgList.value = fileList.map(f => f.raw);
  console.log(imgList.value)
}
const validatePrice = (price) => {
  const pattern = /^\d+(\.\d{1,2})?$/;
  return pattern.test(price) && parseFloat(price) > 0;
};
const launch = async () => {
 if (!title.value.trim()) {
    ElMessage.error("标题不能为空");
    return;
  }
  if (title.value.trim().length > 100) {
    ElMessage.error("标题长度不能超过100个字符");
    return;
  }
  // 验证描述
  if (!description.value.trim()) {
    ElMessage.error("商品描述不能为空");
    return;
  }
  if (description.value.trim().length > 500) {
    ElMessage.error("描述内容不能超过500个字符");
    return;
  }
  // 验证价格
  if (!price.value) {
    ElMessage.error("价格不能为空");
    return;
  }
  if (!validatePrice(price.value)) {
    ElMessage.error("请输入有效的价格（正数，最多两位小数）");
    return;
  }
  // 验证图片
  if (imgList.value.length < 1) {
    ElMessage.error("至少需要上传一张图片");
    return;
  }
  // 所有验证通过，继续发布流程
   try {
    const form = new FormData();
    form.append('title', title.value);
    form.append('description', description.value);
    form.append('price', parseFloat(price.value)); // 转换为数字
    form.append('status', '0'); // 确保字符串类型

    // 修正文件上传逻辑
    console.log(imgList.value)
    imgList.value.forEach(file => {
      form.append('media', file); // 直接使用原始文件对象
    });
    selectedCategories.value.forEach(category => {
      console.log(categoryList.value.indexOf(category))
      form.append('categories',catagoryNumber.value[categoryList.value.indexOf(category)])
    })
    // 删除冗余的用户信息传递
    // ❌ 移除 form.append('user', ...)

    await addProduct(form, getToken());
    ElMessage.success("发布成功！");
    //返回首页
    //  await router.push('/')
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "发布失败，请重试");
  }
}
</script>
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