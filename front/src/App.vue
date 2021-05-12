<template>
  <div id="app">
    <Search @search="search" />
    <div v-if="results.length > 0" class="mt-3 mx-5">
      <h2>Resultados</h2>
      <div v-for="id in results" :key="id">
        <DocumentPreview :id="id" />
      </div>
    </div>
  </div>
</template>

<script>
import Search from "./components/Search.vue";
import DocumentPreview from "./components/DocumentPreview.vue";

export default {
  name: "App",
  components: {
    Search,
    DocumentPreview,
  },
  data() {
    return {
      results: [],
    };
  },
  methods: {
    search(results) {
      this.results = results;
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
