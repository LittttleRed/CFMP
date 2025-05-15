<!-- src/views/complaint/UserComplaint.vue -->
<template>
  <div class="complaint-container">
    <!-- 搜索表单（差异部分） -->
    <el-form :model="searchForm" inline class="search-form">
      <el-form-item label="用户ID">
        <el-input v-model="searchForm.target_id" placeholder="输入用户ID"></el-input>
      </el-form-item>
      <el-form-item label="投诉人ID">
        <el-input v-model="searchForm.complainer_id" placeholder="输入投诉人ID"></el-input>
      </el-form-item>

      <el-form-item label="状态">
        <el-select v-model="searchForm.status" clearable>
          <el-option label="全部" value=""></el-option>
          <el-option label="待处理" value="0"></el-option>
          <el-option label="已处理" value="1"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" class="filter-button" @click="handleSearch">筛选</el-button>
      </el-form-item>
    </el-form>

    <!-- 表格差异列 -->
    <el-table :data="complaintList" style="width: 100%">
      <el-table-column label="被投诉用户ID">
        <template #default="{row}">{{ row.target_id }}</template>
      </el-table-column>
       <el-table-column prop="complainer_id" label="投诉人ID"></el-table-column>
      <el-table-column label="状态">
        <template #default="{row}">
          <el-tag :type="row.status === '0' ? 'warning' : 'success'">
            {{ statusMap[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="投诉时间" sortable></el-table-column>
      <el-table-column label="操作">
        <template #default="{row}">
          <el-button type="primary" size=small @click="openHandleDialog(row)">处理</el-button>
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

     <el-dialog
      title="投诉处理"
      v-model="dialogVisible"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        :model="handleForm"
        width="100%"
        :rules="rules"
        ref="handleForm"
      >
        <el-form-item label="处理方式" prop="action" style="width: 300px">
          <el-select
            v-model="handleForm.action"
            placeholder="请选择处理方式"
          >
            <el-option
              v-for="item in actionOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item
          label="封禁时间"
          prop="banDuration"
          v-if="handleForm.action === 'ban'"
          style="width: 300px"
        >
          <el-select
            v-model="handleForm.banDuration"
            placeholder="请选择封禁时长"
             width="100%"
          >
            <el-option label="3天" value="3"></el-option>
            <el-option label="7天" value="7"></el-option>
            <el-option label="15天" value="15"></el-option>
            <el-option label="30天" value="30"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="处理原因" prop="reason" style="width: 500px">
          <el-input
            type="textarea"
            :rows="6"
            clearable

            v-model="handleForm.reason"
            placeholder="请输入处理原因"
          ></el-input>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button
          type="primary"
          @click="submitHandle"
          :loading="submitting"
        >
          确 定
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'UserComplaint',
  data() {
    return {
      dialogVisible:  false,
      searchForm: {
        target_type: '1', // 固定为用户投诉
        target_id: '',
        complainer_id: '',
        status: '',
        ordering: '-created_at'
      },
      statusMap: { '0': '待处理', '1': '已处理' },
      complaintList: [
        // 模拟数据
        {
          id: 'C1001',
          target_id: 'P2001',
          complainer_id: 'U3001',
          status: '0',
          created_at: '2023-03-15 10:00:00'
        }
      ],
      pagination: {
        page: 1,
        page_size: 10,
        total: 1
      },
      submitting: false,
      currentComplaint: null,
      handleForm: {
        action: '',
        banDuration: '',
        reason: ''
      },
      actionOptions: [
        { value: 'warning', label: '发送警告' },
        { value: 'ban', label: '封禁处理' },
        { value: 'dismiss', label: '驳回投诉' }
      ],
      rules: {
        action: [
          { required: true, message: '请选择处理方式', trigger: 'change' }
        ],
        banDuration: [
          { required: true, message: '请选择封禁时长', trigger: 'change' }
        ],
        reason: [
          { required: true, message: '请输入处理原因', trigger: 'blur' }
        ]
      }
    }
    },
  methods: {
    handleSearch() {
      console.log('搜索参数：', this.searchForm)

    },
    handleDetail(row) {
      console.log('处理投诉：', row.id)
    },
    handlePageChange(page) {
      this.pagination.page = page
    },
      openHandleDialog(row) {
      this.currentComplaint = row
      this.dialogVisible = true

    },

    submitHandle() {
      this.$refs.handleForm.validate(valid => {
        if (valid) {
          this.submitting = true
          // 这里调用处理接口
          console.log('提交处理：', {
            complaintId: this.currentComplaint.id,
            ...this.handleForm
          })

          // 模拟异步操作
          setTimeout(() => {
            this.submitting = false
            this.dialogVisible = false
            this.$message.success('处理成功')
          }, 1000)
        }
      })
    }
  }
}


</script>
<style scoped>
.complaint-container {
  padding: 20px;
  width: 100%;
}

.search-form {
  width: 100%;
}
.filter-button{
 margin:  0 auto;
}
.el-table-column{
  height: 100px;
}
.el-form{
  width: 100%;
}
.el-form-item {
  width:22%;
}

.el-tag {
  margin: 2px;
}

</style>