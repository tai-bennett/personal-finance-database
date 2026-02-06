import sqlite3
import pdb
import json
import uuid
from datetime import datetime


class Normalize():
    def __init__(self, config):
        self.config = config
        self.db_path = config.db_path
        self.ts = config.timestamp
        self.update_mode = (config.update_mode == 'new')
        self.conn = None
        self.cur = None

    def run(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        command = "SELECT raw_id, source_bank, raw_payload, ingestion_ts FROM raw_transactions"
        if self.update_mode:
            command = command + " WHERE ingestion_ts = '" + str(self.ts) + "'"

        rows = self.cur.execute(command).fetchall()

        for raw_id, source, raw_payload, ts in rows:
            payload = json.loads(raw_payload)

            try:
                t_date, p_date, desc, amt, cat = self.normalize_row(source, payload)
            except Exception:
                continue

            self.cur.execute(
                """
                INSERT OR IGNORE INTO staging_transactions
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    cat
                ),
                )
        self.conn.commit()

    def normalize_row(self, source, payload):
        source_name = self.config.normalization[source]

        if source_name == 'boa':
            return (
                payload['Date'],
                None,
                payload['Name'],
                payload['Amount'],
                None
                )
        elif source_name == 'chase':
            t_date = payload['Transaction Date']
            p_date = payload['Post Date']
            t_date = datetime.strptime(t_date, "%m/%d/%Y").date().isoformat()
            p_date = datetime.strptime(p_date, "%m/%d/%Y").date().isoformat()
            return (
                t_date,
                p_date,
                payload['Description'],
                payload['Amount'],
                payload['Category']
                )
        else:
            raise ValueError(f"While normalizing, unknown source {source} was used.")
        
