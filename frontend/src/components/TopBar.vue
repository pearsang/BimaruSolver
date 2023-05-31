<template>
  <v-card class="mb-16" max-width="448">
    <v-app-bar color="grey-darken-4" elevation="3" class="d-flex mb-6">
      <v-sheet color="grey-darken-4" class="ml-2 pl-2 mr-0 pr-0">
        <v-app-bar-title
          style="font-family: 'Roboto Mono', monospace; font-size: 30px"
        >
          BimaruSolver
        </v-app-bar-title>
      </v-sheet>

      <v-sheet class="mb-2 ml-2 me-auto" color="grey-darken-4">
        <v-img height="90" width="90" :src="imageSrc" cover></v-img>
      </v-sheet>

      <v-sheet color="grey-darken-4">
        <Modal />
      </v-sheet>
      <v-sheet class="ma-2 pa-2" color="grey-darken-4">
        <a href="https://en.wikipedia.org/wiki/Battleship_(puzzle)">
          <v-btn
            icon
            width="100px"
            style="font-family: 'Roboto Mono', monospace; font-size: 20px"
            >Rules</v-btn
          >
        </a>
      </v-sheet>
    </v-app-bar>
  </v-card>
</template>

<style lang="css"></style>

<script setup>
import { computed } from "vue";
import Modal from "./Modal.vue";

const imageSrc = computed(() => {
  return new URL("../assets/logo.png", import.meta.url).href;
});
</script>
