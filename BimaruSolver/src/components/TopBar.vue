<template>
  <v-card class="mx-auto mb-16" max-width="448">
    <v-app-bar color="rgb(48, 227, 202)" class="mx-auto" elevation="3">
      <v-app-bar-title
        class="text-left font-weight-medium"
        style="font-size: 20px"
        color="rgb(64, 81, 78)"
      >
        BimaruSolver
      </v-app-bar-title>

      <v-app-bar-nav-icon class="mr-14 mt-0">
        <v-img
          height="100"
          width="100"
          :src="imageSrc"
        ></v-img>
      </v-app-bar-nav-icon>
      
    </v-app-bar>
  </v-card>
</template>

<style lang="css"></style>

<script setup>
  import { computed } from "vue";
  const imageSrc = computed(() => {
        return new URL("../assets/boat.png", import.meta.url).href;
      });
</script>   


