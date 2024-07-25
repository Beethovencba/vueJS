<script setup>
  import { useAuth } from '@/store/auth';
  import { useRouter } from 'vue-router';
  
  const auth = useAuth();
  const router = useRouter();

</script>

<template>
    <div>
      <b-navbar toggleable="lg" type="light" variant="info">
        <img class="img" src="../assets/icon_car_min.png" alt="logo de um carro">
        <b-navbar-brand v-if="auth.user && auth.token" href="#"><b-button size="sm" variant="info" v-b-toggle.sidebar-no-header><b-icon icon="list"></b-icon></b-button></b-navbar-brand>
            
        <b-navbar-nav v-else class="ml-auto" >
          <b-nav-item router-link :to="{name:'login'}">Login</b-nav-item>
          <b-nav-item router-link :to="{name:'register'}">Register</b-nav-item>
        </b-navbar-nav>
      
      </b-navbar>
    </div>
  </template>
  
  <style scoped>
  .img {
    margin-right: 1rem;
  }
</style>
  