<template>
  <v-app>

    <TopBar />
    <Board /> 
    <FooterBar />

  </v-app>
</template>

<script setup lang="ts">
import Board from './components/Board.vue';
import TopBar from './components/TopBar.vue';
import FooterBar from './components/FooterBar.vue';
</script>

<style>
#app {
  text-align: center;
}

body {
  background-color: rgb(228, 249, 245);
}
</style>
