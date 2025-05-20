import { defineStore } from 'pinia'


export const useHomeStore = defineStore('home', {
  state: () => ({
    goodsList: [{
      product_id:'',
      user_id:'',
      title:'',
      description:'',
      price:'',

    }],
    total: 0
  }),
  actions: {
    async getGoodsList(params) {
     console.log("get")
    }
  }
}
)