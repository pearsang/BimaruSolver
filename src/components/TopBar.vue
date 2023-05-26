<template>
  <v-card class="mx-auto mb-16" max-width="448">
    <v-app-bar color="grey-darken-4" elevation="3">
      <v-app-bar-title
        class="d-flex justify-star"
        style="
          font-family: 'Roboto Mono', monospace;
          font-size: 30px;
        "
      >
        BimaruSolver
      </v-app-bar-title>
      <a href="https://en.wikipedia.org/wiki/Battleship_(puzzle)" class="mx-2">
        <v-btn
        icon
        width="100px"
        class="d-flex justify-center"
        style="font-size: 15px; color: white"
      >Rules</v-btn>
      </a>
      
      <v-sheet class="d-flex justify-end" color="grey-darken-4">
        <v-img height="90" width="150" :src="imageSrc"></v-img>
      </v-sheet>
    </v-app-bar>
  </v-card>
</template>

<style lang="css"></style>

<script setup>
import { computed } from "vue";
const imageSrc = computed(() => {
  return new URL("../assets/logo.png", import.meta.url).href;
});
</script>
