import json
import os
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
        self.update_mode = (config.update_mode == 'new')
        self.conn = None
        self.ts = config.timestamp

    def run(self, conn):
        # self.ts = datetime.utcnow().isoformat()
        self.conn = conn
        self.cur = self.conn.cursor()
        for source_dir in self.raw_dir.iterdir():
            for csv_path in source_dir.glob("*.csv"):
                self.ingest_csv(source_dir.name, csv_path)
        self.conn.commit()

    def ingest_csv(self, source, csv_path):
        fh = file_hash(csv_path)

        # TODO: if csv has already been processed and update_mode == True then return
        file_processed = self._check_raw_files(fh)
        if file_processed & self.update_mode:
            return

        with open(csv_path, newline="", encoding="utf-8") as f:
            # TODO: add csv file and meta data to raw_files table in db
            # add meta data
            size = os.path.getsize(csv_path)
            reader = csv.DictReader(f)
            row_count = 0
            for i, row in enumerate(reader):
                row_count += 1
                self.cur.execute(
                    """
                    INSERT INTO raw_transactions
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(uuid.uuid4()),
                        source,
                        str(csv_path),
                        i,
                        self.ts,
                        fh,
                        json.dumps(row)
                    ),
                )
            self._add_meta_data((fh, str(csv_path), source, size, row_count, self.ts))

    def _add_meta_data(self, row):
        self.cur.execute(
            """
            INSERT INTO raw_files
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            row,
            )

    def _check_raw_files(self, fh):
        # check if raw files has given file hash as key
        command = "SELECT 1 FROM raw_files WHERE file_hash = " + "'" + str(fh) + "'"
        out = self.cur.execute(command).fetchall()
        if len(out) > 0:
            return True
        else:
            return False
