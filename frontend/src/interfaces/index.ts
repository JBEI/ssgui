export interface IUserProfile {
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name: string;
  id: number;
}

export interface IUserProfileUpdate {
  email?: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface IUserProfileCreate {
  email: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface Run {
  name: string;
  id: number;
}

export interface Template {
  name: string;
  gff: string;
  genome: string;
  length: number;
  run_id: number;
  id: number;
}

export interface Sample {
  name: string;
  bam: string;
  vcf: string;
  snapshot: string;
  n_reads: number;
  n_r1_reads_aligned: number;
  n_r2_reads_aligned: number;
  average_coverage: number;
  percent_complete: number;
  median_insert_length: number;
  snps: number;
  insertions: number;
  deletions: number;
  template_id: number;
  user_id: number;
  id: number;
}

export interface IGVTrack {
  type: string;
  format: string;
  name: string;
  url: string;
  indexURL: string;
}

export interface IGVView {
  fasta_url: string;
  index_url: string;
  tracks: IGVTrack[];
}

export interface SamplePlusIGV {
  sample: Sample;
  template: Template;
  igvView: IGVView;
}

export interface CeleryWorker {
  name: string;
}

export interface CeleryTask {
  id: string;
  name: string;
  hostname: string;
  time_start: number | null;
  acknowledged: boolean;
  worker_pid: number | null;
  details: string;
}

export interface RawDivaRun {
  name: string;
}
