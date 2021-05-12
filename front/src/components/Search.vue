<template>
  <div class="mx-5" style="text-align: center">
    <b-form-input
      class="mb-3"
      v-model="query"
      placeholder="Realice una busqueda..."
    ></b-form-input>
    <b-button variant="outline-primary" @click="doSearch">Buscar</b-button>
  </div>
</template>

<script>
import { search } from "../api/api";

export default {
  name: "Search",
  data() {
    return {
      query: "",
    };
  },
  methods: {
    doSearch() {
      search(this.query).then((response) => {
        var data = response.data;
        this.$emit("search", data);
      });
    },
  },
};
</script>

<style>
</style>