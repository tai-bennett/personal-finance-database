import sqlite3
import json
import uuid
from datetime import datetime


class Normalize():
    def __init__(self, config):
        self.db_path = config.db_path
        self.ts = config.timestamp
        self.update_mode = True

    def run(self, cur):
        command = "SELECT raw_id, source_bank, raw_payload, ingestion_ts FROM raw_transactions"
        if self.update_mode:
            command = command + " WHERE ingestion_ts = '" + str(self.ts) + "'"

        rows = cur.execute(command).fetchall()

        for raw_id, source, raw_payload, ts in rows:
            payload = json.loads(raw_payload)

            try:
                t_date, p_date, desc, amt = self.normalize_row(source, payload)
            except Exception:
                continue

            cur.execute(
                """
                INSERT OR IGNORE INTO staging_transactions
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid.uuid4()),
                    raw_id,
                    source,
                    None,
                    t_date,
                    p_date,
                    desc,
                    amt,
                    'USD',
                    ts,
                ),
                )

    def normalize_row(self, source, payload):
        if source == 'us_bank_1':
            return (
                payload['Date'],
                None,
                payload['Name'],
                payload['Amount']
                )
        if source == 'chase_credit_card':
            return (
                payload['Transaction Date'],
                payload['Post Date'],
                payload['Description'],
                payload['Amount']
                )
        raise ValueError(f"While normalizing, unknown source {source} was used.")
        
