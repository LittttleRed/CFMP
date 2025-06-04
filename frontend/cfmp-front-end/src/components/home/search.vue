<template>
  <div class="xy-search-container" style="border-radius: 40px">
    <el-input
      v-model="keyword"
      class="xy-search-input"
      :placeholder="placeholder"
      clearable
      @keyup.enter="handleInput"
      style="--el-input-border-radius: 40px;width: 800px;height:60px"
    >
      <template #prefix>
        <el-icon class="search-icon"><Search /></el-icon>
      </template>
    </el-input>

    <el-card
      v-show="showSuggestions && suggestions.length"
      class="suggestions-card"
      shadow="never"
      style="border-radius: 60px"
    >
      <div v-for="(item, index) in suggestions"
           :key="index"
           class="suggestion-item"
           @click="handleSelect(item)">
        {{ item }}
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Search } from '@element-plus/icons-vue'
import {useRoute, useRouter} from "vue-router";

const props = defineProps({
  placeholder: {
    type: String,
    default: '搜索闲置商品'
  },
  suggestions: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['search', 'clear', 'select'])

const keyword = ref('')
const showSuggestions = ref(false)
const route=useRoute()
const router=useRouter()
const handleInput = () => {

router.push({name:'search',query:{search:keyword.value}}).then(()=>router.go(0))
  //刷新

}

const handleClear = () => {
  keyword.value = ''
  showSuggestions.value = false
  emit('clear')
}

const handleSelect = (item) => {
  keyword.value = item
  showSuggestions.value = false
  emit('select', item)
}

// 点击外部关闭建议列表
const clickOutside = (e) => {
  if (!e.target.closest('.xy-search-container')) {
    showSuggestions.value = false
  }
}

// 添加/移除全局点击监听
watch(showSuggestions, (val) => {
  if (val) {
    document.addEventListener('click', clickOutside)
  } else {
    document.removeEventListener('click', clickOutside)
  }
})
</script>

<style scoped>
.xy-search-container {
  position: relative;
  max-width: 1000px;
  margin: 20px auto;
  border-radius: 40px
}

.xy-search-input :deep(.el-input__inner) {
  height: 48px;
  border-radius: 40px;
  padding-left: 50px;
  font-size: 16px;
  border-color: #ff5000;
  width: 500px;

}

.xy-search-input :deep(.el-input__wrapper) {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.search-icon {
  font-size: 20px;
  color: #999;
  margin-left: 12px;
}

.suggestions-card {
  position: absolute;
  width: 100%;
  margin-top: 8px;
  /* 原60px改为与容器一致的40px */
  /* 添加顶部较小圆角避免直角 */
  border-radius: 20px 20px 40px 40px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  z-index: 2000;
}

.suggestion-item {
  padding: 12px 24px;
  cursor: pointer;
  transition: background 0.3s;
  color: #666;
}

.suggestion-item:hover {
  background: #f5f5f5;
  color: #ff5000;
}
</style>