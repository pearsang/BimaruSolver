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
                  : board[row - 1][col - 1]
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
        @click="solve"
        >Solve</v-btn
      >
    </v-col>
  </v-container>
</template>

<script setup>
import axios from "axios";
import { computed } from "vue";
import { ref } from "vue";

const API_URL = "http://127.0.0.1:5000/";
const board = ref([
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
]);

const solve = async () => {
  const response = await axios.get(API_URL);
  console.log(response.data);

  const n_steps = response.data.length;
  for (let i = 0; i < n_steps; i++) {
    // numero de steps
    let count = 0;
    for (let j = 0; j < 10; j++) {
      // numero de posicoes
      for (let k = 0; k < 10; k++) {
        // text to emoji
        const value = response.data[i][count++];
        if (value === "." || value === "W") {
          board.value[j][k] = "﹌";
        } else if (value === "C" || value === "c") {
          board.value[j][k] = "●";
        } else if (value === "R" || value === "r") {
          board.value[j][k] = "►";
        } else if (value === "L" || value === "l") {
          board.value[j][k] = "◄";
        } else if (value === "B" || value === "b") {
          board.value[j][k] = "▼";
        } else if (value === "T" || value === "t") {
          board.value[j][k] = "▲";
        } else if (value === "M" || value === "m") {
          board.value[j][k] = "■";
        }
        else {
          board.value[j][k] = " ";
        }
      }
    }
    await new Promise((r) => setTimeout(r, 200));
  }
};
</script>

<style scoped></style>
