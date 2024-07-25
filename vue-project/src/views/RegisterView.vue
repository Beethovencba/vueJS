<script setup>
    import axios from 'axios';
    import {reactive} from 'vue';
    import { useRouter } from 'vue-router';

    const user = reactive({});
    const router = useRouter();

    function register(){
        axios.post('http://127.0.0.1:5000/api/register', {
            username: user.username,
            email: user.email,
            password: user.password,
            confirmation: user.confirmation,
        }).then(response => {
            console.log('Registro bem-sucedido:', response.data);
            router.push({ name: 'home' });
        }).catch(error => {
            console.error('Erro no login:', error);
        });
    }
    
</script>

<template>
    <main class="container p-5 about">
        <form  @submit.prevent="register">
            <div class="form-group">
                <input autocomplete="off" autofocus class="form-control" placeholder="Username" type="text" v-model="user.username">
            </div>
            
            <div class="form-group">
                <input class="form-control" placeholder="Email" type="email" v-model="user.email">
            </div>
            
            <div class="form-group">
                <input class="form-control" placeholder="Password" type="password" v-model="user.password">
            </div>

            <div>
                <p> </p>
                <input class="form-control"  placeholder="Password (again)" type="password" v-model="user.confirmation">
            </div>
            <button class="btn btn-primary" type="submit">Register</button>
        </form>
    </main>
</template>