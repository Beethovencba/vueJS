<script setup>
  import { useAuth } from '@/store/auth';
  import { useRouter } from 'vue-router';

  const auth = useAuth();
  const router = useRouter();

  function logout()
  {
    auth.clear();
    router.push({name: 'login'});
  }

</script> 

<template>
    <div>
      <b-sidebar id="sidebar-no-header" v-if="auth.user && auth.token" bg-variant="secondary" text-variant="light" aria-labelledby="sidebar-no-header-title" no-header shadow backdrop backdrop-variant="dark">
        <template #default="{ hide }">
          <div  class="p-3">
            <div class="d-flex align-items-center flex-column">
                <b-avatar variant="primary" class="mb-3 mt-3" size="5rem"></b-avatar>
                <h4 id="sidebar-no-header-title">{{ auth.user }}</h4>
                <div class="divisoria"></div>
            </div>
            
            <nav class="mb-3">
              <b-nav vertical>
                <b-nav-item active @click="hide"><b-icon icon="bar-chart-fill"></b-icon> Dashboard</b-nav-item>
                <b-nav-item router-link :to="{name:'cadastroVeiculo'}" type="light" @click="hide"><b-icon icon="truck"></b-icon> Cadastrar Veiculo</b-nav-item>
                <b-nav-item href="#link-2" @click="hide"> <b-icon icon="cash-stack"></b-icon> Receitas</b-nav-item>
                <b-nav-item href="#link-2" @click="hide"> <b-icon icon="tools"></b-icon> Despesas</b-nav-item>
                
                <div class="divisoria text-dark"></div>
              </b-nav>
            </nav>
            <b-button @click="logout()" variant="danger" class="mb-2 ml-2">
              <b-icon icon="power" aria-hidden="true"></b-icon> Logout
            </b-button>
          </div>
        </template>
        
        
      </b-sidebar>
    </div>
</template>

<style >
.nav-item > .nav-link {
    color: white;
  }

  .nav-item > .nav-link:hover {
    color:#CCC;
  }

  .divisoria {
    border: 1px solid #FFF;
    width: 100%;

  }

  h4 {
    text-transform: uppercase;
  }

</style>