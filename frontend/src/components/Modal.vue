<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent width="1024">
      <template v-slot:activator="{ props }" color="grey-darken-4">
        <v-btn
          v-bind="props"
          style="font-family: 'Roboto Mono', monospace; font-size: 20px"
        >
          Input
        </v-btn>
      </template>
      <v-card height="600px" color="grey-darken-4">
        <v-card-title>
          <span style="font-family: 'Roboto Mono', monospace; font-size: 30px"
            >Input</span
          >
        </v-card-title>
        <v-container fluid>
          <v-textarea
            ref="inputTextarea"
            name="input-7-1"
            variant="filled"
            label="Insert input here"
            rows="15"
          ></v-textarea>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false"> Close </v-btn>
          <v-btn color="blue-darken-1" variant="text" @click="saveTextFile()">
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { saveAs } from "file-saver";
import { computed } from "vue";

export default {
  data: () => ({
    dialog: false,
  }),
  computed: {
    imageSrc: () => {
      return new URL("../assets/logo.png", import.meta.url).href;
    },
  },
  methods: {
    saveTextFile() {
      const textContent = this.$refs.inputTextarea.value;
      const blob = new Blob([textContent], {
        type: "text/plain;charset=utf-8",
      });
      saveAs(blob, "input.txt");
      console.log(textContent);
      this.dialog = false;
    },
  },
};
</script>
