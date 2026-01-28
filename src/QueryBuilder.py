class QueryBuilder():
    def __init__(self):
        pass

    def basic_build(self, filters: dict):
        start = "'" + filters['start_date'] + "'"
        end = "'" + filters['end_date'] + "'"
        command = f"""
        SELECT t.transaction_date, t.description, c.category_name, t.amount
        FROM transactions AS t
        LEFT JOIN transaction_categories tc ON tc.transaction_id = t.transaction_id
        LEFT JOIN categories c ON c.category_id = tc.category_id
        WHERE t.transaction_date BETWEEN {start} AND {end}
        ORDER BY t.transaction_date;
        """
        return command

    def build(self, filters: dict):
        """
        From a dictionary of requirements, build an SQL query that fetches such data
        """
        pass
