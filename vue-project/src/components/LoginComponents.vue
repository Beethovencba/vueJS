<template>
    <div>
      <b-button v-b-modal.modal-prevent-closing>Open Modal</b-button>
  
      <b-modal
        id="modal-prevent-closing"
        ref="modal"
        title="Login"
        @show="resetModal"
        @hidden="resetModal"
        @ok="handleOk">

        <form ref="form" @submit.stop.prevent="handleSubmit">
          <b-form-group label="Nome de Usuário" label-for="name-input" invalid-feedback="Insira o nome de usuário!" :state="nameState">
            <b-form-input id="name-input" v-model="name" :state="nameState" required></b-form-input>
          </b-form-group>

          <b-form-group label="Password" label-for="password-input" invalid-feedback="Insira a senha!" :state="passwordState">
            <b-form-input type="password" id="password-input" v-model="password" :state="passwordState" required></b-form-input>
          </b-form-group>
        </form>
      </b-modal>
    </div>
  </template>
  
  <script>
    export default {
      data() {
        return {
          name: '',
          password: '',
          passwordState: null,
          nameState: null,
          submittedNames: []
        }
      },
      methods: {
        checkFormValidity() {
          const valid = this.$refs.form.checkValidity()
          this.nameState = valid
          return valid
        },
        resetModal() {
          this.name = ''
          this.password = ''
          this.nameState = null
        },
        handleOk(bvModalEvent) {
          // Prevent modal from closing
          bvModalEvent.preventDefault()
          // Trigger submit handler
          this.handleSubmit()
        },
        handleSubmit() {
          // Exit when the form isn't valid
          if (!this.checkFormValidity()) {
            return
          }
          // Push the name to submitted names
          this.submittedNames.push(this.name)
          // Hide the modal manually
          this.$nextTick(() => {
            this.$bvModal.hide('modal-prevent-closing')
          })
        }
      }
    }
  </script>