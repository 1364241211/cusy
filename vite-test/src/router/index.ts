import { createRouter, createWebHistory } from "vue-router";
import routes from "./config"
import cookies from '../cookies/index';



const router = createRouter({
    history: createWebHistory(),
    routes
})
// 路由跳转前进行验证
router.beforeEach((to, form, next) => {
    if (to.meta.requireAuth) {
        if (cookies.cookies.isKey("token")) {
            next()
        } else {
            next({ name: "login" })
        }
    } else {
        next()
    }
})

export default router