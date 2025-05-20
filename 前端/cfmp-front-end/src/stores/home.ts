import { defineStore } from 'pinia'

interface GoodsItem {
  id: number
  title: string
  price: number
  cover: string
  // 其他字段...
}

export const useHomeStore = defineStore('home', {
  state: () => ({
    goodsList: [] as GoodsItem[],
    total: 0
  }),
  actions: {
    async getGoodsList(params: { page: number; pageSize: number; keyword?: string }) {
      // 模拟数据，需替换为真实API调用
      this.goodsList = Array.from({ length: 10 }, (_, i) => ({
        id: i + 1,
        title: `商品 ${i + 1}`,
        price: Math.floor(Math.random() * 1000),
        cover: 'https://via.placeholder.com/200x200'
      }))
      this.total = 100
    }
  }
})