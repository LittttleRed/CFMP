
import {createRouter, createWebHashHistory, createWebHistory, useRoute} from "vue-router";
import {constRoutes} from "./routes";
import {getToken} from "@/utils/user-utils.js";


const router = createRouter({
  history: createWebHistory(),
  routes: constRoutes,
});
router.beforeEach((to, from, next) => {
if (to.matched.some(record => record.meta.requiresAuth)) {
if (!getToken()) {
next('/login');
} else {
next();
}
} else {
next();
}
});
export default router;

