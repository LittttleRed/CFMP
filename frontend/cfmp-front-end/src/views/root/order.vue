<script>
import DailyOrderChart from "../../components/root/DailyOrderChart.vue";
import {getOrders} from "../../api/root/index.js";

export default {
  components: { DailyOrderChart },
  data() {
    return {
      showtime:5,
      // 模拟数据（实际应从 API 获取）
      orderData: [
        { date: '2023-10-01', total: 1500.50 },
        { date: '2023-10-02', total: 2300.00 },
        { date: '2023-10-03', total: 1800.75 },
        { date: '2023-10-04', total: 4200.00 },
        { date: '2023-10-05', total: 3100.20 }
      ]
    }
  },
  methods: {
    handleShowTime(time){
      this.showtime = time;
    },
     processOrders(response, n) {
    const dailyTotals = {};

    // 处理每个订单，按日期累加金额
    response.data.forEach(order => {
        const date = order.created_at.slice(0, 10); // 提取日期部分
        const amount = parseFloat(order.total_amount);     // 转换金额为数字
        if (dailyTotals[date]) {
            dailyTotals[date] += amount;
        } else {
            dailyTotals[date] = amount;
        }
    });


    // 转换为目标格式并取最近 n 天
    return Object.entries(dailyTotals)
        .map(([date, total]) => ({ date, total: Number(total.toFixed(2)) }))
        .sort((a, b) => new Date(b.date) - new Date(a.date)) // 按日期倒序
        .slice(0, n).reverse();                                       // 取最近 n 天
},
// 使用示例（假设从 API 获取的响应叫 response）// 获取最近 5 天的数据
  },
  watch: {
    async showtime(newValue, oldValue) {
      let reponse=await getOrders(newValue)
      this.orderData=this.processOrders(reponse,newValue)
      console.log(this.orderData)
    }
  },
  async created() {
    // 模拟从 API 获取数据
    // this.loadOrderData()
    let reponse = await getOrders(5)
    this.orderData = this.processOrders(reponse, 5)
  },
}
</script>

<template>
    <daily-order-chart :chart-data="orderData" @showtime="handleShowTime" class="daily-order-chart"></daily-order-chart>
</template>

<style scoped>
.daily-order-chart{
  width: 50%;
}
</style>