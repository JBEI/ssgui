# About

Welcome to SSGUI, an application designed to help you analyze your next-generation sequencing (NGS) data. In collaboration with the DiVa-Seq team at ESE, we have developed this service to allow you to quickly visualize, analyze, and save your NGS data.

# Get Started

From the home page of this site, you will be able to see all sequencing runs for which you have submitted samples. The email address provided upon sample submission is the sample owner and will be the only user able to view the data associated with their submitted samples.

<div class="image">
    <figure>
        <img src="/img/dashboard-view.png" alt="Dashboard View">
        <figcaption>View of SSGUI dashboard showing available runs</figcaption>
    </figure>
</div>

Click on a run and you will be able to see a table containing statistics about each sample you submitted for that particular run. Your samples are grouped by template ID to allow for quick analysis in the case that you submitted multiple samples for a single template.

<div class="image">
    <figure>
        <img src="/img/run-view.png" alt="Run View">
        <figcaption>View of a run showing each sample grouped by template</figcaption>
    </figure>
</div>

<div class="note">

**Note:**
You can use the search bar to quickly filter your samples

</div>

To download the raw data associated with a particular sample click the download icon on the right-side of a sample row. Clicking the icon will retrieve and download a `.zip` file containing the following sample data files:

1. `*sample*.bam`
2. `*sample*.bam.bai`
3. `*sample*.vcf`
4. `*sample*.vcf.idx`
5. `*reference*.fa`
6. `*reference*.fa.fai`

To view an individual sample in the [Integrative Genomics Viewer (IGV)](https://software.broadinstitute.org/software/igv/), expand the sample by clicking the arrow icon on the left of the sample. Clicking the icon will redirect you to the _IGV_ tab where the data associated with that sample will be loaded into the browser allowing for dynamic visualization of your NGS data.

<div class="image">
    <figure>
        <img src="/img/igv-view.png" alt="IGV View">
        <figcaption>View of IGV displaying NGS data</figcaption>
    </figure>
</div>

<div class="note">

**Note:**
As you are browsing IGV, you may at any point use the built-in download button to download a snapshot of your data. Just right-click the IGV window and Save Image. You can download the snapshot either as an `.svg` or `.png` file.

</div>

<div class="warn">

**Warning:**
Please allow for a lag time when viewing your data in IGV as the raw data is fairly large and needs to be transported into your browser.

</div>

Alternatively, you can navigate to the _Snapshots_ tab to view snapshots for each of your samples.

<div class="image">
    <figure>
        <img src="/img/snapshots-view.png" alt="Snapshots View">
        <figcaption>Snapshots tab displaying IGV images of each sample</figcaption>
    </figure>
</div>

<div class="note">

**Note:**
You may expand the image into a bigger view by clicking on any image.

</div>

Lastly, at any point that you are analyzing your data on the run page, you can download a `.zip` file containing the snapshots for each of your samples by clicking the Download button located on the top right corner of the page.

# FAQs

### How can I share my data with collaborators?

You must download your data to share it.

### What do the colors on the stats page mean?

The colors on the "Percent Complete" column correspond to:

- yellow: 100%
- pink: >98%
- blue: <= 98%

The colors on the "SNPs", "Insertions", and "Deletions" columns correspond to:

- yellow: 0 variants
- pink: <=3 variants
- blue: >3 variants

### Is there an API?

Yes! You may access the API documentation at `/docs`. However, be wary that many of the endpoints require superuser credentials.
