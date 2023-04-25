import random
import string
from typing import Dict
import os

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_password() -> str:
    return (
        "".join(random.choices(string.ascii_uppercase, k=12))
        + "".join(random.choices(string.ascii_lowercase, k=12))
        + "".join(random.choices(string.digits, k=12))
        + "".join(random.choices(string.punctuation, k=12))
    )


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_int() -> int:
    return random.randint(1, 100000)


def random_run_path() -> str:
    return os.path.join(settings.SEQUENCING_DATA_DIR, random_lower_string())


def random_template_path() -> str:
    return os.path.join(
        random_run_path(), "alignment", random_lower_string()
    )


def random_gff_path(random_template_path: str) -> str:
    return os.path.join(
        random_template_path,
        os.path.basename(random_template_path) + ".gff3",
    )


def random_genome_path(random_template_path: str) -> str:
    return os.path.join(
        random_template_path,
        os.path.basename(random_template_path) + ".fa",
    )


def random_bam_path(
    random_template_path: str, username: str, sample_name: str
) -> str:
    return os.path.join(
        random_template_path,
        f"{username}-{sample_name}.bam",
    )


def random_vcf_path(
    random_template_path: str, username: str, sample_name: str
) -> str:
    return os.path.join(
        random_template_path,
        f"{username}-{sample_name}.vcf",
    )


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data
    )
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
