import json
import pdb
import csv
import sqlite3
import hashlib
import uuid
from datetime import datetime
from pathlib import Path
from .utils import file_hash


class Ingest():
    def __init__(self, config):
        self.db_path = config.db_path
        self.raw_dir = Path(config.raw_dir)

    def run(self, cur):
        for source_dir in self.raw_dir.iterdir():
            for csv_path in source_dir.glob("*.csv"):
                self.ingest_csv(source_dir.name, csv_path, cur)



    def ingest_csv(self, source, csv_path, cur):
        fh = file_hash(csv_path)
        ts = datetime.utcnow().isoformat()

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                cur.execute(
                    """
                    INSERT INTO raw_transactions
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(uuid.uuid4()),
                        source,
                        str(csv_path),
                        i,
                        ts,
                        fh,
                        json.dumps(row)
                    ),
                )
