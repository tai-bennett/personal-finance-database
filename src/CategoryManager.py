import sqlite3
import uuid
import pdb
from datetime import datetime


class CategoryManager():
    def __init__(self, config, conn):
        self.db_path = config.db_path
        self.conn = conn
        self.cur = self.conn.cursor()

    # def close_connection(self):
    #     self.conn.close()

    def get_or_create_cat(self, name, description=None):
        command = "SELECT category_id FROM categories WHERE category_name = ?"
        row = self.cur.execute(command, (name,)).fetchone()
        if row:
            return row[0]

        cat_id = str(uuid.uuid4())
        self.cur.execute(
            """
            INSERT INTO categories VALUES (?, ?, ?)

            """,
            (cat_id, name, description)
            )
        self.conn.commit()
        return cat_id

    def cat_transaction(self, transaction_id, cat_name, priority=3, method='bank'):
        cat_id = self.get_or_create_cat(cat_name)
        categorization_id = str(uuid.uuid4())

        command = """
        INSERT INTO transaction_categories (
            categorization_id,
            transaction_id,
            category_id,
            created_at,
            priority,
            method
        ) 
        VALUES (?, ?, ?, ?, ?, ?)

        """
        self.cur.execute(command,
                         (categorization_id,
                          transaction_id,
                          cat_id,
                          datetime.utcnow().isoformat(),
                          priority,
                          method
                          ))

        self.conn.commit()



