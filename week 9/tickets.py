import pandas as pd

def get_all_tickets(conn):
    query = "SELECT * FROM it_tickets ORDER BY id DESC" # select all rows from the it tickets table and order by id 
    return pd.read_sql_query(query, conn)