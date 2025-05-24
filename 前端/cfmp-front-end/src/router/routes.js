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
      },
      {
        path: 'complaint_product',
        name: 'productManagement',
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
        path: 'phone',
        name: 'phone',
        component: () => (import('../views/user/changePhone.vue')),
        meta: {title: '修改手机号'}
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
    path: '/register',
    name: 'Register',
    redirect: '/register/email',
    children:[
      {
        path: 'email',
        name: 'emailRegister',
        component: () => import('../views/RegisterPage.vue'),
        meta: { title: '邮箱注册' }
      },
      {
        path: 'phone',
        name: 'phoneRegister',
        component: () => import('../views/RegisterPage.vue'),
        meta: { title: '手机号注册' }
      }
    ]
  },{
     path: '/product/launch',
     name: 'launch',
      component: () => import('../views/product/launch.vue'),
      meta: { title: '发布商品' }
  },{
    path: '/product',
    name: 'product',
    component: () => import('../views/product/product.vue'),
    meta: { title: '商品详情' }
  },{
  path: '/edit-product',
  name: 'edit-product',
  component: () => import('../views/product/edit.vue'),
  meta: { requiresAuth: true } // 如果需要登录权限
  },


  {
    path: '/test',
    name: 'test',
    component: () => import('../views/test.vue'),
    meta: { title: '测试' }
  }

  ]

