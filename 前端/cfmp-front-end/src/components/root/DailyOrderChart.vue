<template>
  <div class="chart-container">
    <v-chart
      :option="chartOption"
      :autoresize="true"
      style="width: 100%; height: 400px;"
    />
     <el-select
         v-model="showtime"
            placeholder="选择天数"
             style="width: 50%"
         @change="handleShowTime"
          >
            <el-option label="5天" value=5></el-option>
            <el-option label="10天" value=10></el-option>
            <el-option label="15天" value=15></el-option>
          </el-select>
  </div>
</template>

<script>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart } from 'echarts/charts'
import {
  GridComponent,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

// 按需导入 ECharts 模块
use([
  CanvasRenderer,
  BarChart,
  LineChart,
  GridComponent,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent
])

export default {
  name: 'DailyOrderChart',
  components: { VChart },
  data() {
    return{
            showtime:5
    }
  },
  methods: {
    handleShowTime(){//向外暴露信息,子传父
      this.$emit('showtime',this.showtime)
    }
  },
  props: {
    // 接收数据格式示例：
    // [
    //   { date: '2023-10-01', total: 1500 },
    //   { date: '2023-10-02', total: 2300 },
    //   ...
    // ]
     chartData: {
      type: Array,
      required: true,
      default: () => []
    },
  },
  computed: {
    chartOption() {
      return {
        title: {
          text: '每日订单总金额',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          formatter: '{b}<br/>总金额: ¥{c}'
        },
        xAxis: {
          type: 'category',
          data: this.chartData.map(item => item.date),
          axisLabel: {
            rotate: 45 // 日期标签旋转45度防重叠
          }
        },
        yAxis: {
          type: 'value',
          name: '金额 (¥)'
        },
        series: [{
          name: '日销售额',
           type: 'line',
          smooth: true, // 可改为 'line' 切换为折线图
          data: this.chartData.map(item => item.total),
          itemStyle: {
            color: '#5470c6' // 柱状图颜色
          },
          emphasis: {
            focus: 'series'
          }
        }],
        toolbox: {
          feature: {
            saveAsImage: {
              title: '保存图片',
              pixelRatio: 2
            },
            dataZoom: {
              yAxisIndex: 'none'
            }
          },
          right: 20
        }
      }
    }
  },

}
</script>

<style scoped>
.chart-container {
  width: 100%;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

</style>