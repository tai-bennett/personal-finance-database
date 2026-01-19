import hashlib
import json
import uuid


class Categorize():
    def __init__(self, config):
        self.db_path = config.db_path
        self.ts = config['timestamp']
        self.update_mode = True

    def run(self, cur):
        # categorize using category_rules table for all or new rows in transactions
        # get transactions tables
        command = "SELECT * FROM transactions"
        if self.update_mode:
            command = command + " WHERE ingestion_ts = '" + str(self.ts) + "'"

        rows = cur.execute(command).fetchall()

        command = "SELECT * FROM category_rules"
        rules = cur.execute(command).fetchall()

        for row in rows:
            self._categorize_row(row, rules)

    def _categorize_row(self, row, rules):
        for rule in rules:
            self._apply_rule(row, rule)

    def _apply_rule(self, row, rule):
        pass
