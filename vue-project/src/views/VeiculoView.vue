<script setup>
    import axiosInstance from '@/services/http.js';
    import RegistrarVeiculo from '@/components/CadastroVeiculoComponents.vue'
    import InputComponents from '@/components/InputComponents.vue'
    import { ref, onMounted } from 'vue';
    import {formAuth} from '@/store/authForm.js'
  
  
    const authForm = formAuth();
    const show = ref(false);
    const name = ref('flip-list');
    const carList = ref([]);
    const conter = ref(0)
    
    const fields = [
        {key: 'marca', label: 'Marca', sortable: true},
        {key: 'modelo', label: 'Modelo', sortable: true},
        {key: 'ano_modelo', label: 'Ano', sortable: true},
        {key: 'placa', label: 'Placa', formatter: formataPlaca , sortable: true},
        {key: 'delete', label: ''}
    ]
    authForm.placeholder = 'novo titulo';

    function formataPlaca(placa){

        const placaMercosul = /^[A-Z]{3}\d[A-Z]\d{2}$/i;
        
        if (placa.length <= 7){
            
            const letras = placa.substring(0, 3).toUpperCase();
            const numeros = placa.substring(3)
            
            if(placaMercosul.test(placa)){
                return placa.toUpperCase();
            }
            return `${letras}-${numeros}`;
        }

    }

    async function getListCar(){
        
        // isBusy.value = true;

        try {
            const response = await axiosInstance.post('listaVeiculo');
            carList.value = response.data.veiculo;
            // isBusy.value = false;
        } catch (error) {
            console.error('Erro ao carregar a lista de veiculos:', error.message);
        }
    }   
    
    onMounted(() =>{
        getListCar();
    });


    // onUpdated(() =>{
    // });
    // onBeforeMount(() =>{
    // onBeforeUpdate(() =>{
    //     console.log("onBeforeUpdate");
    // }); 

    // onUpdated(() =>{
    //     console.log("onUpdated");
    // });

    // onBeforeUnmount,(() =>{
    //     console.log("onBeforeUnmount");
    // });

    // onUnmounted(() =>{
    //     console.log("onUnmounted");
    // });

</script>

<template>
    <b-container class="mt-4">
        <div>
            <b-overlay 
            no-center 
            :show="show"
            variant="dark"
            :opacity=0.97>
                
                    <b-table 
                        id="table"
                        sticky-header="500px"
                        striped 
                        over 
                        :items="carList" 
                        :fields="fields"
                        :busy="isBusy"
                        :tbody-transition-props="name.value"
                        primary-key="marca" 
                    >
                        <template #cell(delete)>
                                <b-button variant="danger" size="sm" class="mr-2">
                                    <b-icon   icon="trash-fill" aria-hidden="true"></b-icon>
                                </b-button>
                        </template>                  
                    </b-table>
                    <template #overlay>
                        
                        <div v-if="show" class="h-100 justify-content-center d-flex align-items-center">
                            
                            <InputComponents/>
                            
                        </div>
                   
                    </template>
            
            </b-overlay>
        </div>
        <b-button @click="show = !show">Abrir modal</b-button>
        <!-- <RegistrarVeiculo @clickEvent="getListCar"/> -->
        
    </b-container>
</template>


<!-- adicionar o esqueleto para o carregamento par cadastroVeiculoComponts -->