import hashlib
import argparse
from .config import *
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT / "data"
DB_ROOT = PROJECT_ROOT / "db"
CONFIG_ROOT = PROJECT_ROOT / "configs"

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()





