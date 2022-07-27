<template>
    <el-main>
        <el-form :rules="loginFormValidata" :status-icon="true" ref="loginFormInstance" :model="loginForm"
            class="login_form">
            <h2>登&nbsp;录</h2>
            <el-form-item label="管理员账号：" prop="admin_account">
                <el-input v-model.number="loginForm.admin_account" name="admin_account" placeholder="请输入管理员账号"
                    autocomplete="off" pa>
                </el-input>
            </el-form-item>
            <el-form-item label="管理员密码：" prop="password">
                <el-input v-model="loginForm.password" type="password" name="password" placeholder="请输入管理密码"
                    autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item prop="code" label="请输入验证码：" style="flex-wrap: nowarp;">
                <el-input v-model="loginForm.code" name="code" placeholder="请输入验证码" required></el-input>
                <el-image :src="imageUrl" :style="{ height: '30px', width: '150px' }" @click="replaceUrl"></el-image>
            </el-form-item>
            <el-form-item>
                <el-button @click="login" color="#626aef">确认登录</el-button>
            </el-form-item>
        </el-form>
    </el-main>
</template>

<script lang="ts" setup>
import { ElMessage, FormInstance, FormRules } from 'element-plus';
import { useRouter } from 'vue-router';
import { useCookies } from 'vue3-cookies';
import { reactive, ref } from 'vue';
import service from '../util/api';
import encryPass from '../util/crypto';

const router = useRouter()
const cookies = useCookies()
const loginForm = reactive({
    admin_account: '',
    password: '',
    code: ''
})
const admin_account_val = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error("请输入6管理员账号"))
    } else if (!/^[0-9]{6}$/.test(value)) {
        callback(new Error("管理员账号为6位数字"))
    } else {
        callback()
    }
}
const admin_password_val = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error("请输入密码"))
    } else if (!/^[0-9a-zA-Z]{6,20}$/.test(value)) {
        callback(new Error("管理员密码的长度为6-20位，请确认"))
    } else {
        callback()
    }
}
const code_val = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error("请输入验证码"))
    } else {
        callback()
    }
}
const loginFormValidata = reactive<FormRules>(
    {
        admin_account: [{ validator: admin_account_val, required: true, trigger: "blur" }],
        password: [{ validator: admin_password_val, required: true, trigger: "blur" }],
        code: [{ validator: code_val, required: true, trigger: "blur" }]
    }
)
const loginFormInstance = ref<FormInstance>()
const imageUrl = ref('')
const replaceUrl = () => {
    service.get('captcha').then((res) => {
        imageUrl.value = `data:image/png;base64,${res.data.image}`
    }).catch((err) => {
        imageUrl.value = ''
    })
}
const login = () => {
    loginFormInstance.value?.validate((isValid) => {
        if (isValid) {
            service.post('/login', JSON.stringify({
                admin_account: loginForm.admin_account,
                password: encryPass(loginForm.password),
                code: loginForm.code
            })).then((resp) => {
                cookies.cookies.set("token", resp.data.access)
                ElMessage.success("登录成功,正在跳转页面！")
                router.push({ name: "customerControlPanel" })
            }).catch((err) => {
                ElMessage.error(`错误：${err.response.data.detail}`)
            })
        } else {

        }
    })
}

service.get('captcha').then((res) => {
    imageUrl.value = `data:image/png;base64,${res.data.image}`
}).catch((err) => {
    imageUrl.value = ''
})
</script>

<style lang="scss" scoped>
.el-main {
    width: 50vmax;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    .login_form {
        background: whitesmoke;
        width: 70%;
        border-radius: 15px;
        text-align: center;

        @media screen and (max-width:1152px) {
            min-width: 50%;
        }

        @media screen and (min-width:1152px) {
            max-width: 50%;
        }



        .el-form-item {
            margin: 2rem 1.3rem;
            flex-wrap: nowrap;

            :deep(.el-form-item__content) {
                flex-wrap: nowrap;
                justify-content: center;
            }

        }
    }
}
</style>
