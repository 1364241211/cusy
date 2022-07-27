import { InjectionKey, Ref } from "vue"
import { customer } from "."
const customerKey: InjectionKey<Ref<customer>> = Symbol("customer")
export default customerKey