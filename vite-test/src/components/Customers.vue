<template>
  <div>
    <el-table
      :data="tableData"
      ref="tableInstance"
      max-height="800"
      v-loading="tableLoading"
      element-loading-text="加载中"
      border
      stripe
    >
      <!-- <el-table-column type="selection"></el-table-column> -->
      <el-table-column
        label="Id"
        width="70"
        height="10"
        prop="id"
        fit
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="customer_name"
        label="学生姓名"
        align="center"
      ></el-table-column>
      <el-table-column prop="customer_photo" label="学生照片" align="center">
        <template #default="scope">
          <div
            style="display: flex; align-items: center; justify-content: center"
          >
            <el-image
              :src="'/static/avatar/' + scope.row.customer_photo"
              style="height: 100px; width: 80px"
              fit="cover"
              :lazy="true"
              :preview-src-list="pre_src_list"
              :preview-teleported="true"
              :initial-index="pre_init_index"
              @click="changeInitIndex(scope.$index)"
            >
            </el-image>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="customer_id"
        label="学生身份证号"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="parent_phone"
        label="家长手机号"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="class_name"
        label="学生批次"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="customer_logtime"
        label="学生登记时间"
        align="center"
      ></el-table-column>
      <el-table-column align="center">
        <template #header>
          <div class="search-header">
            <el-input
              v-model="search"
              size="small"
              placeholder="请输入身份证号码"
              @input="searchCustomer"
              clearable
              @clear="clearSearch"
            />
          </div>
        </template>
        <template #default="tail">
          <div class="button-groups">
            <el-button type="primary" @click="updateCustomer(tail.$index)"
              >修改</el-button
            >
            <el-button type="danger" @click="deleteCustomer(tail.$index)"
              >删除</el-button
            >
          </div>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      v-model:page-sizes="pageSizeList"
      v-model:total="pagnation.count"
      layout="total,prev, pager, next,jumper,sizes"
      background
      @size-change="sizeChange"
      @current-change="jumpPage"
    />
    <el-drawer
      title="修改"
      v-model="drawer"
      direction="ltr"
      size="45%"
      @close="destroyCom"
    >
      <component
        v-if="isAlive"
        :is="asynComp"
        :itemProps="item_Props.data"
      ></component>
    </el-drawer>
  </div>
</template>

<script lang="ts" setup>
import {
  ref,
  reactive,
  watch,
  defineAsyncComponent,
  provide,
  inject,
} from "vue";
import { ElMessage, ElMessageBox, ElTable } from "element-plus";
import { AxiosResponse } from "axios";
import { customer, pagnationData } from "../types/index";
import service from "../util/api";

const isAlive = ref(false);
const destroyCom = () => {
  isAlive.value = false;
};
const reload = inject("reload", Function, true);
const pagnation = reactive<pagnationData>({
  count: 0,
  next: "null",
  previous: "null",
});
const tableLoading = ref<boolean>(false);
const changeLoading = (): void => {
  tableLoading.value = !tableLoading.value;
};
const tableData = ref<Array<customer>>();
const tableInstance = ref<InstanceType<typeof ElTable>>();
// 设置通过传递的response设置表格数据tableData
const set_tableData = (res: AxiosResponse) => {
  pagnation.count = res.data.count;
  pagnation.next = res.data.next;
  pagnation.previous = res.data.previous;
  tableData.value = res.data.results;
  tableData.value!.forEach((ele) => {
    pre_src_list.value.push(`/static/avatar/${ele.customer_photo}`);
  });
};
const search = ref<string>();
const pre_src_list = ref<Array<string>>([]);
const pre_init_index = ref<number>();

// 更改图片预览的初始下标
const changeInitIndex = (iniInex: number) => {
  pre_init_index.value = iniInex;
};

const pageSize = ref<number>(30);
431381198703102276;
const pageSizeList = ref<Array<number>>([30, 50, 100]);
const currentPage = ref<number>();
// 监听当前页面页码，发生改变时滚动到表格最上方
watch(currentPage, (newValue, oldValue) => {
  // window.scrollTo(0, 0)
  tableInstance.value?.scrollTo(0, 0);
});
// 搜索框清空时触发事件
const clearSearch = () => {
  changeLoading();
  service
    .get("/customers")
    .then((res) => {
      set_tableData(res);
      changeLoading();
    })
    .catch((err) => {
      changeLoading();
      ElMessage.error(err.code);
    });
};

// 当前页数发生改变时触发事件
const sizeChange = () => {
  changeLoading();
  service
    .get(`/customers?pageSize=${pageSize.value}`)
    .then((res: AxiosResponse) => {
      changeLoading();
      set_tableData(res);
    })
    .catch((err) => {
      changeLoading();
    });
};
// 当前页面页码改变时触发事件
const jumpPage = () => {
  changeLoading();
  service
    .get(`/customers?page=${currentPage.value}&pageSize=${pageSize.value}`)
    .then((res) => {
      changeLoading();
      set_tableData(res);
    })
    .catch((err) => {
      changeLoading();
      ElMessage.error(err.code);
    });
};
// 通过身份证查询单个用户
const searchCustomer = () => {
  if (search.value !== "") {
    changeLoading();
    service
      .get(`/customer/${search.value}`)
      .then((res: AxiosResponse) => {
        switch (res.data.code) {
          // case 404: tableData.value = new Array<customer>
          case undefined:
            set_tableData(res);
        }
        changeLoading();
      })
      .catch((err) => {
        // console.log(err.data);
        changeLoading();
        // ElMessage.error(err.data)
      });
  } else {
    clearSearch();
  }
};

// 删除单个用户
const deleteCustomer = (index: number) => {
  const warningInfo = `确定删除该用户吗？（注意该操作不可逆）\n姓名:${
    tableData.value?.at(index)?.customer_name
  }\n用户身份证: ${tableData.value?.at(index)?.customer_id}`;
  ElMessageBox.confirm(warningInfo, "警告!", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "error",
  })
    .then(() => {
      const id: number | undefined = tableData.value?.at(index)?.id;
      if (id !== undefined)
        service
          .delete(`/customers?id=${id}`)
          .then((res) => {
            switch (res.data.code) {
              case 200:
                {
                  ElMessage.success(res.data.message);
                  reload();
                }
                break;
              case 404:
                ElMessage.error(res.data.message);
                break;
            }
          })
          .catch((err) => {});
    })
    .catch(() => {});
};
const drawer = ref(false);
let item_Props = reactive({
  data: {
    id: 0,
    customer_name: "",
    customer_id: "",
    customer_photo: "",
    parent_phone: "",
    customer_logtime: "",
    class_id: 0,
    class_name: "",
  } as customer,
});
const asynComp = defineAsyncComponent({
  loader: () => import("./AddToCustomer.vue"),
  delay: 200,
});

// 更新用户
const updateCustomer = (index: number) => {
  const columnData = tableData.value?.at(index);
  item_Props["data"] = columnData as customer;
  drawer.value = !drawer.value;
  isAlive.value = true;
};
// 刷新页面时请求一次数据
service
  .get("/customers")
  .then((res) => {
    set_tableData(res);
  })
  .catch((err) => {
    ElMessage.error(err.code);
  });
</script>

<style lang="scss">
.search-header {
  display: flex;
  width: 100%;
}

.el-message-box__message {
  white-space: pre-wrap;
}
.button-groups {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  .el-button + .el-button {
    margin: 0;
  }
}
</style>
