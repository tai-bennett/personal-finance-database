import sqlite3
import uuid
import pdb
from datetime import datetime
from .CategoryManager import CategoryManager

class CategoryRuleManager():
    def __init__(self, config, conn):
        self.config = config
        self.db_path = config.db_path
        self.conn = conn
        self.cur = self.conn.cursor()
        self.cat_manager = CategoryManager(config, self.conn)

    def get_or_create_rule(self, pattern_type, pattern, category, description=""):
        command = """
        SELECT r.rule_id
        FROM category_rules r
        LEFT JOIN categories c ON r.category_id = c.category_id
        WHERE (r.pattern_type, r.pattern, c.category_name) = (?, ?, ?);
        """
        row = self.cur.execute(command, (pattern_type, pattern, category)).fetchone()
        if row:
            return row[0]

        cat_id = self.cat_manager.get_or_create_cat(category)
        ts = datetime.utcnow().isoformat()

        rule_id = str(uuid.uuid4())
        self.cur.execute(
            """
            INSERT INTO category_rules VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (rule_id, pattern_type, pattern, cat_id, 2, ts, description)
            )
        self.conn.commit()
        return rule_id

    def delete_rule(self, pattern_type, pattern, category):
        # command = """
        # DELETE FROM category rules ...
        # """
        pass
