import sqlite3
import pdb

from .TagManager import TagManager

class Tagger():
    def __init__(self, config):
        self.db_path = config.db_path
        self.conn = None
        self.cur = None
        self.rows = None
        self.tag_manager = TagManager(config)

    def run(self, start, end):
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
        rows = self.fetch_transactions(start, end)
        self.interactive_tag_loop(rows)
        self.conn.commit()
        self.conn.close()

    def fetch_transactions(self, start, end):
        start = "'" + start + "'"
        end = "'" + end + "'"
        command = f"""
        SELECT t.transaction_id, t.transaction_date, t.description, t.amount, GROUP_CONCAT(tags.tag_name) AS tag_set
        FROM transactions AS t
        LEFT JOIN transaction_tags tt USING (transaction_id)
        LEFT JOIN tags ON tags.tag_id = tt.tag_id
        WHERE t.transaction_date BETWEEN {start} AND {end}
        GROUP BY t.transaction_id
        ORDER BY t.transaction_date
        """
        return self.cur.execute(command).fetchall()

    def interactive_tag_loop(self, rows):
        for r in rows:
            print("|" + "="*40 + "|")
            print(f"Date: {r[1]}")
            print(f"Amount: {r[3]:.2f}")
            print(f"Tags: {r[4] or '-'}")
            print(f"Description: {r[2]}")

            choice = input("Add tag: [y]es/ [n]o / [q]uit: ").strip().lower()

            if choice == "q":
                break
            if choice != "y":
                continue

            tag = input("Enter tag name: ").strip()
            self.tag_manager.tag_transaction(r[0], tag)

