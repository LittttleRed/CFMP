import {createRouter, createWebHashHistory, createWebHistory} from "vue-router";
import {constRoutes} from "./routes";


const router = createRouter({
  history: createWebHistory(),
  routes: constRoutes,
});

export default router;
