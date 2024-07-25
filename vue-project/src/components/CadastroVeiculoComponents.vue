<template>
  <b-container fluid="md" class="bv-example-row d-flexbox"> 
    <b-button v-b-modal.modal-Marca variant="success">Adicionar Veiculo</b-button>
    <b-modal
          id="modal-Marca"
          ref="marca"
          @show="authForm.carregaMarcas()"
          @hide="resetInput('marca')"
          @ok="authForm.keyEnter('marca')"
          @hidden="resetInput('marca')"
          >
          <form ref="form"
          @submit.prevent="authForm.keyEnter('marca'), resetInput('marca'), modelo.show()"
          >
            <b-form-group
              label="Marca"
              label-for="marca-input"
              invalid-feedback="Informe uma marca válida"
              :state="authForm.validar_input"
            >
                <b-form-input
                id="marca-input"
                size="lg"
                type="text"
                placeholder="Selecione a Marca"
                class="text-uppercase"
                autofocus
                required
                minlength="2"
                v-model="inputValue.marca"
                @input="() => { getInput(inputValue.marca); authForm.valida_input(); }"
                @keyup.down.prevent="() => {authForm.keyDown();  scrollToElement();}"
                @keyup.up.prevent="() => {authForm.keyUp();  scrollToElement();}"
                @keyEnter="() => { authForm.keyEnter('marca'); }"
                @keyup.esc="authForm.resetDadosVeiculo()"
                :state="authForm.validar_input"
                trim
                autocomplete="off"
              ></b-form-input>
                    
            </b-form-group>  
            <div style="position: relative;">
              <transition name="fade" mode="out-in">
                <b-list-group
                  :key="authForm.transicaoKey"
                  class="overflow-auto bg-white rounded d-flex flex-column w-100"
                  style="max-height:200px; padding-right:2rem;" 
                                
                >
                  <b-list-group-item
                    v-for="(marca, index) in authForm.listaFiltrada"
                    :id="index"
                    :key="index"
                    button
                    :class="{ 'active': index === authForm.elementSelect }"
                    class="block px-4 py-2 text-sm leading-5 text-gray-700 cursor-pointer lead"
                    @click="() => {authForm.elementSelect = index; inputValue.marca = marca.nome}"
                    
                  >
                    <p
                      class="font-italic text-uppercase text-monospace m-1 text-black"
                      :class="{'text-light': index === authForm.elementSelect}"
                    >
                      {{ marca.nome }}
                    </p>
                  </b-list-group-item>
                </b-list-group>
              </transition>
            </div>
          </form>     
          <template #modal-footer>
              <div class="w-100">
                
                <b-button
                  variant="primary"
                  size="sm"
                  class="float-right"
                  @click="authForm.keyEnter('idMarca'), modelo.show()"
                  :disabled="!authForm.validar_input"              
                  >
                  Proximo
                </b-button>
                <b-button
                  variant="danger"
                  size="sm"
                  class="float-right mr-2"
                  @click=" authForm.resetDadosVeiculo(), marca.hide()"
                >
                  Fechar
                </b-button>
              </div>
          </template>
    </b-modal>

    <b-modal
      id="modal-Modelo"
      ref="modelo"
      @show=" marca.hide(), authForm.carregaModelos()"
      @shown="autoFocusInput('modeloInput')"
      @hide="modelo.hide()"
      @hidden="resetInput('modelo')"
      @ok="authForm.keyEnter('modelo')"
      lazy
      >
      <form ref="form"
      @submit.prevent="authForm.keyEnter('modelo'), ano.show()"
      >
        <b-form-group
          label="Modelo"
          label-for="modeloInput"
          invalid-feedback="Informe uma modelo válido"
          :state="authForm.validar_input"
        >
            <b-form-input
            id="modeloInput"
            size="lg"
            type="text"
            placeholder="Selecione a modelo"
            class="text-uppercase"
            required
            minlength="2"
            v-model="inputValue.modelo"
            @input="() => {getInput(inputValue.modelo); authForm.valida_input();}"
            @keyup.down.prevent="() => {authForm.keyDown();  scrollToElement();}"
            @keyup.up.prevent="() => {authForm.keyUp();  scrollToElement();}"
            @keyEnter.prevent="authForm.keyEnter('modelo')"
            @keyup.esc="authForm.resetDadosVeiculo()"
            :state="authForm.validar_input"
            trim
            autocomplete="off"

          ></b-form-input>
        </b-form-group>  
        <div style="position: relative;">
          <transition name="fade" mode="out-in">
            <b-list-group
              :key="authForm.transicaoKey"
              class="overflow-auto bg-white rounded d-flex flex-column w-100"
              style="max-height:200px; padding-right:2rem;" 
                            
            >
              <b-list-group-item
                v-for="(modelo, index) in authForm.listaFiltrada"
                :id="index"
                :key="index"
                button
                :class="{ 'active': index === authForm.elementSelect }"
                class="block px-4 py-2 text-sm leading-5 text-gray-700 cursor-pointer lead"
                @click="() => {authForm.elementSelect = index; inputValue.marca = modelo.nome}"
              >
                <p
                  class="font-italic text-uppercase text-monospace m-1 text-black"
                  :class="{'text-light': index === authForm.elementSelect}"
                >
                  {{ modelo.nome }}
                </p>
              </b-list-group-item>
            </b-list-group>
          </transition>
        </div>
        </form>     
        <template #modal-footer>
          <div class="w-100">
            
            <b-button
              variant="primary"
              size="sm"
              class="float-right "
              @click="authForm.keyEnter('modelo'), ano.show()"
              :disabled="!authForm.validar_input"
            >
              Proximo
            </b-button>
            <b-button
              variant="danger"
              size="sm"
              class="float-right mr-2"
              @click="authForm.resetDadosVeiculo(), modelo.hide()"
            >
              Fechar
            </b-button>
          </div>
        </template>
    </b-modal>

    <b-modal
      id="modalAno"
      ref="ano"
      @show="modelo.hide(), authForm.carregaAno()"
      @shown="autoFocusInput('anoInput')"
      @hide="ano.hide()"
      @hidden="resetInput('ano')"
      @ok="authForm.keyEnter('idAno')"
      lazy
      >
      <form ref="form"
      @submit.prevent="authForm.keyEnter('idAno'), placa.show()"
      >
        <b-form-group
          label="Ano"
          label-for="anoInput"
          invalid-feedback="Informe um ano valido!"
          :state="authForm.validar_input"
        >
            <b-form-input
            id="anoInput"
            size="lg"
            type="text"
            placeholder="Selecione o Ano"
            class="text-uppercase"
            required
            minlength="2"
            v-model="inputValue.ano"
            @input="() => {getInput(inputValue.ano); authForm.valida_input();}"
            @keyup.down.prevent="() => {authForm.keyDown();  scrollToElement();}"
            @keyup.up.prevent="() => {authForm.keyUp();  scrollToElement();}"
            @keyEnter.prevent="authForm.keyEnter('idAno')"
            @keyup.esc="authForm.resetDadosVeiculo()"
            :state="authForm.validar_input"
            trim
            autocomplete="off"

          ></b-form-input>
        </b-form-group>  
        <div style="position: relative;">
          <transition name="fade" mode="out-in">
            <b-list-group
              :key="authForm.transicaoKey"
              class="overflow-auto bg-white rounded d-flex flex-column w-100"
              style="max-height:200px; padding-right:2rem;" 
                            
            >
              <b-list-group-item
                v-for="(ano, index) in authForm.listaFiltrada"
                :id="index"
                :key="index"
                button
                :class="{ 'active': index === authForm.elementSelect }"
                class="block px-4 py-2 text-sm leading-5 text-gray-700 cursor-pointer lead"
                @click="() => {authForm.elementSelect = index; inputValue.ano = ano.nome}"
              >
                <p
                  class="font-italic text-uppercase text-monospace m-1 text-black"
                  :class="{'text-light': index === authForm.elementSelect}"
                >
                  {{ ano.nome }}
                </p>
              </b-list-group-item>
            </b-list-group>
          </transition>
        </div>
        </form>     
        <template #modal-footer>
          <div class="w-100">
            
            <b-button
              variant="primary"
              size="sm"
              class="float-right "
              @click="authForm.keyEnter('idAno'), placa.show()"
              :disabled="!authForm.validar_input"
            >
              Proximo
            </b-button>
            <b-button
              variant="danger"
              size="sm"
              class="float-right mr-2"
              @click="authForm.resetDadosVeiculo(), ano.hide()"
            >
              Fechar
            </b-button>
          </div>
        </template>
    </b-modal>

    <b-modal
      id="modalPlaca"
      ref="placa"
      @show="ano.hide()"
      @shown="autoFocusInput('placaInput')"
      @hide="placa.hide()"
      @hidden="resetInput('placa')"
      @ok="caixaDialogo()"
      lazy
      >
      <form ref="form"
      @submit.prevent="caixaDialogo()"
      >
        <b-form-group
          label="placa"
          label-for="placaInput"
          invalid-feedback="Informe um placa valido!"
          :state="authForm.validar_input"
        >
            <b-form-input
            id="placaInput"
            size="lg"
            type="text"
            placeholder="Selecione o placa"
            class="text-uppercase"
            required
            minlength="7"
            v-model="inputValue.placa"
            @input="() => {validarPlaca(inputValue.placa)}"
            @keyEnter.prevent="caixaDialogo()"
            @keyup.esc="authForm.resetDadosVeiculo()"
            :state="authForm.validar_input"
            trim
            autocomplete="off"

          ></b-form-input>
        </b-form-group>  
        
        </form>     
        <template #modal-footer>
          <div class="w-100">
            
            <b-button
              variant="primary"
              size="sm"
              class="float-right "
              @click="caixaDialogo()"
              :disabled="!authForm.validar_input"
            >
              Salvar
            </b-button>
            <b-button
              variant="danger"
              size="sm"
              class="float-right mr-2"
              @click="authForm.resetDadosVeiculo(), placa.hide()"
            >
              Fechar
            </b-button>
          </div>
        </template>
    </b-modal>

    <b-modal 
      v-model="state.modalShow" 
      :title="state.modalTitle" 
      size="sm" button-size="sm" 
      :ok-variant="state.modalOkVariant" 
      header-class="p-2 border-bottom-0" 
      footer-class="p-2 border-top-0" 
      centered="true" 
      ok-only 
      @ok="$emit('clickEvent'), placa.hide()"
    >
      <p>{{ state.mensagem }}</p>
    </b-modal>
    
  </b-container>

</template>

<script setup>
  
  import { reactive, ref} from 'vue';
  
  import {formAuth} from '@/store/authForm.js'
  
  
  const authForm = formAuth();
  const inputValue = reactive({});
  const modelo = ref(null);
  const marca = ref(null);
  const ano = ref(null);
  const placa = ref(null);
  const placaRegex = /^([A-Z]{3}\d{4}$|^[A-Z]{3}\d[A-Z]\d{2})$/i;
  const state = reactive({
    modalShow: null,
    modalTitle: '',
    modalOkVariant: '',
    mensagem: '',
  });

  

  async function caixaDialogo() {

    try {
      const resposta = await authForm.salvarVeiculo(inputValue.placa);

      if (resposta.status !== 200) {
        state.modalOkVariant = "danger";
        state.modalTitle = 'Falha!';
      } else {
        state.modalOkVariant = "success";
        state.modalTitle = 'Sucesso!';
      }

      state.mensagem = resposta.message && typeof resposta.message === 'object' ? resposta.message.message : resposta.message;
      state.modalShow = true;
      console.log(state.mensagem)
    } catch (error) {
      console.error('Erro ao chamar salvarVeiculo:', error.message);
      state.modalOkVariant = "danger";
      state.modalTitle = 'Falha!';
      state.mensagem = 'Tente novamente mais tarde!'
      state.modalShow = true;
    }
  }

  async function validarPlaca(placa){
    authForm.validar_input = await placaRegex.test(placa);
  }

  function autoFocusInput(idInput){
    const input = document.getElementById(idInput );
    if (input){
      input.focus();
    }
  }

  function resetInput(str){  
    authForm.input = '';
    authForm.validar_input = null;
    authForm.listaFiltrada = [];
    inputValue[str] = authForm.input;
  }

  function getInput(str){
    authForm.input = str;
  }

  function scrollToElement() {
    const elemento = document.getElementById(authForm.elementSelect);
    
    if (elemento) {
      elemento.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
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