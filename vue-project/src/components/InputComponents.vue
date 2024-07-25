<template>
    <b-container class="text-center w-50 pt-5">
      <template class="" v-if="loading">
        
        <b-spinner variant="warning" type="grow"></b-spinner>
        <h1 class="text-warning">Loading...</h1>
      
      </template>
      <template v-else>
        <form 
        ref="form"
        @submit.prevent
        style="overflow: hidden;"
        
        >
          <h1 class="pb-3 text-left" style="color:ghostwhite; font-family: 'Poppins', sans-serif; font-family: 'PT Serif', serif; ">{{title}}</h1>
          <b-form-group
          
          label-for="marca-input"
          :invalid-feedback="invalidFeedback"
          :state="authForm.validar_input"
          style="overflow: hidden;"
          >
          
          <div v-if="indexCar < 3">
            <b-form-input
            id="marca-input"
            size="lg"
            type="text"
            placeholder="Digite as duas primeiras letras para carregar a lista"
            autofocus
            required
            minlength="2"
            v-model="authForm.input"
            @input="() => { authForm.valida_input(); }"
            
            @keyup.prevent="pressedKeyboard($event)"
            :state="authForm.validar_input"
            trim
            autocomplete="off"
            ></b-form-input>
            
          </div> 
          <div v-else>
            <b-form-input
            id="placa-input"
            size="lg"
            type="text"
            placeholder="ex: AAA1234 ou AA1A234"
            class="text-uppercase"
            autofocus
            required
            minlength="2"
            v-model="authForm.input"
            @input="() => {validarPlaca(authForm.input); }"
            @keyup="pressedKeyboard($event)"
            :state="authForm.validar_input"
            trim
            autocomplete="off"
            ></b-form-input>
          </div>
          
        </b-form-group>   
          <div style="height: 200px; overflow-y: auto;" >
          <transition name="fade" mode="out-in">
              <b-list-group
              :key="authForm.transicaoKey"
              class="bg-white rounded d-flex flex-column w-100 "                  
              >
                <b-list-group-item
                    v-for="(marca, index) in authForm.listaFiltrada"
                    :id="index"
                    :key="index"
                    button
                    :class="{ 'active': index === authForm.elementSelect }"
                    @click="() => {authForm.elementSelect = index; authForm.input = marca.name;}"
                    style="border: none; list-style-type: none; padding: 0; margin: 0;"
                >
                    <p
                    class="mb-0 mt-1 ml-3 text-uppercase text-black text-left"
                    :class="{'text-light': index === authForm.elementSelect}"
                    style="font-size: 18px; font-family: 'Poppins', sans-serif; font-family: 'PT Serif', serif;"
                    >
                    {{ marca.name}}
                    {{ marca.code}}
                    </p>
                </b-list-group-item>
              </b-list-group>
          </transition>
          </div>
        </form>     
    
        <div class="m-3 ">
            <b-button
            variant="outline-success"
            size="lg"
            class="float-right"
            @click="indexCar += 1; nextInputField();"
            :disabled="!authForm.validar_input"              
            >
            <strong>Proximo</strong>
            </b-button>
            
            <b-button
            variant="outline-danger"
            size="lg"
            class="float-right mr-2"
            @click="clickedButton($event)"
            >
            <strong>Fechar</strong>
            </b-button>
        </div>
      </template>
      <b-modal 
      v-model="state.modalShow" 
      :title="state.modalTitle" 
      size="sm" button-size="sm" 
      :ok-variant="state.modalOkVariant" 
      header-class="p-2 border-bottom-0" 
      footer-class="p-2 border-top-0" 
      centered="true"
      ok-only 
      
    >
      <p>{{ state.mensagem }}</p>
    </b-modal>  
    </b-container>
</template>

<script setup>
  
  import {onMounted, reactive, ref, watch} from 'vue';
  
  import {formAuth} from '@/store/authForm.js'
  
  
  const indexCar = ref(0);
  const url = ref('');
  const invalidFeedback = ref('')
  const loading = ref(null);
  const authForm = formAuth();
  
 
  const placaRegex = /^([A-Z]{3}\d{4}$|^[A-Z]{2}\d[A-Z]\d{3})$/i;
  const state = reactive({
    modalShow: null,
    modalTitle: '',
    modalOkVariant: '',
    mensagem: ''
  });
  
  const title = ref('');
  
  onMounted(async () => {
  title.value = 'Informe a Marca';
  invalidFeedback.value = 'Insira uma marca válida';
  loading.value = true;

  try {
    await authForm.resetInput();
    await authForm.searchCar('https://parallelum.com.br/fipe/api/v2/cars/brands');
  } catch (error) {
    console.error('Erro ao buscar dados:', error?.response?.data);
  }

  loading.value = false;
  });
  
  async function caixaDialogo() {

    try {
      const resposta = await authForm.salvarVeiculo();
      console.log(resposta)
      if (resposta.status !== 200) {
        state.modalOkVariant = "danger";
        state.modalTitle = 'Falha!';
      } else {
        state.modalOkVariant = "success";
        state.modalTitle = 'Sucesso!';
      }
      console.log(state.mensagem);
      state.mensagem = resposta.message && typeof resposta.message === 'object' ? resposta.message.message : resposta.message;
      console.log(state.mensagem);
    } catch (error) {
      console.error('Erro ao chamar salvarVeiculo:', error.message);
      state.modalOkVariant = "danger";
      state.modalTitle = 'Falha!';
      state.mensagem = 'Tente novamente mais tarde!';
    }
  }

  async function validarPlaca(placa){
    authForm.validar_input = await placaRegex.test(placa);
  }

  function scrollToElement(){
    const elemento = document.getElementById(authForm.elementSelect);
    
    if (elemento) {
      elemento.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }
  }

  async function nextInputField() {
    switch(indexCar.value) {
      case 0:
        loading.value = true;
        try {
          await authForm.resetInput(); 
          await authForm.searchCar('https://parallelum.com.br/fipe/api/v2/cars/brands');
        } catch (error) {
          console.error('Erro ao buscar dados:', error?.response?.data);
        }
        title.value = 'Informe a Marca';
        invalidFeedback.value = 'Insira uma marca valida'
        loading.value = false;
        break;
      case 1:
        console.log('entrou em modelo');
        console.log(authForm.keyCar[1])
        loading.value = true;
        try {
          authForm.keyEnter(indexCar.value);
          url.value = 'https://parallelum.com.br/fipe/api/v2/cars/brands/' + authForm.keyCar[1] + '/models';
          await authForm.searchCar(url.value);
        } catch (error) {
          console.error('Erro ao buscar dados:', error?.response?.data);
        }
        title.value = 'Informe o Modelo';
        invalidFeedback.value = 'Insira um modelo valido'
        loading.value = false;
        break;
      case 2:
        console.log('entrou em ano');
        loading.value = true;
        try {
          await authForm.keyEnter(indexCar.value);
          url.value = 'https://parallelum.com.br/fipe/api/v2/cars/brands/' + authForm.keyCar[1] + '/models/'+ authForm.keyCar[2] + '/years'
          await authForm.searchCar(url.value);
        } catch (error) {
          console.error('Erro ao buscar dados:', error?.response?.data);
        }
        title.value = 'Informe o Ano';
        invalidFeedback.value = 'Insira um ano/modelo valido'
        loading.value = false;
        break;
      case 3:
        console.log('entrou em placa');
        loading.value = true;

        try {
          await authForm.keyEnter(indexCar.value);
        } catch (error) {
          console.error('Erro ao buscar dados:', error?.response?.data);
        }
        
        title.value = 'Informe a Placa';
        invalidFeedback.value = 'Insira uma placa valida ex: AAA1234 ou AA1A234'
        loading.value = false;
        break;
      case 4:
        loading.value = true;
        console.log(authForm.keyCar);
        console.log(indexCar.value);
        try {
          authForm.keyCar[4] = authForm.input;
          await caixaDialogo();
        } catch (error) {
          console.error('Erro ao buscar dados:', error?.response?.data);
        }
        
        loading.value = false;
        state.modalShow = true;
      default:
        break;
    }
  }


  function pressedKeyboard(keyEvent){
    
    console.log(keyEvent)
    
    switch(keyEvent.key){
      case 'Enter':
        if(authForm.validar_input){
          indexCar.value += 1; 
          nextInputField();
        }
        
      case 'ArrowUp':
        authForm.keyUp();  
        scrollToElement();
        break;
      
      case 'ArrowDown':
        authForm.keyDown();
        scrollToElement();
        break;
      
      case 'Escape':
        console.log('tecla Esc acionada');
        break;
      default:
        console.log('Qualquer coisa');
    }
  }

  function clickedButton(clickEvent){
    
    switch(clickEvent.target.innerText){
      case 'Proximo':
        indexCar += 1; 
        nextInputField();
        
        break;
      case 'Fechar':
        console.log('botao fechar');
        authForm.resetDadosVeiculo();
        break;
    }
  }


</script>

<style>
  .fade-enter-active,
  .fade-leave-active {
    transition: all 0.2s ease-in-out;
  }

  .fade-enter-from,
  .fade-leave-to {
    transform: translateY(20px);
    opacity: 0;
  }

</style>


<!-- bugs: verificar se da pra cadastrar placa caso retorno status 401; definir atualizacao altomatica para lista de veiculos; fixar titulos da tabela -->