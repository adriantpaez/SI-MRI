<template>
  <div>
    <b-card
      :title="title"
      :sub-title="author"
      v-if="!loading"
      @click="sendClick"
    >
      <b-card-text>
        {{ preview }}
      </b-card-text>
    </b-card>
    <b-card :title="'Cargando...'" v-else> </b-card>
  </div>
</template>

<script>
import { documentPreview } from "../api/api";

export default {
  name: "DocumentPreview",
  props: {
    id: Number,
  },
  data() {
    return {
      title: "",
      author: "",
      preview: "",
      loading: true,
    };
  },
  mounted() {
    documentPreview(this.id).then((response) => {
      var data = response.data;
      this.title = data.title;
      this.author = data.author;
      this.preview = data.preview;
    });
    this.loading = false;
  },
  methods: {
    sendClick() {
      this.$emit("click", this.id);
    },
  },
};
</script>

<style>
</style>