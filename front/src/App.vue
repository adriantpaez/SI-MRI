<template>
  <div id="app">
    <Search @search="search" v-if="!onDetails" />
    <div class="mt-3 mx-5">
      <div v-if="results.length > 0 && !onDetails">
        <h2>Resultados</h2>
        <div v-for="id in results" :key="id">
          <DocumentPreview :id="id" @click="doDetails" />
        </div>
      </div>
      <div v-if="onDetails">
        <h2>{{ details.title }}</h2>
        <h5>{{ details.author }}</h5>
        <p>{{ details.text }}</p>
        <b-button variant="success" @click="onDetails = false">Cerrar</b-button>
      </div>
    </div>
  </div>
</template>

<script>
import Search from "./components/Search.vue";
import DocumentPreview from "./components/DocumentPreview.vue";
import { document } from "./api/api.js";

export default {
  name: "App",
  components: {
    Search,
    DocumentPreview,
  },
  data() {
    return {
      results: [],
      details: {
        author: "",
        text: "",
        title: "",
      },
      onDetails: false,
    };
  },
  methods: {
    search(results) {
      this.results = results;
    },
    doDetails(id) {
      document(id).then((response) => {
        this.details = response.data;
        this.onDetails = true;
      });
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
