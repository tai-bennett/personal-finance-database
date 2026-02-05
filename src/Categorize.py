import hashlib
import pdb
import sqlite3
import json
import uuid
from .CategoryManager import CategoryManager
from .config import *
from .utils import CONFIG_ROOT


class Categorize():
    def __init__(self, config):
        self.config = config
        self.db_path = config.db_path
        self.ts = config['timestamp']
        self.update_mode = (config.update_mode == 'new')
        self.cat_manager = None
        self.conn = None
        self.cur = None

    def run(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.cat_by_rule()

    # def cat_by_source(self, cur):
    #     command = "SELECT * FROM staging_transactions WHERE category NOT NULL"
    #     if self.update_mode:
    #         command = command + " AND ingestion_ts = '" + str(self.ts) + "'"
    #     pdb.set_trace()

    #     rows = cur.execute(command).fetchall()

    #     for r in rows:
    #         self.cat_manager.cat_transactions()
    #         

    def cat_by_rule(self):
        # categorize using category_rules table for all or new rows in transactions
        # get transactions tables
        self.cat_manager = CategoryManager(self.config, self.conn)
        command = "SELECT * FROM transactions"
        if self.update_mode:
            command = command + " WHERE ingestion_ts = '" + str(self.ts) + "'"

        rows = self.cur.execute(command).fetchall()
        rules = self._get_rules()

        for row in rows:
            self._categorize_row(row, rules)

    def _get_rules(self):
        # command = "SELECT * FROM category_rules"
        # rules = self.cur.execute(command).fetchall()
        path = CONFIG_ROOT / self.config.cat_rules
        rules, _ = get_config_from_json(str(path))
        rules = rules.category
        return rules
        

    def _categorize_row(self, row, rules):
        # for rule in rules:
        #     self._apply_rule(row, rule)
        for rule in rules.values():
            self._apply_rule(row, rule)

    def _apply_rule(self, row, rule):
        cat = self._apply_rule_to_row(row, rule)
        self._set_cat_to_row(row, cat)

    def _apply_rule_to_row(self, row, rule):
        if rule['type'] == 'substring':
            # pdb.set_trace()
            if rule['pattern'].lower() in row[5].lower():  # the description column is r[5]
                return rule['category']
            else:
                return None

    def _set_cat_to_row(self, row, cat):
        if cat is None:
            return
        else:
            self.cat_manager.cat_transaction(
                row[5],
                cat,
                priority=2,
                method='json'
                )
                

    def manual_cat(self, start, end):
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
        self.cat_manager = CategoryManager(self.config, self.conn)
        rows = self.fetch_transactions(start, end)
        self.interactive_cat_loop(rows)
        self.conn.commit()
        self.conn.close

    def interactive_cat_loop(self, rows):
        for r in rows:
            print("|" + "="*40 + "|")
            print(f"Date: {r[1]}")
            print(f"Amount: {r[3]:.2f}")
            print(f"Category: {r[4] or '-'}")
            print(f"Description: {r[2]}")

            print(f"ID: {r[0]}")
            choice = input("Add tag: [y]es/ [n]o / [q]uit: ").strip().lower()

            if choice == "q":
                break
            if choice != "y":
                continue

            cat = input("Enter cat name: ").strip()
            self.cat_manager.cat_transaction(r[0], cat, priority=1, method="manual")

    def fetch_transactions(self, start, end):
        start = "'" + start + "'"
        end = "'" + end + "'"
        command = f"""
        SELECT t.transaction_id, t.transaction_date, t.description, t.amount, c.category_name
        FROM transactions AS t
        LEFT JOIN transaction_categories tc USING (transaction_id)
        LEFT JOIN categories c ON c.category_id = tc.category_id
        WHERE t.transaction_date BETWEEN {start} AND {end}
        GROUP BY t.transaction_id
        ORDER BY t.transaction_date
        """
        return self.cur.execute(command).fetchall()
