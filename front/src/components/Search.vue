<template>
  <div class="mx-5" style="text-align: center">
    <b-form-input
      class="mb-3"
      v-model="query"
      placeholder="Realice una busqueda..."
    ></b-form-input>
    <b-button variant="outline-primary">Buscar</b-button>
  </div>
</template>

<script>
export default {
  name: "Search",
  data() {
    return {
      query: "",
    };
  },
};
</script>

<style>
</style>