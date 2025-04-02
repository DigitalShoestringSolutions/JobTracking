from django.core.management.utils import get_random_secret_key
from pathlib import Path

secret_key_file = Path("/app/data/secret_key")

if not secret_key_file.exists():
    with open(secret_key_file, "w") as f:
        f.write(get_random_secret_key())
