import axios from 'axios';
import {ref} from 'vue';

const token = ref(localStorage.getItem('token'));
const tokenAuth = 'Bearer ' + token.value;

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000/api/',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': tokenAuth,
    },
    withCredentials: true,
})

export default axiosInstance;