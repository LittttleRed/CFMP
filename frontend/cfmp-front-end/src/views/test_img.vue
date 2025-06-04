
<template>
 <input
      type="file"
      accept="image/*"
      @change="handleFileSelect"
      ref="fileInput"
      class="file-input"
    />

    <!-- 上传按钮和进度条 -->
    <button @click="upload" :disabled="!selectedFile">上传</button>
    <div v-if="progress > 0" class="progress-bar">
      <div :style="{ width: progress + '%' }"></div>
    </div>
    <img  :src="previewUrl" alt="Preview" />

  <button @click="getUserAvatar">
    获取当前用户头像
  </button>
  <img :src="returnUrl" alt="return" crossOrigin="anonymous" width="100px" height="100px"/>
</template>
<script setup>
    import { ref } from 'vue';
    import {getFile, uploadFile} from '../api/img/index.js'


const selectedFile = ref(null);
const previewUrl = ref('');
const progress = ref(0);
const error = ref('');
let returnUrl = ref('');
let ip= ref('/minio')

// 处理文件选择
const handleFileSelect = (event) => {
  console.log(event)
  const file = event.target.files[0];
  if (!file) return;

  // 验证文件类型和大小
  if (!file.type.startsWith('image/')) {
    error.value = '请选择图片文件';
    return;
  }
  if (file.size > 2 * 1024 * 1024) {
    error.value = '文件大小不能超过2MB';
    return;
  }

  selectedFile.value = file;
  error.value = '';
  previewUrl.value = URL.createObjectURL(file);
};
const upload = async () => {
  const formData = new FormData();
  formData.append('image', selectedFile.value)
  formData.append('user',9)
  formData.append('image_id',1)
  console.log(formData)
    const response = await uploadFile(formData)

    // 上传成功后处理（假设返回头像URL）
    // previewUrl.value = response.data.url;
    alert('上传成功！');
};
const getUserAvatar = async () => {
  const response = await getFile()
  console.log(response)
  returnUrl.value = ip.value+response.image;
  console.log(returnUrl.value)
  alert('获取成功！');
};
</script>
<style scoped>

</style>