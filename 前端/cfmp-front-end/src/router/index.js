
import {createRouter, createWebHashHistory, createWebHistory, useRoute} from "vue-router";
import {constRoutes} from "./routes";
import {getToken} from "@/utils/user-utils.js";
import {getMe} from "@/api/user/index.js";


const router = createRouter({
  history: createWebHistory(),
  routes: constRoutes,
});
router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!getToken()) {
      next('/login');
    } else {
      next();
    }
  } else {
    if (getToken()) {
      try {
        const user = await getMe(getToken());
      } catch (e) {
        next('/login');
      }
    }
    next();
  }
});
export default router;

