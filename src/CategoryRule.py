import pdb
import sqlite3

from .CategoryRuleManager import CategoryRuleManager

class CategoryRule():
    def __init__(self, config):
        self.config = config
        self.db_path = config.db_path
        self.conn = None
        self.cur = None
        self.cat_rule_manager = None

    def run(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
        self.cat_rule_manager = CategoryRuleManager(self.config, self.conn)
        self._interactive_add_rule()
        self.conn.commit()
        self.conn.close()

    def _interactive_add_rule(self):
        pt = input("Pattern type is [s]ubstring, [e]xact string or [r]egex?: ")
        if pt == 's':
            pattern_type = 'substring'
        elif pt == 'e':
            pattern_type = 'exact'
        elif pt == 'r':
            pattern_type = 'regex'
        else:
            raise Exception("Invalid pattern type")

        pattern = input("Pattern: ")
        category = input("Category: ")
        desc = input("Description: ")
        self.cat_rule_manager.get_or_create_rule(pattern_type, pattern, category, description=desc)

    def fetch_rules(self):
        # TODO: implement a function that prints rules nicely for app
        pass
