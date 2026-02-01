from .Ingest import Ingest
from .Normalize import Normalize
from .Dedupe import Dedupe
from .Categorize import Categorize
from datetime import datetime
import sqlite3
import pdb

class Agent():
    def __init__(self, config):
        ts = datetime.utcnow().isoformat()
        self.config = config
        self.config['timestamp'] = ts
        self.db_path = config.db_path
        self.conn = None
        self.cur = None
        self.ingest = Ingest(self.config)
        self.normalize = Normalize(self.config)
        self.dedupe = Dedupe(self.config)
        self.cat = Categorize(self.config)

    def run(self):
        self.conn = sqlite3.connect(self.db_path)
        self.ingest.run(self.conn)
        self.normalize.run(self.conn)
        self.dedupe.run(self.conn)
        self.cat.run(self.conn)
        self.conn.close()
