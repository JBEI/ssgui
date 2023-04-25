<template>
  <v-container fluid>
    <v-app-bar prominent>
      <v-toolbar-title primary-title>
        <div v-if="runIsMounted" class="headline primary--text text-truncate">
          {{ activeRun.name }}
        </div>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <div v-if="selectedSamples.length > 0">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" icon @click="downloadSelectedStats">
              <v-icon color="primary">mdi-download-circle-outline</v-icon>
            </v-btn>
          </template>
          <span>Download statistics for selected samples</span>
        </v-tooltip>
      </div>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" icon @click="downloadStats">
            <v-icon>mdi-table-arrow-down</v-icon>
          </v-btn>
        </template>
        <span>Download all statistics</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" icon @click="downloadSnapshots">
            <v-icon>mdi-folder-download</v-icon>
          </v-btn>
        </template>
        <span>Download all snapshots</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            v-on="on"
            icon
            @click="deleteConfirmationDialog = true"
            v-show="hasAdminAccess"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
        <span>Delete run</span>
      </v-tooltip>
      <v-dialog v-model="deleteConfirmationDialog" max-width="290">
        <v-card>
          <v-card-title>Delete Run</v-card-title>
          <v-card-text>
            Are you sure you want to delete run and all it's contents?
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="red darken-1"
              text
              @click="deleteConfirmationDialog = false"
            >
              Cancel
            </v-btn>
            <v-btn color="green darken-1" text @click="handleRunDelete">
              Yes
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <template v-slot:extension>
        <v-tabs v-model="tab" align-with-title grow show-arrows icons-and-text>
          <v-tab href="#stats">
            Statistics
            <v-icon>mdi-animation</v-icon>
          </v-tab>
          <v-tab href="#snapshots">
            Snapshots
            <v-icon>mdi-image</v-icon>
          </v-tab>
          <v-tab href="#igv">
            IGV
            <v-icon>mdi-play-circle</v-icon>
          </v-tab>
        </v-tabs>
      </template>
    </v-app-bar>
    <v-tabs-items v-model="tab">
      <!-- Stats Tab -->
      <v-tab-item value="stats">
        <v-data-table
          :headers="statsHeaders"
          :items="activeSamples"
          :search="search"
          item-key="sample.id"
          multi-sort
          :loading="!samplesAreMounted"
          loading-text="Loading data... please wait"
          v-model="selectedSamples"
          show-expand
          single-expand
          :expanded.sync="expandedSample"
          @item-expanded="loadIGV"
          group-by="template.name"
          show-select
        >
          <template v-slot:top>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </template>
          <template v-slot:[`item.sample.percent_complete`]="{ item }">
            <v-chip
              :color="getPercentCompleteColor(item.sample.percent_complete)"
              outlined
            >
              <v-icon left>
                {{ getPercentCompleteIcon(item.sample.percent_complete) }}
              </v-icon>
              {{ item.sample.percent_complete.toFixed(1) }}%
            </v-chip>
          </template>
          <template v-slot:[`item.sample.snps`]="{ item }">
            <v-chip :color="getVariantColor(item.sample.snps)" outlined>
              <v-icon left>
                {{ getVariantIcon(item.sample.snps) }}
              </v-icon>
              {{ item.sample.snps }}
            </v-chip> </template
          ><template v-slot:[`item.sample.insertions`]="{ item }">
            <v-chip :color="getVariantColor(item.sample.insertions)" outlined>
              <v-icon left>
                {{ getVariantIcon(item.sample.insertions) }}
              </v-icon>
              {{ item.sample.insertions }}
            </v-chip> </template
          ><template v-slot:[`item.sample.deletions`]="{ item }">
            <v-chip :color="getVariantColor(item.sample.deletions)" outlined>
              <v-icon left>
                {{ getVariantIcon(item.sample.deletions) }}
              </v-icon>
              {{ item.sample.deletions }}
            </v-chip>
          </template>
          <template v-slot:[`item.sample.id`]="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on" @click="downloadSampleData(item)"
                  >mdi-download</v-icon
                >
              </template>
              <span>Download raw sample data</span>
            </v-tooltip>
          </template>
          <template v-slot:expanded-item="{ headers, item }">
            <td :colspan="headers.length">
              <div class="text-center">
                <v-btn rounded outlined @click="tab = 'igv'"
                  >View live IGV for sample {{ item.sample.name }}
                  <small>(ID: {{ item.sample.id }})</small></v-btn
                >
              </div>
            </td>
          </template></v-data-table
        >
      </v-tab-item>
      <!-- Snapshots Tab -->
      <v-tab-item value="snapshots">
        <v-container>
          <v-data-iterator
            :items="activeSamples"
            item-key="sample.id"
            :group-by="groupbyVariable"
            :search="search"
            :custom-filter="customFilter"
          >
            <template v-slot:header>
              <v-toolbar flat>
                <v-text-field
                  v-model="search"
                  append-icon="mdi-magnify"
                  label="Search"
                  single-line
                  hide-details
                ></v-text-field>
              </v-toolbar>
            </template>
            <template v-slot:default="props">
              <v-item-group
                active-class="primary"
                multiple
                v-model="selectedSamples"
              >
                <div
                  v-for="groupedItem in props.groupedItems"
                  :key="groupedItem.name"
                >
                  <v-container>
                    <v-row>
                      <div>{{ groupedItem.name }}</div>
                      <v-col
                        v-for="item in groupedItem.items"
                        :key="item.sample.id"
                        cols="12"
                        sm="6"
                        md="4"
                        lg="3"
                      >
                        <v-item v-slot="{ active, toggle }" :value="item">
                          <v-card
                            :color="active ? 'primary' : ''"
                            class="hover-pointer"
                          >
                            <v-card-title
                              @click="toggle"
                              class="text-subtitle-1"
                            >
                              {{ item.sample.name }}
                            </v-card-title>
                            <v-card-subtitle @click="toggle"
                              >{{ item.template.name }}
                              <v-btn icon>
                                <v-icon>
                                  {{
                                    active
                                      ? 'mdi-checkbox-marked-outline'
                                      : 'mdi-checkbox-blank-outline'
                                  }}
                                </v-icon>
                              </v-btn>
                            </v-card-subtitle>
                            <div
                              class="snapshot-img-wrapper"
                              @click="zoomImage(item)"
                            >
                              <v-img
                                v-bind:src="
                                  `data:image/png;base64,${item.sample.snapshot}`
                                "
                                contain
                                aspect-ratio="1"
                                class="snapshot-img grey lighten-2"
                              >
                                <template v-slot:placeholder>
                                  <v-row
                                    class="fill-height ma-0"
                                    align="center"
                                    justify="center"
                                  >
                                    <v-progress-circular
                                      indeterminate
                                      color="grey lighten-5"
                                    ></v-progress-circular>
                                  </v-row>
                                </template>
                              </v-img>
                              <v-icon class="snapshot-img-icon">
                                mdi-magnify-plus
                              </v-icon>
                            </div>
                          </v-card>
                        </v-item>
                      </v-col>
                    </v-row>
                    <v-divider></v-divider>
                  </v-container>
                </div>
              </v-item-group>
            </template>
          </v-data-iterator>
        </v-container>
      </v-tab-item>
      <v-dialog v-model="zoomedSampleDialog" max-width="75vw">
        <v-card v-if="zoomedSample" @click.stop="unzoomImage()">
          <v-card-title v-text="zoomedSample.sample.name"></v-card-title>
          <v-card-subtitle
            v-text="zoomedSample.template.name"
          ></v-card-subtitle>
          <v-img
            v-bind:src="`data:image/png;base64,${zoomedSample.sample.snapshot}`"
          ></v-img
        ></v-card>
      </v-dialog>
      <!-- IGV Tab -->
      <v-tab-item value="igv" eager>
        <v-container>
          <div v-if="!expandedSample.length" class="text-center text-title">
            Expand a sample in stats page to view in IGV. May take a minute to
            load data.
          </div>
          <div v-else class="text-center text-title">
            May take a minute to load data...
          </div>
          <!-- <v-sparkline
            line-width="1"
            :gradient="['yellow', 'pink', 'purple']"
            smooth
            padding="25"
            :value="coverageData"
            auto-draw
          ></v-sparkline> -->
          <div id="igv-div" style="overflow-x: auto; white-space: nowrap"></div>
        </v-container>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { IGVView, SamplePlusIGV } from '@/interfaces';
import {
  readActiveRun,
  readActiveSamples,
  readHasAdminAccess
} from '@/store/main/getters';
import {
  dispatchGetRun,
  dispatchGetSamples,
  dispatchGetSnapshots,
  dispatchGetSampleData,
  dispatchGetSampleCoverage
} from '@/store/main/actions';
import { dispatchDeleteRun } from '@/store/main/actions';
import igv from 'igv';
import {
  forceFileDownload,
  defaultFilter,
  getObjectValueByPath
} from '@/utils';

@Component({
  components: {}
})
export default class UserRun extends Vue {
  public runIsMounted: boolean = false;
  public samplesAreMounted: boolean = false;

  public tab: string = 'stats';

  public deleteConfirmationDialog: boolean = false;
  public zoomedSampleDialog: boolean = false;

  public zoomedSample: SamplePlusIGV | null = null;
  public selectedSamples: SamplePlusIGV[] = [];
  public expandedSample: SamplePlusIGV[] = [];

  public groupbyVariable: string = 'template.name';

  public search: string = '';
  public statsHeaders = [
    {
      text: 'Name',
      sortable: true,
      value: 'sample.name',
      align: 'left'
    },
    {
      text: '# Reads',
      sortable: true,
      value: 'sample.n_reads',
      align: 'left'
    },
    {
      text: 'Average Coverage',
      sortable: true,
      value: 'sample.average_coverage',
      align: 'left'
    },
    {
      text: 'Percent Complete',
      sortable: true,
      value: 'sample.percent_complete',
      align: 'left'
    },
    {
      text: 'Reference ID',
      sortable: true,
      value: 'template.name',
      align: 'left'
    },
    {
      text: 'Reference Length',
      sortable: true,
      value: 'template.length',
      align: 'left'
    },
    {
      text: 'Median Insert Length',
      sortable: true,
      value: 'sample.median_insert_length',
      align: 'left'
    },
    {
      text: 'SNPs',
      sortable: true,
      value: 'sample.snps',
      align: 'left'
    },
    {
      text: 'Insertions',
      sortable: true,
      value: 'sample.insertions',
      align: 'left'
    },
    {
      text: 'Deletions',
      sortable: true,
      value: 'sample.deletions',
      align: 'left'
    },
    {
      text: 'Actions',
      sortable: false,
      value: 'sample.id',
      align: 'center'
    }
  ];

  public labels: number[] = [];
  public coverageData: number[] = [];

  public async mounted() {
    await dispatchGetRun(this.$store, +this.$router.currentRoute.params.id);
    await dispatchGetSamples(this.$store, +this.$router.currentRoute.params.id);
    this.runIsMounted = true;
    this.samplesAreMounted = true;
  }

  public get hasAdminAccess() {
    return readHasAdminAccess(this.$store);
  }

  public get activeRun() {
    return readActiveRun(this.$store);
  }

  public get activeSamples() {
    return readActiveSamples(this.$store);
  }

  public async handleRunDelete() {
    this.deleteConfirmationDialog = false;
    await dispatchDeleteRun(this.$store, +this.$router.currentRoute.params.id);
    this.$router.push({ name: 'main-dashboard' }).catch(err => {
      throw new Error(`Problem handling something: ${err}.`);
    });
  }

  public async zoomImage(samplePlusIGV: SamplePlusIGV) {
    this.zoomedSample = samplePlusIGV;
    this.zoomedSampleDialog = true;
  }
  public async unzoomImage() {
    this.zoomedSampleDialog = false;
    this.zoomedSample = null;
  }

  public getPercentCompleteColor(percentComplete) {
    if (percentComplete >= 100) return '#ffb14e';
    else if (percentComplete > 98) return '#ea5f94';
    else return '#0000ff';
  }

  public getVariantColor(variant) {
    if (variant <= 0) return '#ffb14e';
    else if (variant <= 3) return '#ea5f94';
    else return '#0000ff';
  }

  public getPercentCompleteIcon(percentComplete) {
    if (percentComplete >= 100) return 'mdi-thumb-up';
    else if (percentComplete > 98) return 'mdi-thumbs-up-down';
    else return 'mdi-thumb-down';
  }

  public getVariantIcon(variant) {
    if (variant <= 0) return 'mdi-thumb-up';
    else if (variant <= 3) return 'mdi-thumbs-up-down';
    else return 'mdi-thumb-down';
  }

  public async loadIGV({ item, value }) {
    if (value) {
      this.tab = 'igv';
      this.launchIGV(item.igv_view);
      // const response = await dispatchGetSampleCoverage(
      //   this.$store,
      //   item.sample.id
      // );
      // if (response !== undefined) {
      //   this.labels = response.data.labels;
      //   this.coverageData = response.data.values;
      // } else {
      //   this.labels = [];
      //   this.coverageData = [];
      // }
    } else {
      igv.removeAllBrowsers();
      this.labels = [];
      this.coverageData = [];
    }
  }

  public async launchIGV(igvView: IGVView) {
    const igvDiv = document.getElementById('igv-div');
    const options = {
      reference: {
        fastaURL: igvView.fasta_url,
        indexURL: igvView.index_url
      },
      tracks: igvView.tracks,
      loadDefaultGenomes: false
    };
    igv.removeAllBrowsers();
    igv.createBrowser(igvDiv, options).then(function(browser) {
      browser.zoomOut();
      browser.visibilityChange();
    });
  }

  public async downloadSampleData(item: SamplePlusIGV) {
    const response = await dispatchGetSampleData(this.$store, item.sample.id);
    if (response === undefined) {
      throw new Error('One of the params must be provided.');
    }
    if (response.data === undefined) {
      throw new Error('One of the params must be provided.');
    }
    const data: any = response.data;
    const resultZipDownload = data;
    const resultZipNameDownload = `${item.template.name}-${item.sample.name}-data.zip`;
    forceFileDownload(resultZipDownload, resultZipNameDownload);
  }

  public async downloadSnapshots() {
    var runName: string;
    if (this.activeRun) {
      runName = this.activeRun.name;
    } else {
      runName = this.$router.currentRoute.params.id;
    }
    const response = await dispatchGetSnapshots(
      this.$store,
      +this.$router.currentRoute.params.id
    );
    if (response === undefined) {
      throw new Error('One of the params must be provided.');
    }
    if (response.data === undefined) {
      throw new Error('One of the params must be provided.');
    }
    const data: any = response.data;
    const resultZipDownload = data;
    const resultZipNameDownload = `${runName}-snapshots.zip`;
    forceFileDownload(resultZipDownload, resultZipNameDownload);
  }

  public async downloadStats() {
    var runName: string;
    if (this.activeRun) {
      runName = this.activeRun.name;
    } else {
      runName = this.$router.currentRoute.params.id;
    }
    var csvString =
      'Sample_Name,#_Reads_(PF),#_R1_Reads_Aligned,#_R2_Reads_Aligned,' +
      'Average_Coverage,%_Complete,Reference_ID,Reference_Length,' +
      'Median_Insert_Length,SNPs,Insertions,Deletions\n';
    this.activeSamples.forEach((sample: SamplePlusIGV) => {
      csvString +=
        sample.sample.name +
        ',' +
        sample.sample.n_reads +
        ',' +
        sample.sample.n_r1_reads_aligned +
        ',' +
        sample.sample.n_r2_reads_aligned +
        ',' +
        sample.sample.average_coverage +
        ',' +
        sample.sample.percent_complete +
        ',' +
        sample.template.name +
        ',' +
        sample.template.length +
        ',' +
        sample.sample.median_insert_length +
        ',' +
        sample.sample.snps +
        ',' +
        sample.sample.insertions +
        ',' +
        sample.sample.deletions +
        '\n';
    });
    forceFileDownload(csvString, `${runName}-stats.csv`);
  }

  public async downloadSelectedStats() {
    var runName: string;
    if (this.activeRun) {
      runName = this.activeRun.name;
    } else {
      runName = this.$router.currentRoute.params.id;
    }
    var csvString =
      'Sample_Name,#_Reads_(PF),#_R1_Reads_Aligned,#_R2_Reads_Aligned,' +
      'Average_Coverage,%_Complete,Reference_ID,Reference_Length,' +
      'Median_Insert_Length,SNPs,Insertions,Deletions\n';
    this.selectedSamples.forEach((sample: SamplePlusIGV) => {
      csvString +=
        sample.sample.name +
        ',' +
        sample.sample.n_reads +
        ',' +
        sample.sample.n_r1_reads_aligned +
        ',' +
        sample.sample.n_r2_reads_aligned +
        ',' +
        sample.sample.average_coverage +
        ',' +
        sample.sample.percent_complete +
        ',' +
        sample.template.name +
        ',' +
        sample.template.length +
        ',' +
        sample.sample.median_insert_length +
        ',' +
        sample.sample.snps +
        ',' +
        sample.sample.insertions +
        ',' +
        sample.sample.deletions +
        '\n';
    });
    forceFileDownload(csvString, `${runName}-selected-stats.csv`);
  }

  public customFilter(items: SamplePlusIGV[], search: string) {
    if (!search) return items;
    search = search.toString().toLowerCase();
    if (search.trim() === '') return items;

    return items.filter((item: any) => {
      const flatItem = { name: item.sample.name, template: item.template.name };
      return Object.keys(flatItem).some(key =>
        defaultFilter(getObjectValueByPath(flatItem, key), search, item)
      );
    });
  }
}
</script>

<style scoped>
.hover-pointer {
  cursor: pointer;
}

.snapshot-img-wrapper {
  position: relative;
  border-width: 2px;
  border-color: grey;
  border-style: solid;
}

.snapshot-img-icon {
  position: absolute;
  top: 0;
  left: 0;
  padding: 0.5rem;
}
</style>
