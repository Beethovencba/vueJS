<template>
    <div>
        <b-modal v-model="modalShow" ok-only ok-variant="danger" ok-title="Fechar">
            <p class="my-4">Nome de usuário e/ou senha inválidos!</p>
        </b-modal>
    </div>
  </template>
  
  <script>
    export default {
      data() {
        return {
          modalShow: true
        }
      }
    }
  </script>