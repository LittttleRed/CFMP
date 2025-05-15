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
        <el-button class="search-button" type="primary" @click="handleSearch">搜索</el-button>
      </el-form-item>
    </el-form>

    <!-- 用户列表 -->
    <el-table
      :data="userList"
      style="width: 100%"
      :default-sort="{ prop: 'createTime', order: 'descending' }"
    >
      <el-table-column prop="id" label="用户ID" ></el-table-column>
      <el-table-column prop="name" label="姓名" ></el-table-column>
      <el-table-column prop="phone" label="手机号" ></el-table-column>
      <el-table-column prop="status" label="状态" >
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
      ></el-table-column>
      <el-table-column label="操作">
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
     <el-pagination
      :current-page="pagination.page"
      :page-size="pagination.page_size"
      layout="total, prev, pager, next"
      :total="pagination.total"
      @current-change="handlePageChange"
    ></el-pagination>
  </div>
</template>

<script>
import Head from "../../components/root/Head.vue";
import LeftBar from "../../components/root/LeftBar.vue";
import {getAllUser} from "../../api/root/index.js";

export default {
  name: 'UserManagement',
  components: {LeftBar, Head},
  all_user:{},
  data() {
    return {
      pagination: {
        page: 1,
        page_size: 10,
        total: 1
      },
      searchForm: {
        id: '',
        name: '',
        phone: '',
        status: ''
      },
      user:''
      ,
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
          id: '1001',
          name: '张三',
          phone: '13800138000',
          status: '1',
          createTime: '2023-03-15 10:00:00'
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
    },
     async loadUsers() {
      try {
        this.loading = true
        this.all_user = await getAllUser()
        console.log(this.all_user)
      } catch (err) {
        this.error = err.message
        console.error('API Error:', err)
      } finally {
        this.loading = false
      }
    }
  },
    created() {
  this.loadUsers() // 调用独立方法
}
}
</script>

<style scoped>
.user-management {
  padding: 20px;
  width: 100%;
}

.search-form {
  width: 100%;
}
.search-button{
 margin:  0 auto;
}
.el-table-column{
  height: 100px;
}
.el-form{
  width: 100%;
}
.el-form-item {
  width:18%;
}

.el-tag {
  margin: 2px;
}
</style>