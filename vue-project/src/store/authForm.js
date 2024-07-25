import {ref, reactive} from 'vue';
import { defineStore } from 'pinia';
import axiosInstance from '@/services/http.js';
import axios from 'axios';

export const formAuth = defineStore('authForm', () =>{
    
  
  const input = ref('');
  const carData = ref([]);
  const transicaoKey = ref(0);
  const elementSelect = ref();
  const listaFiltrada = ref([]);
  const validar_input = ref(null);
  const keyCar = reactive({});
  

  async function salvarVeiculo(){
    
    try {
      
      const response = await axiosInstance.post('veiculo', keyCar);
      console.log('Registro bem-sucedido:', response.data);
      console.log('response.data[0]: ', response.data[0].message);  
      return {
        message: response.data[0].message,
        status: response.data[1],
      };
    } catch (error) {
      console.error('Erro ao registrar veiculo:', error.message);
      return {
        message: error.message,
        status: 401,
      };
    }
  }

  // async function carregaAno(){ 
    
  //   try {
  //       const response = await axios.get('https://parallelum.com.br/fipe/api/v1/carros/marcas/' + keyCar.marca + '/modelos/' + keyCar.modelo + '/anos')

  //   if (response.data) {
      
  //       carData.value = response.data;
      
  //   } else {
  //       console.error('A resposta da API não contém dados esperados.');
  //   }
  //   } catch (error) {
  //   console.error('Erro ao buscar dados:', error?.response?.data);
  //   }
  // }

  // async function carregaModelos(){ 

  //     try {
  //         const response = await axios.get('https://parallelum.com.br/fipe/api/v1/carros/marcas/'+ keyCar.marca +'/modelos');

  //     if (response.data) {
  //         carData.value = response.data.modelo;
  //         console.log(carData.value);
  //     } else {
  //         console.error('A resposta da API não contém dados esperados.');
  //     }
  //     } catch (error) {
  //         console.error('Erro ao buscar dados:', error?.response?.data);
  //     }
  // }

  // async function carregaMarcas(){

  //     try {
  //     const response = await axios.get('https://parallelum.com.br/fipe/api/v1/carros/marcas');

  //     if (response.data) {
  //         carData.value = response.data;
  //         console.log(carData.value)
  //     } else {
  //         console.error('A resposta da API não contém os dados esperados.');
  //     }
  //     } catch (error) {
  //     console.error('Erro ao buscar dados:', error?.response?.data);
  //     }
  // }

  async function searchCar(url){

    try {
      const response = await axios.get(url);

      if (response.data) {

          carData.value = response.data;
          console.log(carData.value);
      } else {
        console.error('A resposta da API não contém os dados esperados.');
      }
      } catch (error) {
        console.error('Erro ao buscar dados:', error?.response?.data);
      }
      
  }

  function valida_input() {
      console.log(input.value)
    
      const listArray = Array.from(carData.value);
      elementSelect.value = 0;
      
      if(input.value.length > 1){
        
          if (Array.isArray(listArray)) {
        
              listaFiltrada.value = listArray.filter((car) => car.name.toLowerCase().includes(input.value.toLowerCase()));
              transicaoKey.value = listaFiltrada.value.length;
              
              if(listaFiltrada.value.length){
                console.log('lista filtrada ', listaFiltrada.value)
                validar_input.value = true;    
              }
              else {
                validar_input.value = false;    
              }
          }
      } else {
        validar_input.value = null;
        listaFiltrada.value = null;
        transicaoKey.value += 1;
      }

  }

  function keyDown(){
    
    if (elementSelect.value >= 0 && elementSelect.value < listaFiltrada.value.length - 1){
      elementSelect.value = elementSelect.value + 1;
    } else {
      elementSelect.value = 0;
    }
  }

  function keyUp(){
    
    if (elementSelect.value > 0){
      elementSelect.value = elementSelect.value - 1;
    } else {
      elementSelect.value = listaFiltrada.value.length - 1;
    }
  }

  function keyEnter(ind) {
    
    input.value = listaFiltrada.value[elementSelect.value].name;
    keyCar[ind] = listaFiltrada.value[elementSelect.value].code;
    validar_input.value = true;
    resetInput();

  }
  
  function resetInput(){
    input.value = '';
    validar_input.value = null;
    elementSelect.value = 0;
    listaFiltrada.value = [];
  }

    return {
        salvarVeiculo,
        // carregaMarcas,
        // carregaModelos,
        // carregaAno,
        valida_input,
        searchCar,
        resetInput,
        keyCar,
        input,
        validar_input,
        elementSelect,
        keyDown,
        keyUp,
        keyEnter,
        listaFiltrada,
        transicaoKey,
    }
})