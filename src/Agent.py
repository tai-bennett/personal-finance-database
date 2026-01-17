from .Ingest import Ingest
from .Normalize import Normalize
from .Dedupe import Dedupe
import sqlite3
import pdb

class Agent():
    def __init__(self, config):
        self.db_path = config.db_path
        self.conn = None
        self.cur = None
        self.ingest = Ingest(config)
        self.normalize = Normalize(config)
        self.dedupe = Dedupe(config)

    def run(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        self.ingest.run(cur)
        self.normalize.run(cur)
        self.dedupe.run(cur)
        conn.commit()
        conn.close()
