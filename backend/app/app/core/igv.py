import logging
import subprocess

from app.core.config import settings
from app import schemas

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run_igv(batch_file_path: str) -> None:
    igv_command = f"{settings.IGV_PATH} {batch_file_path}"
    logger.debug(
        f"Launching igv command in python subprocess"
        f" with timeout 300s: {igv_command}"
    )
    subprocess.run(igv_command, shell=True, check=True, timeout=5 * 60)
    logger.debug(
        f"igv command in python subprocess finished: {igv_command}"
    )


def prepare_igv_view(
    sample: schemas.Sample, template: schemas.Template
) -> schemas.IGVView:
    return schemas.IGVView(
        fasta_url=template.genome.replace(
            settings.SEQUENCING_DATA_DIR, settings.IGV_SERVER_URL
        ),
        index_url=template.genome.replace(
            settings.SEQUENCING_DATA_DIR, settings.IGV_SERVER_URL
        )
        + ".fai",
        tracks=[
            schemas.IGVTrack(
                type="variant",
                format="vcf",
                name=sample.name,
                url=sample.vcf.replace(
                    settings.SEQUENCING_DATA_DIR, settings.IGV_SERVER_URL
                ),
                indexURL=sample.vcf.replace(
                    settings.SEQUENCING_DATA_DIR, settings.IGV_SERVER_URL
                )
                + ".idx",
            ),
            schemas.IGVTrack(
                type="alignment",
                format="bam",
                name="READS",
                url=sample.bam.replace(
                    settings.SEQUENCING_DATA_DIR, settings.IGV_SERVER_URL
                ),
                indexURL=sample.bam.replace(
                    settings.SEQUENCING_DATA_DIR, settings.IGV_SERVER_URL
                )
                + ".bai",
            ),
            schemas.IGVTrack(
                type="annotation",
                format="gff3",
                name="ANNOTATIONS",
                url=template.gff.replace(
                    settings.SEQUENCING_DATA_DIR, settings.IGV_SERVER_URL
                ),
            ),
        ],
    )
