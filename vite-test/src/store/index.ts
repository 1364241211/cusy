/**
 * 1. 定义容器并导出
 * 2. 使用容器中的state
 * 3. 修改容器中的state
 * 4. 使用容器中的action
 */
import { defineStore } from "pinia"

export const mainStore = defineStore("main", {
    state: () => {
        return {
            admin_name: "admin",
        }
    },
})