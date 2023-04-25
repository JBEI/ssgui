<template>
  <v-container>
    <div class="text-center text-title">Select a run to view data</div>
    <v-text-field
      v-model="search"
      append-icon="mdi-magnify"
      label="Search"
      single-line
      hide-details
    ></v-text-field>
    <v-data-table
      :headers="headers"
      :items="runs"
      :search="search"
      :sort-by="['name']"
      :sort-desc="[true]"
      @click:row="handleRunClick"
    ></v-data-table>
  </v-container>
</template>

<script lang="ts">
import { Run } from '@/interfaces';
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserProfile, readRuns } from '../../store/main/getters';
import { dispatchGetRuns } from '../../store/main/actions';
import { commitSetActiveRun } from '@/store/main/mutations';

@Component
export default class Dashboard extends Vue {
  public headers = [
    {
      text: 'ID Number',
      sortable: true,
      value: 'id',
      align: 'left',
    },
    {
      text: 'Name',
      sortable: true,
      value: 'name',
      align: 'left',
    },
  ];
  public search: string = '';

  public async mounted() {
    await dispatchGetRuns(this.$store);
  }

  get runs() {
    return readRuns(this.$store);
  }

  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile && userProfile.full_name) {
      if (userProfile.full_name) {
        return userProfile.full_name;
      } else {
        return userProfile.email;
      }
    }
  }

  get username() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile != null) {
      return userProfile!.email.split('@')[0];
    }
  }

  get is_superuser() {
    const userProfile = readUserProfile(this.$store);
    return userProfile!.is_superuser;
  }

  public handleRunClick(run: Run) {
    commitSetActiveRun(this.$store, run);
    this.$router
      .push({
        name: 'main-run',
        params: { id: String(run.id) },
      })
      .catch((err) => {
        throw new Error(`Problem handling something: ${err}.`);
      });
  }
}
</script>

<style scoped></style>
