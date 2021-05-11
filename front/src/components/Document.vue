<template>
  <div >
    <b-card :title="title" :sub-title="author">
      <b-card-text>
        {{ preview }}
      </b-card-text>
    </b-card>
  </div>
</template>

<script>
export default {
  name: "Document",
  props: {
    id: Number,
  },
  data() {
    return {
      title: String,
      author: String,
      preview: String,
    };
  },
  beforeMount() {
    this.title = "Title";
    this.author = "Author";
    this.preview = "Preiew...";
  },
};
</script>

<style>
</style>