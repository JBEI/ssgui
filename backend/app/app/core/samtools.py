import io
import logging
import subprocess

import pandas as pd
from pandera.typing import DataFrame

from app import schemas
from app.core.config import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run_samtools_depth(bam_file_path: str) -> str:
    samtools_command = f"{settings.SAMTOOLS_PATH} depth -a {bam_file_path}"
    logger.debug(
        f"Launching samtools depth command in python subprocess"
        f" with timeout 300s: {samtools_command}"
    )
    samtools_process: subprocess.CompletedProcess = subprocess.run(
        samtools_command,
        shell=True,
        check=True,
        timeout=5 * 60,
        capture_output=True,
        encoding="utf-8",
    )
    logger.debug(
        f"samtools command in python subprocess "
        f"finished: {samtools_command}"
    )
    samtools_process.check_returncode()
    return samtools_process.stdout


def parse_samtools_depth(
    coverage_contents: str,
) -> DataFrame[schemas.SamtoolsCoverage]:
    return schemas.SamtoolsCoverage.validate(
        pd.read_csv(
            io.StringIO(coverage_contents),
            header=None,
            sep="\t",
            names=["CHROM", "LOC", "DEPTH"],
        )
    )


def run_samtools_consensus(bam_file_path: str) -> str:
    samtools_command = (
        f"{settings.SAMTOOLS_PATH} consensus {bam_file_path}"
    )
    logger.debug(
        f"Launching samtools consensus command in python subprocess"
        f" with timeout 300s: {samtools_command}"
    )
    samtools_process: subprocess.CompletedProcess = subprocess.run(
        samtools_command,
        shell=True,
        check=True,
        timeout=5 * 60,
        capture_output=True,
        encoding="utf-8",
    )
    logger.debug(
        f"samtools command in python subprocess "
        f"finished: {samtools_command}"
    )
    samtools_process.check_returncode()
    return samtools_process.stdout
