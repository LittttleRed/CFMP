<!-- src/views/complaint/UserComplaint.vue -->
<template>
  <div class="complaint-container">
    <!-- 搜索表单（差异部分） -->
    <el-form :model="tempForm" inline class="search-form">
      <el-form-item label="投诉ID">
        <el-input v-model="tempForm.complaint_id" placeholder="输入投诉ID"></el-input>
      </el-form-item>
      <el-form-item label="用户ID">
        <el-input v-model="tempForm.target_id" placeholder="输入用户ID"></el-input>
      </el-form-item>
      <el-form-item label="投诉人ID">
        <el-input v-model="tempForm.complainer_id" placeholder="输入投诉人ID"></el-input>
      </el-form-item>

      <el-form-item label="状态">
        <el-select v-model="tempForm.status" clearable>
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
      <el-table-column label="投诉ID">
        <template #default="{row}">{{ row.complaint_id }}</template>
      </el-table-column>
      <el-table-column label="被投诉用户ID">
        <template #default="{row}">{{ row.target_id }}</template>
      </el-table-column>
       <el-table-column prop="complainer_id" label="投诉人ID"></el-table-column>
      <el-table-column label="状态">
        <template #default="{row}">
          <el-tag :type="row.status === 0 ? 'warning' : 'success'">
            {{ statusMap[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="投诉时间" sortable></el-table-column>
      <el-table-column label="操作">
        <template #default="{row}">
          <el-button type="primary" size=small @click="openHandleDialog(row)" v-if="row.status === 0">处理</el-button>
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
        <el-form-item label="处理方式" prop="ban_type" style="width: 300px">
          <el-select
            v-model="handleForm.ban_type"
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
          v-if="handleForm.ban_type === 'ban'"
          style="width: 300px"
        >
          <el-select
            v-model="handleForm.ban_time"
            placeholder="请选择封禁时长"
             width="100%"
          >
            <el-option label="3天" value=3></el-option>
            <el-option label="7天" value=7></el-option>
            <el-option label="15天" value=15></el-option>
            <el-option label="30天" value=30></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="处理原因" prop="result" style="width: 500px">
          <el-input
            type="textarea"
            :rows="6"
            clearable

            v-model="handleForm.result"
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
import {changeUserState, createReview, getAllComplaints, getComplaintByID, updateReview} from "../../api/root/index.js";

export default {
  name: 'UserComplaint',
  data() {
    return {
      dialogVisible:  false,
      searchForm: {
        complaint_id: '',
        target_type: '1', // 固定为用户投诉
        target_id: '',
        complainer_id: '',
        status: '',
        ordering: '-created_at'
      },
      tempForm: {
        complaint_id: '',
        target_type: '1', // 固定为用户投诉
        target_id: '',
        complainer_id: '',
        status: '',
        ordering: '-created_at'
      },
      statusMap: { '0': '待处理', '1': '已处理' },
      complaintList: [
        // 模拟数据

      ],
      pagination: {
        page: 1,
        page_size: 10,
        total: 1
      },
      submitting: false,
      currentComplaint: null,
      handleForm: {
        ban_time: 0,
        ban_type:'',
        result: ''
      },
      actionOptions: [
        { value: 'warning', label: '发送警告' },
        { value: 'ban', label: '封禁处理' },
        { value: 'dismiss', label: '驳回投诉' }
      ],
      rules: {
        result: [
          { required: true, message: '请选择处理方式', trigger: 'change' }
        ],
        ban_time: [
          { required: true, message: '请选择封禁时长', trigger: 'change' }
        ],
        ban_type: [
          { required: true, message: '请输入处理原因', trigger: 'blur' }
        ]
      }
    }
    },
  methods: {
    async handleSearch() {
      this.searchForm = this.tempForm;
      this.tempForm = {
        target_type: '1', // 固定为用户投诉
        target_id: '',
        complainer_id: '',
        status: '',
        ordering: '-created_at',
        complaint_id: ''
      }
      this.pagination.page = 1
      this.complaintList = []
      this.pagination.total = 0
      if (this.searchForm.complaint_id !== '') {
        await this.getComplaintByID(this.searchForm.complaint_id)
      } else if (this.searchForm.complainer_id !== '' || this.searchForm.status !== ''||  this.searchForm.target_id !== '') {
            const queryParams = {
              target_id: this.searchForm.target_id,
        complainer_id: this.searchForm.complainer_id,
        status: this.searchForm.status,
              page:1
      };
            await this.loadComplaints(queryParams);
      } else {
        await this.loadComplaints();
      }

    },
    handleDetail(row) {
      console.log('处理投诉：', row.id)
    },
    handlePageChange(page) {
       this.pagination.page = page
       if(this.searchForm.complainer_id!==''||this.searchForm.status!==''||this.searchForm.target_id!=='') {
          const queryParams = {
              target_id: this.searchForm.target_id,
        complainer_id: this.searchForm.complainer_id,
        status: this.searchForm.status,
            page: page
      };
          this.loadComplaints(queryParams)
       }else{
         this.loadComplaints()
       }
    },
      openHandleDialog(row) {
      this.currentComplaint = row
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.handleForm.resetFields()
      })
    },

    submitHandle() {
      this.$refs.handleForm.validate(async valid => {
        if (valid) {
          this.submitting = true
          let review={
            target_type: 1, // 用户类型
            target_id: this.currentComplaint.target_id,
            ...this.handleForm,
            reviewer_id: 2
          }
          console.log(review)
          await createReview(review)
          await updateReview(this.currentComplaint.target_id,1,1)
          await changeUserState(this.currentComplaint.target_id,1)
            this.submitting = false
            this.dialogVisible = false
            this.$message.success('处理成功')
          for (let i = 0; i < this.complaintList.length; i++) {
            if (this.complaintList[i].target_id === this.currentComplaint.target_id ) {
              this.complaintList[i].status = 1
            }
          }
        }
      })
    },
    async getComplaintByID(id) {
        let response =await getComplaintByID(id)
        if(response.data.target_type===1){
        this.complaintList[0]=response.data
      }
      console.log(this.complaintList[0])
        this.pagination.total=1
    },
    async loadComplaints(queryParams = {page: 1}) {
      const filteredParams = Object.fromEntries(
      Object.entries(queryParams).filter(([_, v]) => v !== '' && v !== null)
    );
       try {
         console.log(filteredParams)
          let response =await getAllComplaints(1,{...filteredParams,page: this.pagination.page})
          console.log(response.data)
          this.complaintList = response.data.results
          this.pagination.total = response.data.count
      } catch (err) {
        this.error = err.message
      }
  },
  },
  created() {
     this.loadComplaints()
  }
}


</script>
<style scoped>
.complaint-container {
  padding: 20px;
  width: auto;
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
  width:16%;
}

.el-tag {
  margin: 2px;
}

</style>