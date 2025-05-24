<template>
  <Head />
  <div class="edit-container">
    <el-card shadow="hover" class="edit-card">
      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        label-width="100px"
        label-position="top"
      >
        <!-- 商品标题 -->
        <el-form-item label="商品标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入商品标题" />
        </el-form-item>

        <!-- 商品价格 -->
        <el-form-item label="商品价格" prop="price">
          <el-input-number
            v-model="form.price"
            :min="0"
            :precision="2"
            :step="1"
            controls-position="right"
          />
        </el-form-item>

        <!-- 商品描述 -->
        <el-form-item label="商品描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="6"
            placeholder="请输入详细商品描述"
          />
        </el-form-item>

        <!-- 商品图片上传 -->
        <el-form-item label="商品图片">
          <el-upload
            list-type="picture-card"
            :file-list="list.map(f => ({ url: f.media || f.url ,name: f.media_id }))"
            :on-change="handleChange"
            :on-remove="handleRemove"
            multiple
            :limit="9"
            action="#"
            :auto-upload="false"
          >
          </el-upload>
        </el-form-item>

        <!-- 提交按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            @click="submitForm"
            :loading="submitting"
          >
            提交修改
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted,toRaw } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import {getAllImage, getProduct, updateImg, updateProduct} from '../../api/product';
import Head from '../../components/Head.vue';
import {getToken, getUserId} from "../../utils/user-utils.js";

const route = useRoute();
const router = useRouter();
const formRef = ref(null);
const submitting = ref(false);

// 表单数据
const form = reactive({
  title: '',
  price: 0,
  description: '',
  media: []
});

// 图片文件列表
const list = ref([]);

// 验证规则
const rules = reactive({
  title: [
    { required: true, message: '标题不能为空', trigger: 'blur' },
    { max: 50, message: '标题不能超过50字', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '价格不能为空', trigger: 'blur' },
    { type: 'number', min: 0, message: '价格不能为负数' }
  ],
  description: [
    { required: true, message: '描述不能为空', trigger: 'blur' },
    { max: 1000, message: '描述不能超过1000字', trigger: 'blur' }
  ]
});

// 初始化加载商品数据
onMounted(async () => {
    const product = await getProduct(route.query.product_id).then(
        product =>{
          form.title = product.title;
          //转换为数字
          form.price = Number(product.price);
          form.description = product.description;
          form.media = product.media.map(m => m.media);
        }
    );
    list.value=await getAllImage(route.query.product_id,getToken()).then(
        img => {
          return prepareMediaFiles(img)
        }
    )
    console.log(list.value)
});
async function urlToFile(url, filename, mimeType) {
  try {
    const response = await fetch(url);
    const blob = await response.blob();
    return new File([blob], filename, { type: mimeType || blob.type });
  } catch (error) {
    console.error('转换失败:', url, error);
    return null;
  }
}
async function prepareMediaFiles(mediaList) {
  return await Promise.all(
    mediaList.map(async (item) => {
      // 如果已有 File 对象则跳过
      if (item.file instanceof File) return item;

      // 从 URL 创建 File
      const file = await urlToFile(
        item.media,
        `media_${item.media_id}.jpg`, // 自定义文件名
        'image/jpeg'
      );

      return { ...item, file };
    })
  );
}
// 处理图片上传成功
const handleChange = (file, fileList) => {
  list.value.push(file)
  console.log(list.value)
};

// 处理图片删除
const handleRemove = (file) => {
  console.log(file)
  console.log(list.value[0])
  const index = list.value.findIndex(f => f.media === file.url);
  if (index !== -1) {
    list.value.splice(index, 1);
  }
  console.log(list.value)
};

// 提交表单
const submitForm = async () => {
  console.log(form)

    submitting.value = true;

    // 表单验证
    await formRef.value.validate();

    // 调用API更新商品
    await updateProduct(route.query.product_id, {
      title: form.title,
      price: form.price,
      description: form.description,
      media: form.media
    },getToken());
    let mediaform = new FormData();
     console.log(list.value)
  list.value.forEach(item => {
  mediaform.append('media', item.file||item.raw)
});
    await updateImg(route.query.product_id, mediaform, getToken())

    ElMessage.success('修改成功');
    // router.push({
    //   name: 'product',
    //   query: { product_id: route.query.product_id }
    // });
  // } catch (error) {
  //   if (error.name !== 'ValidationError') {
  //     ElMessage.error('修改失败，请稍后重试');
  //   }
  // } finally {
  //   submitting.value = false;
  // }
};
</script>

<style scoped>
.edit-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.edit-card {
  margin-top: 20px;
  padding: 20px;
}

:deep(.el-form-item__label) {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.el-input-number {
  width: 200px;
}
</style>