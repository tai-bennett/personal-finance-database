import sqlite3
import pdb
import pandas as pd
from .QueryBuilder import QueryBuilder

class Repository():
    def __init__(self, conn):
        self.conn = conn
        self.query_builder = QueryBuilder()
        self.cur = None

    def get_data(self, filters: dict):
        self.cur = self.conn.cursor()
        command = self.query_builder.basic_build(filters)
        data = self.cur.execute(command).fetchall()
        out = pd.DataFrame(data)
        # pdb.set_trace()
        return out
        
        
