<template>
  <v-container style="max-width: 800px">
    <div id="toc"></div>
    <div>
      <vue-markdown
        class="markdown"
        :source="admin_markdown"
        toc="true"
        toc-id="toc"
        toc-first-level="1"
        toc-last-level="5"
      ></vue-markdown>
    </div>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import VueMarkdown from 'vue-markdown';
import adminContent from '@/docs/Admin.md';

@Component({
  components: {
    VueMarkdown
  }
})
export default class AdminHelp extends Vue {
  public admin_markdown: string = '';

  public async mounted() {
    this.admin_markdown = adminContent;
  }
}
</script>

<style>
.image {
  text-align: center;
  color: #696969;
  margin: 1rem 0;
}
.image figure img {
  width: 90%;
  border-radius: 1rem;
}
.note {
  background-color: #f3f5f7;
  border-color: #2196f3;
  color: #2c3e50;
  padding: 0.1rem 1.5rem;
  border-left-width: 0.5rem;
  border-left-style: solid;
  border-radius: 0.2rem;
  box-shadow: 0 0.2rem 0.5rem rgba(0, 0, 0, 0.05),
    0 0 0.0625rem rgba(0, 0, 0, 0.1);
  margin: 1rem 0;
}
.note p {
  margin-bottom: 0;
}
.warn {
  background-color: #ffe5644d;
  border-color: #ffc107;
  color: #2c3e50;
  padding: 0.1rem 1.5rem;
  border-left-width: 0.5rem;
  border-left-style: solid;
  border-radius: 0.2rem;
  box-shadow: 0 0.2rem 0.5rem rgba(0, 0, 0, 0.05),
    0 0 0.0625rem rgba(0, 0, 0, 0.1);
  margin: 1rem 0;
}
.warn p {
  margin-bottom: 0;
}
.toc-anchor {
  display: none;
}
.markdown h1:hover .toc-anchor,
.markdown h2:hover .toc-anchor,
.markdown h3:hover .toc-anchor,
.markdown h4:hover .toc-anchor,
.markdown h5:hover .toc-anchor {
  display: inline;
}
.table-of-contents * {
  color: rgba(0, 0, 0, 0.87) !important;
  list-style-type: none;
}
.table-of-contents *:hover {
  color: #c21659 !important;
}
</style>
