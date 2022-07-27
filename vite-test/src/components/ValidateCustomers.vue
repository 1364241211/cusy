<template>
  <el-header>
		<div class="button-group">
				<el-button type="primary" :disabled="buttonEnable" @click="moderateUsers">通过 ({{buttonEnable?0:selectionRows}})</el-button>
		</div>
  </el-header>
  <el-table :data="tableData" ref="tableInstance" max-height="800" v-loading="tableLoading" element-loading-text="加载中"
    border stripe @selection-change="columnSelect()">
    <el-table-column type="selection"></el-table-column> 
	<el-table-column label="Id" width="70" height="10" prop="id" fit align="center">
    </el-table-column>
    <el-table-column prop="customer_name" label="学生姓名" align="center"></el-table-column>
    <el-table-column prop="customer_photo" label="学生照片" align="center">
      <template #default="scope">
        <div style="display: flex; align-items: center;justify-content: center;">
          <el-image :src="'/static/avatar/' + scope.row.customer_photo" style="height:100px; width:80px;" fit="cover"
            :lazy="true" :preview-src-list="pre_src_list" :initial-index="pre_init_index" :z-index="5000" preview-teleported
            @click="changeInitIndex(scope.$index)">
          </el-image>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="customer_id" label="学生身份证号" align="center"></el-table-column>
    <el-table-column prop="parent_phone" label="家长手机号" align="center"></el-table-column>
    <el-table-column prop="class_name" label="学生班级" align="center"></el-table-column>
    <el-table-column prop="customer_logtime" label="学生登记时间" align="center"></el-table-column>
  </el-table>
  <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="pageSizeList"
    :total="pagnation.count" layout="total,prev, pager, next,jumper,sizes" background @size-change="sizeChange"
    @current-change="jumpPage" />
  </template>
<script lang="ts" setup>
import { ref, reactive, watch,inject} from 'vue';
import { ElMessage, ElTable } from 'element-plus';
import { AxiosResponse } from 'axios';
import { customer, pagnationData } from '../types/index'
import service from "../util/api"

const pagnation = reactive<pagnationData>({
  count: 0,
  next: "null",
  previous: "null",
})
const tableLoading = ref<boolean>(false)
const changeLoading = (): void => {
  tableLoading.value = !tableLoading.value

}
const tableData = ref<Array<customer>>()
const tableInstance = ref<InstanceType<typeof ElTable>>()
const buttonEnable = ref(true)
const selectionRows = ref(0)
// 设置通过传递的response设置表格数据tableData
const set_tableData = (res: AxiosResponse) => {
  pagnation.count = res.data.count
  pagnation.next = res.data.next
  pagnation.previous = res.data.previous
  tableData.value = res.data.results
  tableData.value!.forEach(ele => {
    pre_src_list.value.push(ele.customer_photo)
  });
}
const columnSelect = ()=>{
		if(tableInstance.value?.getSelectionRows().length!==0){
				buttonEnable.value=false
				selectionRows.value=tableInstance.value?.getSelectionRows().length
		}else{
				buttonEnable.value=true
		}
}
const reload = inject("reload",Function,true)
// 为通过按钮添加点击事件
const moderateUsers = (()=>{
		changeLoading()
		service.post("/validateCustomers",JSON.stringify({
				idList:tableInstance.value?.getSelectionRows().map((item:customer)=>{
						return item.id
				})
		})).then(res=>{
				ElMessage.success({message:res.data.message})
				reload()
				changeLoading()
		}).catch(err=>{
				ElMessage.error({message:err})
				changeLoading()
		})
})
const pre_src_list = ref<Array<string>>([])
const pre_init_index = ref<number>()

// 更改图片预览的初始下标
const changeInitIndex = (iniInex: number) => {
  pre_init_index.value = iniInex
}

const pageSize = ref<number>(30)
const pageSizeList = ref<Array<number>>([30, 50, 100])
const currentPage = ref<number>()
// 监听当前页面页码，发生改变时滚动到表格最上方
watch(currentPage, (newValue, oldValue) => {
  // window.scrollTo(0, 0)
  tableInstance.value?.scrollTo(0, 0)
})

// 当前页数发生改变时触发事件
const sizeChange = () => {
  changeLoading()
  service.get(`/customers?pageSize=${pageSize.value}&is_valided=0`).then((res: AxiosResponse) => {
    changeLoading()
    set_tableData(res)
  }).catch((err) => {
    changeLoading()
  })
}
// 当前页面页码改变时触发事件
const jumpPage = () => {
  changeLoading()
  service.get(`/customers?page=${currentPage.value}&pageSize=${pageSize.value}&is_valided=0`).then((res) => {
    changeLoading()
    set_tableData(res)
  }).catch((err) => {
    changeLoading()
    ElMessage.error(err.code)
  })
}
// 刷新页面时请求一次数据
service.get("/customers?is_valided=0").then((res) => {
  set_tableData(res)
}).catch((err => {
  ElMessage.error(err.code)
}))
</script>

<style lang="scss" scoped>

.el-message-box__message {
  white-space: pre-wrap;
}
.el-header{
  height:fit-content;
  margin-bottom:1rem;
  padding:0;
  .button-group{
    display:flex,
	
  }
}
</style>

  <style lang="scss" scoped>
  </style>
