/**
 * 路由项
 *  {
 *     path: "/components",          // 路由地址
 *     name: "components",           // 路由名称
 *     meta: {
 *         title: "组件示例",          // 路由标题
 *         icon: "Basketball",       // 路由图标
 *         requiresAuth: true,       // 是否需要登录
 *         cache: true,              // 是否缓存
 *         isLink: false,            // 是否外链
 *         hidden: false,            // 是否隐藏
 *         url: 'www.baidu.com',     // 内嵌地址 需要指定在 frame 组件配置
 *         perms: [                  // 权限控制
 *             "/components"         // 权限标识
 *         ],
 *     },
 *     children: []                  // 子路由
 * }
 */

export const constRoutes =   [
   {
    path: '/root',
    component: () => (import('../views/root/index.vue')),
    redirect: '/root/user', // 默认重定向到用户管理
    children: [
      {
        path: 'user',
        name: 'UserManagement',
        component: () => (import('../views/root/user.vue')),
        meta: {title: '用户管理'}
      },{
        path: 'product',
            name: 'productManagement',
            component: () => (import('../views/root/product.vue')),
            meta: {title: '商品审核'}
        },
      {
        path: 'complaint_product',
        name: 'ProductReview',
        component: () => (import('../views/root/complaint_product.vue')),
        meta: {title: '投诉管理'}
      },{
        path: 'complaint_user',
        name: 'userManagement',
        component: () => (import('../views/root/complaint_user.vue')),
        meta: {title: '投诉管理'}
      },{
        path: 'order',
        name: 'orderManagement',
        component: () => (import('../views/root/order.vue')),
        meta: {title: '订单管理'}
      }
    ]
  },{
  path: '/user',
    component: () => (import('../views/user/index.vue')),
    name: 'user',
    redirect: '/user/MyRelease',
        meta: { requiresAuth: true }, // 添加这里
    children: [
      {
        path:'MyRelease',
        name: 'MyRelease',
        component: () => (import('../views/user/myrelease.vue')),
        meta: {title: '我的发布'}
      },{
        path:'MyBought',
        name: 'MyBought',
        component: () => (import('../views/user/mybought.vue')),
        meta: {title: '我的购买'}
      },{
        path: 'MyOrder',
            name: 'MyOrder',
            component: () => (import('../views/user/myorder.vue')),
            meta: {title: '我的订单'}
        },{
        path:'MyCollection',
        name: 'MyCollection',
        component: () => (import('../views/user/mycollection.vue')),
        meta: {title: '我的收藏'}
      },{
        path:'setting',
        name: 'setting',
        component: () => (import('../views/user/setting.vue')),
        meta: {title: '个人资料'}
      },{
        path: 'pwd',
        name: 'pwd',
        component: () => (import('../views/user/changePwd.vue')),
        meta: {title: '修改密码'}
      },{
        path: 'email',
        name: 'email',
        component: () => (import('../views/user/changeEmail.vue')),
        meta: {title: '修改邮箱'}
      }
    ]
  },{
    path: '/img',
    component: () => (import('../views/test_img.vue')),
  },
 {
  path: '/chat',
    component: () => (import('../views/chat/index.vue')),
  },{
    path: '/',
    name: 'Home',
    component: () => import('../views/HomePage.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginPage.vue'),
    meta: {
      title: '用户登录',
    //   guestOnly: true // 标记仅未登录用户可访问
    }
  },{
    path: '/forget',
        name: 'Forget',
        component: () => import('../views/forgetPage.vue'),
        meta: {
          title: '忘记密码',
        //   guestOnly: true // 标记仅未登录用户可访问
        }
    },{
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterPage.vue'),
    meta: {
      title: '用户注册',
    //   guestOnly: true // 标记仅未登录用户可访问
    }
  },{
     path: '/product/launch',
     name: 'launch',
      component: () => import('../views/product/launch.vue'),
      meta: { title: '发布商品' }
  },{
    path: '/product',
    name: 'product',
    component: () => import('../views/product/product.vue'),
    meta: { title: '商品详情' }  },{
  path: '/edit-product',
  name: 'edit-product',
  component: () => import('../views/product/edit.vue'),
  meta: { requiresAuth: true } // 如果需要登录权限
  },{
    path: '/order/pay',
    name: 'pay',
    component: () => import('../views/order/pay.vue'),
    meta: {
      title: '订单支付',
      requiresAuth: true
    }
  },{
    path: '/order/payment',
    name: 'OrderPayment',
    component: () => import('../views/order/payment.vue'),
    meta: {
      title: '订单详情',
      requiresAuth: true
    }
  },
  {
    path: '/test',
    name: 'test',
    component: () => import('../views/chat/systemchat.vue'),
    meta: { title: '测试' }
  },{
    path: '/search',
    name: 'search',
    component: () => import('../views/search.vue'),
    meta:{title: '搜索'}
    }
  ]

