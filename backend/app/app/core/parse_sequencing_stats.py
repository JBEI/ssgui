#!/usr/bin/env python

from typing import Optional, List, Dict, Tuple
import os
import glob

import pandas as pd
from pandera.typing import DataFrame

from app import schemas


def find_stats_csv_file(run_path: str) -> Optional[str]:
    """Find path to sequencing statistics file for a run"""
    stats: List[str] = glob.glob(os.path.join(run_path, "stats/*.csv"))
    if stats:
        return stats[0]
    else:
        return None


def combine_dicts(dicts: List[dict]) -> dict:
    """Combine multiple dicts into one dict"""
    super_dict = dict()
    for d in dicts:
        for k, v in d.items():
            super_dict[k] = v
    return super_dict


def parse_stats_file(
    stats_path: str,
) -> Tuple[
    Dict[str, schemas.TemplateStats], Dict[str, schemas.SampleStats]
]:
    unvalidated_stats_df: pd.DataFrame = pd.read_csv(stats_path)
    unvalidated_stats_df.columns = [
        col.replace(" ", "_") for col in unvalidated_stats_df.columns
    ]
    stats_df: DataFrame[
        schemas.SequencingStats
    ] = schemas.SequencingStats.validate(  # type: ignore
        unvalidated_stats_df
    )
    template_stats: Dict[str, schemas.TemplateStats] = combine_dicts(
        stats_df.apply(
            lambda row: {
                row[
                    schemas.SequencingStats.Reference_ID
                ]: schemas.TemplateStats(
                    length=row[schemas.SequencingStats.Reference_Length]
                )
            },
            axis=1,
        ).values
    )
    sample_stats: Dict[str, schemas.SampleStats] = combine_dicts(
        stats_df.apply(
            lambda row: {
                row[
                    schemas.SequencingStats.Sample_Name
                ]: schemas.SampleStats(
                    n_reads=row[schemas.SequencingStats.N_Reads],
                    n_r1_reads_aligned=row[
                        schemas.SequencingStats.N_R1_Reads_Aligned
                    ],
                    n_r2_reads_aligned=row[
                        schemas.SequencingStats.N_R2_Reads_Aligned
                    ],
                    average_coverage=row[
                        schemas.SequencingStats.Average_Coverage
                    ],
                    percent_complete=row[
                        schemas.SequencingStats.Percent_Complete
                    ],
                    median_insert_length=row[
                        schemas.SequencingStats.Median_Insert_Length
                    ],
                    snps=row[schemas.SequencingStats.SNPs],
                    insertions=row[schemas.SequencingStats.Insertions],
                    deletions=row[schemas.SequencingStats.Deletions],
                )
            },
            axis=1,
        ).values
    )
    return template_stats, sample_stats
