import pandas as pd

def get_all_datasets(conn):
    query = "SELECT * FROM datasets_metadata ORDER BY id" # select all rows from the table sort by id
    return pd.read_sql_query(query, conn)