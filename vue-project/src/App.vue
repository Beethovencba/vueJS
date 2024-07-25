<script setup>
  import { useAuth } from './store/auth';
  import { useRouter } from 'vue-router';
  import SidebarComponents from './components/SidebarComponents.vue';
  import NavBarComponents from './components/NavBarComponents.vue';
  const auth = useAuth();
  const router = useRouter();
  function logout(){
        auth.clear();
  }
</script>

<template>


  <NavBarComponents />
  <SidebarComponents />
  
  <main>
    <router-view />
  </main>
  
  <footer class="d-none d-lg-block rodape">
     <img class="img" src="./assets/logo_city.png" alt="logo da uber">
      <p class="copyright">&copy; Copyrigth Gerenciamento Uber - 2022</p> 
  </footer>
</template>

<style scoped>
@media (min-width: 1024px) {
  main {
    min-height: 60vh;
    align-items: center;    
  }
}
.img{
  width: 150px;
}

.rodape {
text-align: center;
background: #FEFEFE;
padding: 40px 0;
}

.copyright {
color: #000000;
font-size: 13px;
margin: 20px 0 0;
}
</style>




<!-- 
<template>
  <div class="cabecalho">
    <router-link :to="{name:'home'}"><img src="./assets/transferir.png" alt="logo da uber"></router-link>

    <nav class="menu">
    
        <ul v-if="auth.user && auth.token" class="menu__lista">
            <p class="user">{{ auth.user }}</p>
            <li class="menu__item logout" @click="logout">
              
              <router-link :to="{name:'home'}"  class="menu__link" >Log Out</router-link>
            </li>
        </ul>
        <ul v-if="auth.user && auth.token" class="menu__lista">
            <li class="menu__item"><a class="menu__link ativo" href="/veiculo">cadastrar veiculo</a></li>
            <li class="menu__item"><a class="menu__link" href="/ganhos">GANHOS</a></li>
            <li class="menu__item"><a class="menu__link" href="/despesas"> DESPESAS</a></li>
            <li class="menu__item"><a class="menu__link" href="/dashboard"> dashboard</a></li>
        </ul >

        <ul v-if="!auth.user && !auth.token" class="menu__lista">
          <li class="menu__item">
            <router-link class="menu__link ativo" :to="{name:'login'}">login</router-link>
          </li> 
          <li class="menu__item">
            <router-link class="menu__link" :to="{name:'register'}">register</router-link>
          </li>
        </ul>
    
    </nav>

  </div>
  <router-view />


  <footer class="rodape">
      <img src="./assets/logoFundoBranco.png" alt="logo da uber">
      <p class="copyright">&copy; Copyrigth Gerenciamento Uber - 2022</p> 
      
  </footer>
</template>
 -->
