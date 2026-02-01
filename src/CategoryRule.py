import pdb
import sqlite3

from .CategoryRuleManager import CategoryRuleManager
from .config import *


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

    def add_rule_from_json(self, path):
        pdb.set_trace()
        rules, _ = get_config_from_json(path)
        rules = rules.category
        for rule in rules.values():
            self.cat_rule_manager.get_or_create_rule(
                rule['type'],
                rule['pattern'],
                rule['category'],
                description=rule['description']
            )


    def _interactive_add_rule(self):
        option = input("Get rules from json? (Y/n): ")
        if option == "Y":
            path = input("Path to json: ")
            self.add_rule_from_json(path)
        else:
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
            self.cat_rule_manager.get_or_create_rule(pattern_type, pattern, category, source='manual', description=desc)

    def fetch_rules(self):
        # TODO: implement a function that prints rules nicely for app
        pass
