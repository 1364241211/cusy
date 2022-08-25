<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <div class="left-header">东辰后台管理系统</div>
        <div class="right-header">
          <span>您好,账号为： {{ admin_account }}</span
          >,<span>{{ admin_name }}</span>
        </div>
      </el-header>
      <el-container>
        <el-aside>
          <el-menu router defaultActive="customers">
            <el-menu-item
              v-for="(item, index) in asideMenuList"
              :key="index"
              :index="item.routeIndex"
              :route="{ name: item.routeIndex }"
            >
              <el-icon>
                <component :is="item.iconName"></component>
              </el-icon>
              <span>{{ item.itemName }}</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-container>
          <el-main class="main-content">
            <router-view v-if="isRouterAlive"></router-view>
          </el-main>
          <!-- <el-footer>Footer</el-footer> -->
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import jwtDecode, { JwtPayload } from "jwt-decode";
import { onUnmounted, onMounted, inject, ref, provide, nextTick } from "vue";
import cookies from "../cookies/index";

interface MenuItem {
  routeIndex: string;
  itemName: string;
  iconName: string;
}
const asideMenuList = ref<Array<MenuItem>>([
  { routeIndex: "customers", itemName: "用户管理", iconName: "User" },
  { routeIndex: "moderateUsers", itemName: "用户审核", iconName: "UserFilled" },
  { routeIndex: "adDesign", itemName: "通知定制", iconName: "VideoPlay" },
  { routeIndex: "rechargeNotice", itemName: "充值通知", iconName: "Present" },
  { routeIndex: "classesControl", itemName: "班级管理", iconName: "School" },
  { routeIndex: "exportAvatar", itemName: "用户头像导出", iconName: "Money" },
  {
    routeIndex: "importOperations",
    itemName: "重要操作",
    iconName: "WarningFilled",
  },
]);

const jwtData = jwtDecode(cookies.cookies.get("token"));
interface jwtAdmin extends JwtPayload {
  admin_account?: string;
  admin_id?: number;
  admin_name?: string;
}
const { admin_account, admin_id, admin_name } = jwtData as jwtAdmin;
onMounted(() => {
  const updateShow = inject("updateFaShow", Function, true);
  updateShow();
});
onUnmounted(() => {
  const updateShow = inject("updateFaShow", Function, true);
  updateShow();
});
// 控制router-view 组件是否显示
const isRouterAlive = ref(true);
// 定义组件重载
const reload = () => {
  isRouterAlive.value = false;
  nextTick(() => {
    isRouterAlive.value = true;
  });
};
// 向后代注入reload方法加载组件
provide("reload", reload);
</script>

<style lang="scss" scoped>
.common-layout {
  height: fit-content;
  width: calc(100% - 1%);

  .el-container {
    height: fit-content;
    width: 100%;
    .el-aside {
      @media screen and (max-width: 1024px) {
        min-width: calc(130px + 1%);
      }
      @media screen and(min-width:1024px) {
        max-width: calc(200px - 1%);
      }
    }
    .main-content {
      height: 100%;
      overflow-y: scroll;
    }

    .el-main {
      width: 100%;
      height: fit-content;
    }

    .el-menu {
      background: #78b078;
      color: white;

      .el-menu-item {
        color: white;

        &:hover {
          background: #e9e9e9;
          color: rgb(9, 144, 189);
        }
      }
    }
  }

  .el-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgb(51, 74, 51);
    color: white;
  }
}
</style>
