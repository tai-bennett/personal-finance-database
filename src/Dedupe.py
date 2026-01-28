import sqlite3
import pdb
import hashlib
import json
import uuid
from datetime import datetime
from .CategoryManager import CategoryManager

class Dedupe():
    def __init__(self, config):
        self.db_path = config.db_path
        self.config = config
        self.ts = config['timestamp']
        self.cat_manager = None
        self.conn = None
        self.cur = None

    def run(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.cat_manager = CategoryManager(self.config, self.cur)
        rows = self.cur.execute("SELECT * FROM staging_transactions").fetchall()
        now = self.ts
        for r in rows:
            self.dedupe(r, now)
            if r[10] is not None:
                self.cat_manager.cat_transaction(r[0], r[10])
        self.conn.commit()

    def dedupe(self, row, now):
        fp = self._fingerprint(row)
        self.cur.execute(
            """
            INSERT INTO transactions (
                transaction_id,
                fingerprint,
                account_id,
                transaction_date,
                posted_date,
                description,
                amount,
                currency,
                first_seen,
                last_seen
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(fingerprint)
            DO UPDATE SET last_seen = excluded.last_seen
            """,
            (
                str(uuid.uuid4()),
                fp,
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                now,
                now,
            ),
        )

    def _fingerprint(self, row):
        key = "|".join(
            [
                row[4],                # get transaction date from staging table
                f"{row[7]:.2f}",       # get amount from ... ''
                row[6].lower()         # get description from staging table
            ]
            )
        return hashlib.sha256(key.encode()).hexdigest()
