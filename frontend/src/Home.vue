<template>
  <v-app id="app">

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
  background-color: rgb(198, 233, 225);
}

 a, a:hover, a:focus, a:active {
      text-decoration: none;
      color: inherit;
 }
</style>
