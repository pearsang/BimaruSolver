<template>
  <v-card class="elevation-6 mx-auto mt-16" width="650px" height="650px">
    <v-container>
      <v-row v-for="n in 10" :key="n">
        <v-col v-for="n in 10" :key="n">
          <v-card width="40px" height="40px" color="light-blue-darken-4">
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script setup></script>

<style scoped></style>
