#!/usr/bin/env python

from typing import Optional, List, Dict, Tuple
import os
import glob
import base64
import tempfile
import logging

from app import models, schemas, crud
from app.core.bam_features import (
    update_or_create_sample_coverage,
    update_or_create_sample_consensus,
)
from app.core.config import settings
from app.core.igv import run_igv
from app.core.parse_sequencing_stats import (
    find_stats_csv_file,
    parse_stats_file,
)
from app.tests.utils.utils import random_password
from app.core.celery_app import celery_app

from sqlalchemy.orm import Session
from pydantic import BaseModel
from pandera.errors import SchemaError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def find_template_dirs(run_path: str) -> List[str]:
    """Find paths to template directorys for a run"""
    return glob.glob(os.path.join(run_path, "alignment/*"))


def find_bam_files(run_path: str) -> List[str]:
    """Find paths to template directorys for a run"""
    return glob.glob(
        os.path.join(run_path, "alignment/**/*.bam"), recursive=True
    )


def find_template_bam_files(template_path: str) -> List[str]:
    """Find paths to samples bams for a template"""
    return glob.glob(os.path.join(template_path, "*.bam"), recursive=True)


def find_all_bam_files() -> List[str]:
    """Find all bam files in /diva share"""
    return glob.glob(
        os.path.join(settings.SEQUENCING_DATA_DIR, "**/alignment/**/*.bam"),
        recursive=True,
    )


def count_run_samples(db: Session, run: schemas.Run) -> schemas.RunCounts:
    samples_on_disk: int = len(
        find_bam_files(
            run_path=os.path.join(settings.SEQUENCING_DATA_DIR, run.name)
        )
    )
    samples_in_db: int = crud.run.count_samples(db=db, run_id=run.id)
    return schemas.RunCounts(
        id=run.id,
        name=run.name,
        samples_on_disk=samples_on_disk,
        samples_in_db=samples_in_db,
    )


def count_template_samples(
    db: Session, template: schemas.Template
) -> schemas.TemplateCounts:
    template_run: Optional[models.Run] = crud.run.get(
        db=db, id=template.run_id
    )
    if not template_run:
        raise ValueError(f"Could not find run with id = {template.run_id}")
    if not template_run.name:
        raise ValueError(
            f"Run with id = {template.run_id} does not have name"
        )
    samples_on_disk: int = len(
        find_template_bam_files(
            template_path=os.path.join(
                settings.SEQUENCING_DATA_DIR,
                template_run.name,
                "alignment",
                template.name,
            )
        )
    )
    samples_in_db: int = crud.template.count_samples(
        db=db, template_id=template.id
    )
    return schemas.TemplateCounts(
        samples_on_disk=samples_on_disk,
        samples_in_db=samples_in_db,
        **template.dict(),
    )


class SnapshotInput(BaseModel):
    """Snapshot info for a given sample"""

    template_name: str
    sample_name: str
    jbx_path: str
    bam_path: str
    vcf_path: str
    gff_path: str
    snapshot_path: str

    def create_snapshot_instructions(self) -> str:
        """Create IGV snapshot instructions for a given sample"""
        instructions: str = "new" + "\n"
        instructions += f"genome {self.jbx_path}" + "\n"
        instructions += f"load {self.vcf_path}" + "\n"
        instructions += f"load {self.bam_path}" + "\n"
        instructions += f"load {self.gff_path}" + "\n"
        instructions += f"snapshot {self.snapshot_path}" + "\n"
        return instructions

    def read_snapshot(self) -> bytes:
        with open(self.snapshot_path, "rb") as image_file:
            b64_encoded_img: bytes = base64.b64encode(image_file.read())
        return b64_encoded_img


def create_igv_instructions(
    snapshot_inputs: List[SnapshotInput],
) -> str:
    """Create IGV batch file instruction contents"""
    batch_file: str = ""
    for snapshot_input in snapshot_inputs:
        batch_file += snapshot_input.create_snapshot_instructions() + "\n"
    batch_file += "exit\n"
    return batch_file


def create_snapshot_inputs(
    template_path: str, temp_dir_path: str
) -> List[SnapshotInput]:
    """Identify file paths for each sample data file"""
    sample_snapshot_inputs: List[SnapshotInput] = []
    template_name: str = os.path.basename(template_path)
    bam_paths: List[str] = glob.glob(os.path.join(template_path, "*.bam"))
    vcf_paths: List[str] = glob.glob(os.path.join(template_path, "*.vcf"))
    sample_name: str
    snapshot_name: str
    for bam_path, vcf_path in zip(bam_paths, vcf_paths):
        sample_name = os.path.basename(bam_path).replace("_R1R2.bam", "")
        snapshot_name = f"{template_name}_{sample_name}.png"
        sample_snapshot_inputs.append(
            SnapshotInput(
                template_name=template_name,
                sample_name=sample_name,
                jbx_path=os.path.join(
                    template_path, template_name + ".fa"
                ),
                bam_path=bam_path,
                vcf_path=vcf_path,
                gff_path=os.path.join(
                    template_path, template_name + ".gff3"
                ),
                snapshot_path=os.path.join(temp_dir_path, snapshot_name),
            )
        )
    return sample_snapshot_inputs


def create_sample_snapshots_for_template(
    template_path: str, temp_dir_path: str
) -> Tuple[List[SnapshotInput], str]:
    """Run IGV locally to take snapshots of each sample"""
    snapshot_inputs: List[SnapshotInput] = create_snapshot_inputs(
        template_path=template_path, temp_dir_path=temp_dir_path
    )
    igv_batch_instructions: str = create_igv_instructions(
        snapshot_inputs=snapshot_inputs
    )
    igv_batch_path: str = os.path.join(temp_dir_path, "igv_batch.txt")
    with open(igv_batch_path, "w") as F:
        F.write(igv_batch_instructions)
    return snapshot_inputs, igv_batch_path


def find_or_create_sample_owner(
    db: Session, sample_name: str
) -> models.User:
    """Identify owner of sample by filename

    Notes: Expect sample name to be in format {email}-*
    """
    owner_email: str = (sample_name.split("-")[0] + settings.INSTITUTION_SUFFIX).lower()
    owner: Optional[models.User] = crud.user.get_by(
        db=db, obj_in={"email": owner_email}
    )
    if owner:
        return owner
    else:
        user_create: schemas.UserCreate = schemas.UserCreate(
            email=owner_email,
            password=random_password(),
            is_active=False,
        )
        user: models.User = crud.user.create(db=db, obj_in=user_create)
        logger.debug(f"Created new user: {owner_email}")
        if settings.EMAILS_ENABLED and settings.SSGUI_APPROVAL_CONTACT:
            celery_app.send_task(
                "app.worker.celery_send_email",
                kwargs={
                    "email_to": settings.SSGUI_APPROVAL_CONTACT,
                    "subject_template": (
                        "SSGUI - New User Automatically "
                        "Created Notification"
                    ),
                    "html_template": (
                        f"Created new user: {owner_email}. User must be "
                        'activated from "Manage Users" page.'
                    ),
                },
            )
        else:
            logger.debug(
                f"Tried to send email notification to "
                f"{settings.SSGUI_APPROVAL_CONTACT} but emails not enabled"
            )
        return user


def find_or_create_template(
    db: Session,
    template_name: str,
    run_id: int,
    gff_path: str,
    jbx_path: str,
    template_stats: schemas.TemplateStats,
) -> models.Template:
    """Identify template in db or create one"""
    existing_template: Optional[models.Template] = crud.template.get_by(
        db=db,
        obj_in={
            "run_id": run_id,
            "name": template_name,
        },
    )
    if existing_template:
        return existing_template
    else:
        return crud.template.create(
            db=db,
            obj_in=schemas.TemplateCreate(
                name=template_name,
                gff=gff_path,
                genome=jbx_path,
                **template_stats.dict(),
            ),
            run_id=run_id,
        )


def find_or_create_sample(
    db: Session,
    snapshot: SnapshotInput,
    sample_stats: schemas.SampleStats,
    user_id: int,
    template_id: int,
) -> models.Sample:
    """Identify sample in db or create one"""
    existing_sample: Optional[models.Sample] = crud.sample.get_by(
        db=db,
        obj_in={
            "template_id": template_id,
            "user_id": user_id,
            "name": snapshot.sample_name,
        },
    )
    if existing_sample:
        return existing_sample
    else:
        return crud.sample.create(
            db=db,
            obj_in=schemas.SampleCreate(
                name=snapshot.sample_name,
                bam=snapshot.bam_path,
                vcf=snapshot.vcf_path,
                snapshot=snapshot.read_snapshot(),
                **sample_stats.dict(),
            ),
            user_id=user_id,
            template_id=template_id,
        )


def parse_divaseq_template(
    db: Session, run_id: int, template_path: str, stats_path: str
) -> Optional[models.Template]:
    template_name: str = os.path.basename(template_path)
    logger.debug(f"Looking at {template_name}")

    # Check if template already loaded in database
    potential_template: Optional[models.Template] = crud.template.get_by(
        db=db, obj_in={"name": template_name, "run_id": run_id}
    )
    if potential_template:
        template_counts: schemas.TemplateCounts = count_template_samples(
            db=db,
            template=schemas.Template.from_orm(potential_template),
        )
        if template_counts.samples_on_disk_match_db:
            logger.debug(
                f"{template_name} is already correctly loaded in database"
            )
            return None
        else:
            logger.debug(
                f"{template_name} in database but not correctly loaded"
            )
    else:
        logger.debug(f"{template_name} not in database")

    # Parse stats file
    all_template_stats: Dict[str, schemas.TemplateStats]
    all_sample_stats: Dict[str, schemas.SampleStats]
    all_template_stats, all_sample_stats = parse_stats_file(
        stats_path=stats_path
    )

    # Gather screenshots for each sample in template
    template: models.Template
    with tempfile.TemporaryDirectory() as temp_dir:
        snapshot_inputs: List[SnapshotInput]
        igv_batch_path: str
        (
            snapshot_inputs,
            igv_batch_path,
        ) = create_sample_snapshots_for_template(
            template_path=template_path, temp_dir_path=temp_dir
        )
        if not snapshot_inputs:
            raise IndexError(
                f"No samples found for template: {template_name}"
            )
        run_igv(batch_file_path=igv_batch_path)

        # Add template to database
        template = find_or_create_template(
            db=db,
            template_name=template_name,
            run_id=run_id,
            gff_path=snapshot_inputs[0].gff_path,
            jbx_path=snapshot_inputs[0].jbx_path,
            template_stats=all_template_stats[template_name],
        )

        # Add each sample to database
        for snapshot in snapshot_inputs:
            owner: models.User = find_or_create_sample_owner(
                db=db, sample_name=snapshot.sample_name
            )
            sample: models.Sample = find_or_create_sample(
                db=db,
                snapshot=snapshot,
                sample_stats=all_sample_stats[snapshot.sample_name],
                user_id=owner.id,
                template_id=template.id,
            )
            update_or_create_sample_coverage(
                db=db,
                sample_id=sample.id,
                sample_bam=sample.bam if sample.bam else "",
            )
            update_or_create_sample_consensus(
                db=db,
                sample_id=sample.id,
                sample_bam=sample.bam if sample.bam else "",
            )
    return template


def parse_divaseq_run(db: Session, run_path: str) -> Optional[models.Run]:
    """Parse data in divaseq run into database"""
    run_name: str = os.path.basename(run_path)
    logger.debug(f"Looking at {run_name}")

    # Check if run is already loaded in database
    potential_run: Optional[models.Run] = crud.run.get_by(
        db=db, obj_in={"name": run_name}
    )
    if potential_run:
        run_counts: schemas.RunCounts = count_run_samples(
            db=db, run=schemas.Run.from_orm(potential_run)
        )
        if run_counts.samples_on_disk_match_db:
            logger.debug(
                f"{run_name} is already correctly loaded in database"
            )
            return None
        else:
            logger.debug(
                f"{run_name} in database but not correctly loaded"
            )
    else:
        logger.debug(f"{run_name} not in database")

    # Check if run contains stats csv file
    stats_path: Optional[str] = find_stats_csv_file(run_path=run_path)
    if not stats_path:
        logger.debug(f"{run_name} is not a valid run because no stats csv")
        return None

    # Check if stats csv file is properly formatted
    try:
        parse_stats_file(stats_path=stats_path)
    except SchemaError as e:
        logger.debug(
            f"{run_name} contains invalid stats {stats_path}: {e}"
        )
        return None

    # Add run to database
    run: models.Run
    if potential_run:
        run = potential_run
    else:
        run = crud.run.create(
            db=db, obj_in=schemas.RunCreate(name=run_name)
        )

    # Queue adding run's templates to database
    template_paths: List[str] = find_template_dirs(run_path=run_path)
    for template_path in template_paths:
        celery_app.send_task(
            "app.worker.celery_add_template_to_database",
            kwargs={
                "run_id": run.id,
                "template_path": template_path,
                "stats_path": stats_path,
            },
        )
    return run
