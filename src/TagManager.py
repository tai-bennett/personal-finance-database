import sqlite3
import uuid
import pdb
from datetime import datetime


class TagManager():
    def __init__(self, config):
        self.db_path = config.db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def get_or_create_tag(self, name, description=None):
        command = "SELECT tag_id FROM tags WHERE tag_name = ?"
        row = self.cur.execute(command, (name,)).fetchone()
        if row:
            return row[0]

        tag_id = str(uuid.uuid4())
        self.cur.execute(
            """
            INSERT INTO tags VALUES (?, ?, ?)

            """,
            (tag_id, name, description)
            )
        self.conn.commit()
        return tag_id

    def tag_transaction(self, transaction_id, tag_name):
        tag_id = self.get_or_create_tag(tag_name)
        tagged_id = str(uuid.uuid4())

        command = """
        INSERT INTO transaction_tags (
            tagged_id,
            transaction_id,
            tag_id,
            created_at
        ) 
        VALUES (?, ?, ?, ?)

        """
        self.cur.execute(command,
                         (tagged_id,
                          transaction_id,
                          tag_id,
                          datetime.utcnow().isoformat()))

        self.conn.commit()


