<template>
        <v-col cols="auto">
      <v-dialog
        transition=""
        width="auto"
      >
        <template v-slot:activator="{ props }">
          <v-btn
            color="primary"
            v-bind="props"
          >From the top</v-btn>
        </template>
        <template v-slot:default="{ isActive }">
          <v-card>
            <v-toolbar
              color="primary"
              title="Opening from the top"
            ></v-toolbar>
            <v-card>
                <v-text-field
                    width="100%"
                    max-height="500%"
                  label="Legal middle name"
                  hint="example of helper text only on focus"
                ></v-text-field>
            </v-card>
            <v-card-actions class="justify-end">
              <v-btn
                variant="text"
                @click="isActive.value = false"
              >Close</v-btn>
            </v-card-actions>
          </v-card>
        </template>
      </v-dialog>
    </v-col>

</template>


<script setup>
const openModal = async () => {

    isActive.value = true;
};

</script>