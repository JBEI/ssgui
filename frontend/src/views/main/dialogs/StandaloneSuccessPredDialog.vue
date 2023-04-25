<template>
  <v-dialog v-model="standaloneDialog" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Input Success Predictions Variables</span>
      </v-card-title>
      <v-card-text> </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancelStandaloneDialog">Cancel</v-btn>
        <v-btn @click="resetStandaloneDialog">Reset</v-btn>
        <v-btn @click="submitForm" :disabled="!validForm" color="primary"
          >Submit</v-btn
        >
        <v-btn @click="downloadResults" :disabled="!resultIsReady"
          >Download Result</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { Store } from 'vuex';
import { dispatchStandaloneSuccessPred } from '@/store/main/actions';
import { forceFileDownload } from '@/utils';
@Component
export default class StandaloneSuccessPredDialog extends Vue {
  // Common variables for Dialog
  @Prop(Boolean) active: boolean = false;
  get standaloneDialog() {
    return this.active;
  }
  set standaloneDialog(value) {
    this.$emit('update:active', value);
  }
  public validForm: boolean = false;
  public resultIsReady: boolean = false;
  // Form variables for Dialog
  public input1: File | any = null;
  public input2: File | any = null;
  // Result variables for Dialog
  public resultWorksheetFile: string = '';
  public resultWorksheetFileName: string = '';
  // Functions for Dialog
  public resetStandaloneDialog() {
    this.input1 = null;
    this.input2 = null;

    this.resultIsReady = false;
    this.resultWorksheetFile = '';
    this.resultWorksheetFileName = '';
    this.$validator.reset();
  }
  public cancelStandaloneDialog() {
    this.standaloneDialog = false;
    this.resetStandaloneDialog();
  }
  public async submitForm() {
    if (await this.$validator.validateAll()) {
      const formData = new FormData();
      formData.append(
        'input1',
        this.input1,
        this.input1.name
      );
      formData.append(
        'input2',
        this.input2,
        this.input2.name
      );
      const response = await dispatchStandaloneSuccessPred(
        this.$store,
        formData
      );
      if (response === undefined) {
        throw new Error('One of the params must be provided.');
      }
      if (response.data === undefined) {
        throw new Error('One of the params must be provided.');
      }
      const data: any = response.data;
      this.resultWorksheetFile = data.worksheet;
      this.resultWorksheetFileName = 'testing.csv';
      forceFileDownload(this.resultWorksheetFile, this.resultWorksheetFileName);
      this.resultIsReady = true;
    }
  }
  public async downloadResults() {
    if (this.resultIsReady) {
      forceFileDownload(this.resultWorksheetFile, this.resultWorksheetFileName);
    }
  }
}
</script>

<style scoped>
</style>
