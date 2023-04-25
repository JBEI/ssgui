from typing import Optional, List, Generator, Tuple
import more_itertools
import pandas as pd
from pandera.typing import DataFrame

from sqlalchemy.orm import Session
from app import crud, models, schemas

from app.core.samtools import (
    parse_samtools_depth,
    run_samtools_consensus,
    run_samtools_depth,
)


def find_ranges(
    iterable: List[int],
) -> Generator[Tuple[int, int], None, None]:
    """Yield range of consecutive numbers

    Adapted from: https://stackoverflow.com/a/47642650

    Examples
    --------
    >>> find_ranges([2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 20])
    [(2, 5), (12, 17), 20]
    """
    indexable_group: List[int]
    for group in more_itertools.consecutive_groups(iterable):
        indexable_group = list(group)
        yield indexable_group[0], indexable_group[-1]


def find_low_coverage_regions(
    coverage: DataFrame[schemas.SamtoolsCoverage],
    low_coverage_threshold: int = 4,
) -> List[Tuple[int, int]]:
    """Find regions of low coverage in samtools depth result"""
    low_coverage_positions: pd.Series = coverage.loc[
        coverage["DEPTH"] < low_coverage_threshold, "LOC"
    ]
    low_coverage_regions: List[Tuple[int, int]] = list(
        find_ranges(iterable=low_coverage_positions)
    )
    return low_coverage_regions


def update_or_create_sample_coverage(
    db: Session, sample_id: int, sample_bam: str
) -> models.Coverage:
    depth_contents: str = run_samtools_depth(bam_file_path=sample_bam)
    depth: DataFrame[schemas.SamtoolsCoverage] = parse_samtools_depth(
        coverage_contents=depth_contents
    )

    coverage: Optional[models.Coverage] = crud.coverage.get_by(
        db=db, obj_in={"sample_id": sample_id}
    )
    if not coverage:
        return crud.coverage.create(
            db=db,
            obj_in=schemas.CoverageCreate(
                labels=depth.LOC.to_list(), values=depth.DEPTH.to_list()
            ),
            sample_id=sample_id,
        )
    else:
        return crud.coverage.update(
            db=db,
            db_obj=coverage,
            obj_in=schemas.CoverageUpdate(
                labels=depth.LOC.to_list(), values=depth.DEPTH.to_list()
            ),
        )


def update_or_create_sample_consensus(
    db: Session, sample_id: int, sample_bam: str
) -> models.Consensus:
    contents: str = run_samtools_consensus(bam_file_path=sample_bam)
    consensus: Optional[models.Consensus] = crud.consensus.get_by(
        db=db, obj_in={"sample_id": sample_id}
    )
    if not consensus:
        return crud.consensus.create(
            db=db,
            obj_in=schemas.ConsensusCreate(contents=contents),
            sample_id=sample_id,
        )
    else:
        return crud.consensus.update(
            db=db,
            db_obj=consensus,
            obj_in=schemas.ConsensusUpdate(contents=contents),
        )
