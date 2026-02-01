import pdb
from .Repository import Repository
from datetime import date
import calendar

class DashboardService():
    def __init__(self, conn):
        self.repo = Repository(conn)

    def filtered_transactions(self, filters: dict):
        return self.repo.get_data(filters)

    def get_this_month(self):
        today = date.today()
        filters = {'start_date': None, 'end_date': None}
        filters['start_date'] = today.replace(day=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        filters['end_date'] = today.replace(day=last_day)

        return self.filtered_transactions(filters)

    def get_test_df(self):
        filters = {'start_date': None, 'end_date': None}
        filters['start_date'] = "2025-10-01"
        filters['end_date'] = "2025-10-31"

        return self.filtered_transactions(filters)

    def get_aggregate(self):
        filters = {'start_date': None, 'end_date': None}
        filters['start_date'] = "2025-10-01"
        filters['end_date'] = "2025-10-31"

        return self.repo.get_aggregate(filters)
