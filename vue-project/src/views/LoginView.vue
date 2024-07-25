<script setup>
    
    import { reactive} from 'vue';
    import axios from 'axios';
    import { useAuth } from '@/store/auth.js';
    import { useRouter } from 'vue-router';
    import ModalComponents from '@/components/ModalComponents.vue'
    

    const user = reactive({});
    const auth = useAuth();
    const router = useRouter();
    
    async function login() {
        auth.clear();
        try {
            const { data } = await axios.post('http://127.0.0.1:5000/api/login', user, { headers: {
        'Content-Type': 'application/json',
        // Outros cabeçalhos, se necessário
      },
    });
            auth.setToken(data.token);
            auth.setUser(data.username);
            router.push({ name: 'home' });
        } catch (error) {
            console.log(error?.response?.data);
        }
    }
    
</script>

<template>
    <main class="container p-5 about">
        <form @submit.prevent="login">
            <div class="form-group">
                <b-form-input autocomplete="off" autofocus class="form-control" name="username" placeholder="Username" type="text" v-model="user.username"></b-form-input>
            </div>
            <div class="form-group">
                <input class="form-control" name="password" placeholder="Password" required type="password" v-model="user.password">
            </div>
            <button class="btn btn-primary" type="submit">Log In</button>
        </form>
        
        <div v-if="auth.user === undefined">
            <ModalComponents/>
        </div>
    </main>
</template>
