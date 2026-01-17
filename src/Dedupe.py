import sqlite3
import hashlib
import json
import uuid
from datetime import datetime

class Dedupe():
    def __init__(self, config):
        self.db_path = config.db_path

    def run(self, cur):
        rows = cur.execute("SELECT * FROM staging_transactions").fetchall()
        now = datetime.utcnow().isoformat()
        for r in rows:
            self.dedupe(r, cur, now)

    def dedupe(self, row, cur, now):
        fp = self._fingerprint(row)
        cur.execute(
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
