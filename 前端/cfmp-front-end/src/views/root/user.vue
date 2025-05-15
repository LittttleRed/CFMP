<template>
  <div class="user-management">
    <!-- 搜索表单 -->
    <el-form :model="searchForm" ref="searchForm" inline class="search-form">
      <el-form-item label="用户ID">
        <el-input v-model="searchForm.id" placeholder="请输入用户ID"></el-input>
      </el-form-item>

      <el-form-item label="用户姓名">
        <el-input v-model="searchForm.name" placeholder="请输入姓名"></el-input>
      </el-form-item>

      <el-form-item label="手机号">
        <el-input v-model="searchForm.phone" placeholder="请输入手机号"></el-input>
      </el-form-item>

      <el-form-item label="用户状态">
        <el-select v-model="searchForm.status" placeholder="请选择状态">
          <el-option label="全部" value=""></el-option>
          <el-option label="正常" value="0"></el-option>
          <el-option label="封禁" value="1"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </el-form-item>
    </el-form>

    <!-- 用户列表 -->
    <el-table
      :data="userList"
      style="width: 100%"
      :default-sort="{ prop: 'createTime', order: 'descending' }"
    >
      <el-table-column prop="id" label="用户ID" width="120"></el-table-column>
      <el-table-column prop="name" label="姓名" width="150"></el-table-column>
      <el-table-column prop="phone" label="手机号" width="180"></el-table-column>
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="row.status === '0' ? 'success' : 'danger'">
            {{ row.status === '0' ? '正常' : '已封禁' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="createTime"
        label="创建时间"
        sortable
        width="200"
      ></el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button
            v-if="row.status === '0'"
            type="danger"
            size=small
            @click="handleBan(row)"
          >
            封禁
          </el-button>
          <el-button
            v-else
            type="success"
            size=small
            @click="handleUnban(row)"
          >
            解封
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import Head from "../../components/root/Head.vue";
import LeftBar from "../../components/root/LeftBar.vue";

export default {
  name: 'UserManagement',
  components: {LeftBar, Head},
  data() {
    return {
      searchForm: {
        id: '',
        name: '',
        phone: '',
        status: ''
      },
      // 模拟数据
      userList: [
        {
          id: '1001',
          name: '张三',
          phone: '13800138000',
          status: '0',
          createTime: '2023-03-15 10:00:00'
        },
        {
          id: '1002',
          name: '李四',
          phone: '13900139000',
          status: '1',
          createTime: '2023-03-16 14:30:00'
        }
      ]
    }
  },
  methods: {
    handleSearch() {
      // 这里应实现搜索逻辑
      console.log('搜索条件：', this.searchForm)
    },
    handleBan(user) {
      // 封禁逻辑
      console.log('封禁用户：', user.id)
    },
    handleUnban(user) {
      // 解封逻辑
      console.log('解封用户：', user.id)
    }
  }
}
</script>

<style scoped>
.user-management {
  padding: 20px;
}

.search-form {
  margin-bottom: 20px;
}

.el-form-item {
  margin-right: 20px;
}

.el-tag {
  margin: 2px;
}
</style>