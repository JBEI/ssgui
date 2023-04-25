<template>
  <v-container style="max-width: 800px">
    <v-card @click="updateDatabase">
      <div class="text-center headline primary--text">
        Update Full Database
      </div>
    </v-card>
    <v-card @click="purgeCeleryQueue" class="mt-4">
      <div class="text-center headline primary--text">
        Purge Celery Queue
      </div>
    </v-card>
    <div class="text-center text-title mt-4">Active Celery Workers</div>
    <v-data-table
      :headers="celeryWorkerHeaders"
      :items="celeryWorkers"
      :sort-by="['name']"
      :sort-desc="[true]"
      hide-default-header
      hide-default-footer
      disable-pagination
    ></v-data-table>

    <div class="text-center text-title mt-4">Active Tasks</div>
    <v-data-table
      :headers="activeCeleryTaskHeaders"
      :items="activeCeleryTasks"
      hide-default-footer
      disable-pagination
    ></v-data-table>

    <div class="text-center text-title mt-4">Reserved Tasks</div>
    <v-data-table
      :headers="reservedCeleryTaskHeaders"
      :items="reservedCeleryTasks"
    ></v-data-table>

    <div class="text-center text-title mt-4">Runs in /diva share</div>
    <v-data-table
      :headers="divaRunHeaders"
      :items="divaRuns"
      :sort-by="['name']"
      :sort-desc="[true]"
      hide-default-header
      hide-default-footer
      disable-pagination
    >
      <template v-slot:[`item.name`]="{ item }">
        {{ item.name }}
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn text icon @click="handleRunClick(item)">
              <v-icon v-on="on">mdi-plus-box</v-icon>
            </v-btn>
          </template>
          <span>Add task to update this run</span>
        </v-tooltip>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  dispatchUpdateDatabase,
  dispatchPurgeCeleryQueue,
  dispatchGetCeleryWorkers,
  dispatchGetActiveCeleryTasks,
  dispatchGetReservedCeleryTasks,
  dispatchGetDivaRuns,
  dispatchUpdateDatabaseRun
} from '@/store/main/actions';
import {
  readCeleryWorkers,
  readActiveCeleryTasks,
  readReservedCeleryTasks,
  readRawDivaRuns
} from '@/store/main/getters';
import { RawDivaRun } from '@/interfaces';

@Component
export default class ManageDatabase extends Vue {
  public async mounted() {
    await dispatchGetCeleryWorkers(this.$store);
    await dispatchGetActiveCeleryTasks(this.$store);
    await dispatchGetReservedCeleryTasks(this.$store);
    await dispatchGetDivaRuns(this.$store);
  }

  public async updateDatabase() {
    await dispatchUpdateDatabase(this.$store);
  }

  public async purgeCeleryQueue() {
    await dispatchPurgeCeleryQueue(this.$store);
  }

  public celeryWorkerHeaders = [
    {
      text: 'Name',
      sortable: true,
      value: 'name',
      align: 'left'
    }
  ];
  get celeryWorkers() {
    return readCeleryWorkers(this.$store);
  }

  public activeCeleryTaskHeaders = [
    {
      text: 'ID',
      sortable: true,
      value: 'id',
      align: 'left'
    },
    {
      text: 'Type',
      sortable: true,
      value: 'name',
      align: 'left'
    },
    {
      text: 'Details',
      sortable: true,
      value: 'details',
      align: 'left'
    }
  ];
  get activeCeleryTasks() {
    return readActiveCeleryTasks(this.$store);
  }

  public reservedCeleryTaskHeaders = [
    {
      text: 'ID',
      sortable: true,
      value: 'id',
      align: 'left'
    },
    {
      text: 'Type',
      sortable: true,
      value: 'name',
      align: 'left'
    },
    {
      text: 'Details',
      sortable: true,
      value: 'details',
      align: 'left'
    }
  ];
  get reservedCeleryTasks() {
    return readReservedCeleryTasks(this.$store);
  }

  public divaRunHeaders = [
    {
      text: 'Name',
      sortable: true,
      value: 'name',
      align: 'left'
    }
  ];
  get divaRuns() {
    return readRawDivaRuns(this.$store);
  }

  public async handleRunClick(run: RawDivaRun) {
    const runBasename = run.name.split('/').pop();
    if (runBasename !== undefined) {
      await dispatchUpdateDatabaseRun(this.$store, runBasename);
      await dispatchGetActiveCeleryTasks(this.$store);
      await dispatchGetReservedCeleryTasks(this.$store);
    }
  }
}
</script>
