import pdb
import os

from .Agent import Agent
from .Tagger import Tagger
from .Categorize import Categorize
from .CategoryRule import CategoryRule

class App():
    def __init__(self, config):
        self.config = config
        self.agent = Agent(config)
        config = self.agent.config      # this is a super hacky fix for timestamp
        self.tagger = Tagger(config)
        self.categorize = Categorize(config)
        self.cat_rule = CategoryRule(config)
        

    def run(self):
        print("|" + "=" * 40 + "|")
        print("-"*12 + "WELCOME TO THE API" + "-"*12)
        print("|" + "=" * 40 + "|")
        self.menu()

    def menu(self):
        while True:
            print("\n")
            print("|" + "=" * 40 + "|")
            print("Select options ... \n [t]agger \n [c]ategorize \n [r]un update  \n c[a]tegory rules \n [q]uit \n")
            choice = input("Option: ")
            if choice == 't':
                self._tagger_loop()
                break
            if choice == 'c':
                self._cat_loop()
                break
            if choice == 'r':
                self._agent_loop()
                break
            if choice == 'a':
                self._cat_rule_loop()
                break
            if choice == 'reset':
                self._reset_db()
                break
            if choice == 'q':
                print("quitting...\n")
                break
            else:
                print("Invalid option...\n")

    def _tagger_loop(self):
        while True:
            start = input("Start date: ")
            end = input("End date: ")
            self.tagger.run(start, end)
            choice = input("[c]ontinue tagging or [q]uit: ")
            if choice == 'q':
                break

    def _cat_loop(self):
        while True:
            start = input("Start date: ")
            end = input("End date: ")
            self.categorize.manual_cat(start, end)
            choice = input("[c]ontinue categorizing or [q]uit: ")
            if choice == 'q':
                break

    def _cat_rule_loop(self):
        while True:
            self.cat_rule.run()
            choice = input("[c]ontinue creating rules or [q]uit: ")
            if choice == 'q':
                break

    def _agent_loop(self):
        while True:
            mode = input("[R]un all or only [n]ew files?: ")
            if mode == 'R':
                self.agent.config['mode'] = 'all'
            elif mode == 'n':
                self.agent.config['mode'] = 'new'
            else:
                print('running config default mode')
            self.agent.run()
            choice = input("[c]ontinue or [q]uit: ")
            if choice == 'q':
                break

    def _reset_db(self):
        command = "rm -f " + self.config.db_path
        print("removing database ...")
        os.system(command)

        command = "sqlite3 " + self.config.db_path + " < " + self.config.schema_path
        print("initiating database ...")
        os.system(command)

        print("repopulating database ...")
        self.agent.run()


