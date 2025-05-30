<template>
  <div class="user-management">
    <!-- 搜索表单 -->
    <el-form :model="tempForm" ref="searchForm" inline class="search-form">
      <el-form-item label="用户ID">
        <el-input v-model="tempForm.id" placeholder="请输入用户ID"></el-input>
      </el-form-item>

      <el-form-item label="用户姓名">
        <el-input v-model="tempForm.name" placeholder="请输入姓名"></el-input>
      </el-form-item>

      <el-form-item label="用户状态">
        <el-select v-model="tempForm.status" placeholder="请选择状态">
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
      <el-table-column prop="user_id" label="用户ID" ></el-table-column>
      <el-table-column prop="username" label="姓名" ></el-table-column>
      <el-table-column prop="status" label="状态" >

        <template #default="{ row }">
          <el-tag :type="row.status === 0 ? 'success' : 'danger'">
            {{ row.status === 0 ? '正常' : '已封禁' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="created_at"
        label="创建时间"
        sortable
      ></el-table-column>
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 0"
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
import Head from "../../components/Head.vue";
import LeftBar from "../../components/root/LeftBar.vue";
import {getAllUser, getUserByID,changeUserState} from "../../api/root/index.js";

export default {
  name: 'UserManagement',
  components: {LeftBar, Head},
  user:{},
  data() {
    return {
      pagination: {
        page: 1,
        page_size: 10,
        total: 1
      },tempForm:{
        id: '',
        name: '',
        phone: '',
        status: ''
      },
      searchForm: {
        id: '',
        name: '',
        phone: '',
        status: ''
      },
      user:{
        id: '',
        username: '',
        phone: '',
        status: '',
        createTime: '',
      }
      ,
      // 模拟数据
      userList: [{
        user_id: 1,
        username: 'John Doe',
        phone: '123-456-789',
        status: 0,
      }
      ]
    }
  },
  watch:{
     userList: {
    handler: function(newVal, oldVal) {

    },
    deep: true
  }
  },
  methods: {

    async handleBan(user) {
      // 封禁逻辑
      await changeUserState(user.user_id, 1).then(async () => {
        for (let i = 0; i < this.userList.length; i++){
          if (this.userList[i].user_id === user.user_id) {
            this.userList[i].status = 1
            break
          }
        }
      })
    },
    async handleUnban(user) {
      // 解封逻辑
      await changeUserState(user.user_id, 0).then(async () => {
         for (let i = 0; i < this.userList.length; i++) {
          if (this.userList[i].user_id === user.user_id) {
            this.userList[i].status = 0
            break
          }
        }
      })
    },
    handlePageChange(page) {
      this.pagination.page = page
       if(this.searchForm.name!==''||this.searchForm.phone!==''||this.searchForm.status!=='') {
         const queryParams = {
           username: this.searchForm.name,    // 键名改为 name
           phone: this.searchForm.phone,
           status: this.searchForm.status, // 使用动态分页
           page: page
         };
         this.loadUsers(queryParams)
       }else{
         this.loadUsers()
       }
    },
      async handleSearch() {

          this.searchForm = this.tempForm
          this.tempForm = {
            id: '',
            name: '',
            phone: '',
            status: ''
          }

      // 这里应实现搜索逻辑
        this.pagination.page = 1
        this.userList  = []
        this.pagination.total=0
      if(this.searchForm.id!==''){
        await this.getUserByID(this.searchForm.id)
      }else if(this.searchForm.name!==''||this.searchForm.phone!==''||this.searchForm.status!==''){
          const queryParams = {
        username: this.searchForm.name,    // 键名改为 name
        phone: this.searchForm.phone,
        status: this.searchForm.status, // 使用动态分页
      };
         console.log(queryParams)
      await this.loadUsers(queryParams);
      }else{
        await this.loadUsers()
      }
    },
     async loadUsers(queryParams = {page: 1}) {
      const filteredParams = Object.fromEntries(
      Object.entries(queryParams).filter(([_, v]) => v !== '' && v !== null)
    );
      try {
          let response =await getAllUser({...filteredParams,page: this.pagination.page})
          this.userList = response.data.results
          this.pagination.total = response.data.count
      } catch (err) {
        this.error = err.message
      }
    },
    async getUserByID(id) {
      const response = await getUserByID(id)
        this.userList[0]=response.data
        this.pagination.total=1
    }
  },
    created() {
  this.loadUsers() // 调用独立方法
},
}
</script>

<style scoped>
.user-management {
  padding: 20px;
  width: auto;
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