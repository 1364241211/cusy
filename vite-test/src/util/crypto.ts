import { MD5 } from 'crypto-js';


const encryPass = (pass: string) => {
    return MD5(pass).toString()
}

export default encryPass