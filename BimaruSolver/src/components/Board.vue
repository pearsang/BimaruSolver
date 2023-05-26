<template>
  <v-card class="elevation-6 mx-auto mt-16">
    <v-container>
      <v-row v-for="row in 11" :key="row" class="pa-0 ma-0">
        <v-col v-for="col in 11" :key="col" class="pa-0 ma-0" board>
          <v-card
            width="50px"
            height="50px"
            class="pa-0 ma-0 rounded-0"
            :color="
              row === 11 || col === 11
                ? 'blue-grey-darken-4'
                : 'light-blue-lighten-5'
            "
            style="border: 1px solid black"
          >
            <v-card-text class="px-0" style="font-size: 20px">
              {{
                row === 11 && col !== 11
                  ? col
                  : col === 11 && row !== 11
                  ? row
                  : ""
              }}
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
  <v-container>
    <v-col cols="auto">
      <v-btn
        size="large"
        color="blue-grey-darken-4"
        style="font-family: 'Roboto Mono', monospace; border-radius: 5px"
        width="120px"
        >Solve</v-btn
      >
    </v-col>
  </v-container>
</template>

<script setup></script>

<style scoped></style>
