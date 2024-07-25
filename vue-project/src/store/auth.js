import {ref} from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuth = defineStore('auth', () =>{
    
    const token = ref(localStorage.getItem('token'));
    const user = ref(JSON.parse(localStorage.getItem('username')));
    
    
    function setToken(tokenValue){
        localStorage.setItem('token', tokenValue);
        token.value = tokenValue;
    }

    function setUser(userValue){
        localStorage.setItem('user', userValue);
        user.value = userValue;
    }

    async function clear(){
                
        try {
            //reseta variaveis de login
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            token.value = "";
            user.value = "";
          } catch (error) {
            console.error("Erro durante o logout:", error);
          }
        
    }

    async function checkToken() {
        try {
            const tokenAuth = 'Bearer ' + token.value;
            
            const { data } = await axios.get('http://127.0.0.1:5000/api/verifyToken', {
                headers: {
                    Authorization: tokenAuth
                } 
            })
            
            return data;
        } catch (error) {
            console.log(error.response.data)
        }
    }
    
    return {
        setToken, 
        setUser,
        token,
        user,
        checkToken,
        clear,
    }
})