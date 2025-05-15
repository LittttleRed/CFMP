<!-- src/views/complaint/GoodsComplaint.vue -->
<template>
  <div class="complaint-container">
    <!-- 搜索表单 -->
    <el-form :model="searchForm" inline class="search-form">
      <el-form-item label="商品ID">
        <el-input v-model="searchForm.target_id" placeholder="输入商品ID"></el-input>
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

    <!-- 投诉列表 -->
    <el-table :data="complaintList" style="width: 100%">
      <el-table-column prop="id" label="投诉ID"></el-table-column>
      <el-table-column label="商品ID">
        <template #default="{row}">{{ row.target_id }}</template>
      </el-table-column>
      <el-table-column prop="complainer_id" label="投诉人ID"></el-table-column>
      <el-table-column label="状态" width="120">
        <template #default="{row}">
          <el-tag :type="row.status === '0' ? 'warning' : 'success'">
            {{ statusMap[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="投诉时间" sortable></el-table-column>
      <el-table-column label="操作">
        <template #default="{row}">
          <el-button type="primary" size="mini" @click="openHandleDialog(row)">处理</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      :current-page="pagination.page"
      :page-size="pagination.page_size"
      layout="total, prev, pager, next"
      :total="pagination.total"
      @current-change="handlePageChange"
    ></el-pagination>
    <el-dialog
      title="商品投诉处理"
      v-model="dialogVisible"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        :model="handleForm"
        label-width="100px"
        :rules="rules"
        ref="handleForm"
      >
        <el-form-item label="处理方式" prop="action" style="width: 300px">
          <el-select
            v-model="handleForm.action"
            placeholder="请选择处理方式"
            style="width: 100%"
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
          label="下架时长"
          prop="duration"
          v-if="handleForm.action === 'remove'"
          style="width: 300px"
        >
          <el-select
            v-model="handleForm.duration"
            placeholder="请选择下架时长"
            style="width: 100%"
          >
            <el-option label="3天" value="3"></el-option>
            <el-option label="7天" value="7"></el-option>
            <el-option label="15天" value="15"></el-option>
            <el-option label="永久下架" value="0"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item
          label="处罚卖家"
          prop="punishSeller"
          v-if="handleForm.action === 'punish'"
          style="width: 300px"
        >
          <el-select
            v-model="handleForm.punishSeller"
            placeholder="请选择处罚方式"
            style="width: 100%"
          >
            <el-option label="警告" value="warning"></el-option>
            <el-option label="限制发布商品" value="restrict"></el-option>
            <el-option label="封禁账号" value="ban"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="处理原因" prop="reason" style="width: 500px">
          <el-input
            type="textarea"
            :rows="4"
            v-model="handleForm.reason"
            placeholder="请输入处理原因及依据"
            maxlength="300"
            show-word-limit
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
  name: 'GoodsComplaint',
  data() {
    return {
      searchForm: {
        target_type: '0', // 固定为商品投诉
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
      dialogVisible: false,
      submitting: false,
      currentComplaint: null,
      handleForm: {
        action: '',
        duration: '',
        punishSeller: '',
        reason: ''
      },
      actionOptions: [
        { value: 'remove', label: '下架商品' },
        { value: 'punish', label: '处罚卖家' },
        { value: 'dismiss', label: '驳回投诉' }
      ],
      rules: {
        action: [
          { required: true, message: '请选择处理方式', trigger: 'change' }
        ],
        duration: [
          { required: true, message: '请选择下架时长', trigger: 'change' }
        ],
        punishSeller: [
          { required: true, message: '请选择处罚方式', trigger: 'change' }
        ],
        reason: [
          { required: true, message: '请输入处理原因', trigger: 'blur' },
          { min: 10, message: '至少输入10个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    openHandleDialog(row) {
      this.currentComplaint = row
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.handleForm.resetFields()
      })
    },

    submitHandle() {
      this.$refs.handleForm.validate(valid => {
        if (valid) {
          this.submitting = true
          const params = {
            target_type: 0, // 商品类型
            target_id: this.currentComplaint.target_id,
            ...this.handleForm
          }

          console.log('提交商品处理：', params)

          // 模拟接口调用
          setTimeout(() => {
            this.submitting = false
            this.dialogVisible = false
            this.$message.success('处理成功')
            // 这里应刷新表格数据
          }, 1000)
        }
      })

    },
    handleSearch() {
      console.log('搜索参数：', this.searchForm)
    },
    handleDetail(row) {
      console.log('处理投诉：', row.id)
    },
    handlePageChange(page) {
      this.pagination.page = page
    }
  },
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