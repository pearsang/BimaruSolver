<template>
  <v-card class="elevation-6 mx-auto mt-16">
    <v-container>
      <v-row v-for="n in 10" :key="n" class="pa-0 ma-0">
        <v-col v-for="n in 10" :key="n" class="pa-0 ma-0">
          <v-card width="50px" height="50px" color="light-blue-lighten-4" class="pa-0 ma-0">
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script setup></script>

<style scoped></style>
