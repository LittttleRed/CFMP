<template>
  <div class="product-management">
    <!-- 搜索表单 -->
    <el-form :model="tempForm" ref="searchForm" inline class="search-form" @keyup.enter.native="handleSearch">
      <el-form-item label="商品ID">
        <el-input v-model="tempForm.id" placeholder="请输入商品ID"></el-input>
      </el-form-item>

      <el-form-item label="商品名称">
        <el-input v-model="tempForm.title" placeholder="请输入商品名称"></el-input>
      </el-form-item>

      <el-form-item label="状态">
        <el-select v-model="tempForm.status" placeholder="请选择状态">
          <el-option label="全部" value=""></el-option>
          <el-option label="未审核" value="3"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button class="search-button" type="primary" @click="handleSearch">搜索</el-button>
      </el-form-item>
    </el-form>

    <!-- 商品列表 -->
    <el-table
      :data="productList"
      style="width: 100%"
      :default-sort="{ prop: 'created_at', order: 'descending' }"
    >
      <el-table-column prop="product_id" label="商品ID"></el-table-column>
      <el-table-column prop="title" label="商品名称"></el-table-column>
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="row.status !== 0 && row.status !== 2 ? 'warning' : 'success'">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" sortable></el-table-column>
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button size="small" type="danger" @click="handleBan(row)" v-if="row.status===0||row.status===3">封禁</el-button>
          <el-button size="small" type="success" @click="handleApprove(row)" v-if="row.status===1||row.status===3">上架</el-button>
          <el-button size="small" type="primary" @click="handleDetail(row)">详情</el-button>
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
  </div>
</template>

<script>
import Head from "../../components/Head.vue";
import LeftBar from "../../components/root/LeftBar.vue";
import { getAllProducts, getProductById, updateProductStatus } from "../../api/root/index";

export default {
  name: "ProductReview",
  components: { Head, LeftBar },
  data() {
    return {
      pagination: {
        page: 1,
        page_size: 10,
        total: 0
      },
      tempForm: {
        id: "",
        title: "",
        status: "3"
      },
      searchForm: {
        id: "",
        title: "",
        status: ""
      },
      productList: []
    };
  },
  methods: {
    // 获取商品状态标签
    getStatusLabel(status) {
      switch (status) {
        case 0:
          return "上架";
        case 1:
          return "封禁";
        case 2:
          return "已出售";
        case 3:
          return "未审核";
        default:
          return "未知";
      }
    },

    // 封禁商品
    async handleBan(product) {
      await updateProductStatus(product.product_id, 1).then(() => {
        product.status = 1;
      });
    },

    // 上架商品
    async handleApprove(product) {
      await updateProductStatus(product.product_id, 0).then(() => {
        product.status = 0;
      });
    },

    // 查看详情（逻辑留空）
    handleDetail(product) {
      // 这里可以跳转到商品详情页，例如：
      // this.$router.push(`/root/product/detail/${product.product_id}`);
      this.$router.push(`/product?product_id=${product.product_id}`)
    },

    // 分页切换
    handlePageChange(page) {
      this.pagination.page = page;
      const queryParams = {
        title: this.searchForm.title,
        status: this.searchForm.status,
        page: page
      };
      this.loadProducts(queryParams);
    },

    // 搜索处理
    async handleSearch() {
      this.searchForm = { ...this.tempForm };
      this.pagination.page = 1;
      this.productList = [];
      if (this.searchForm.id) {
        await this.getProductByID(this.searchForm.id);
      } else {
        const queryParams = {
          title: this.searchForm.title,
          status: this.searchForm.status
        };
        await this.loadProducts(queryParams);
      }
    },

    // 加载商品列表
    async loadProducts(queryParams = { page: 1 }) {
      try {
        const filteredParams = Object.fromEntries(
          Object.entries(queryParams).filter(([_, v]) => v !== "" && v !== null)
        );
        const response = await getAllProducts({ ...filteredParams, page: this.pagination.page });
        this.productList = response.data.results;
        this.pagination.total = response.data.count;
      } catch (err) {
        console.error("加载商品失败:", err.message);
      }
    },

    // 根据 ID 查询商品
    async getProductByID(id) {
      try {
        const response = await getProductById(id);
        this.productList = [response.data];
        this.pagination.total = 1;
      } catch (err) {
        console.error("查询商品失败:", err.message);
      }
    }
  },
  created() {
    this.loadProducts();
  }
};
</script>

<style scoped>
.product-management {
  padding: 20px;
  width: auto;
}

.search-form {
  width: 100%;
}
.search-button {
  margin: 0 auto;
}

.el-table-column {
  height: 100px;
}

.el-form {
  width: 100%;
}

.el-form-item {
  width: 18%;
}

.el-tag {
  margin: 2px;
}
</style>
