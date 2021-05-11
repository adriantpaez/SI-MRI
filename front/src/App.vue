<template>
  <div id="app">
    <Search />
    <div v-if="results.length > 0" class="mt-3 mx-5">
      <h2>Resultados</h2>
      <div v-for="id in results" :key="id">
        <Document :id="id" />
      </div>
    </div>
  </div>
</template>

<script>
import Search from "./components/Search.vue";
import Document from "./components/Document.vue";

export default {
  name: "App",
  components: {
    Search,
    Document,
  },
  data() {
    return {
      results: [],
    };
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
