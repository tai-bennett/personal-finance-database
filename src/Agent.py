from .Ingest import Ingest

class Agent():
    def __init__(self, config):
        self.ingest = Ingest(config)

    def run(self):
        self.ingest.run()
