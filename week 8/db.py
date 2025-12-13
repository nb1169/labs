import sqlite3
from pathlib import Path
import pandas as pd

DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)  # create the directory if it doesn't exist, including parent directories

def connect_database(db_path=DB_PATH):   # connect to SQLite database and enable Foreign Keys
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def load_csv_to_table(conn, csv_path: Path, table_name: str):   # loads a CSV file into a database table
    if not csv_path.exists():
        return 0
    try:
        df = pd.read_csv(csv_path)   # reads the csv file into pandas dataframe
        rows_loaded = df.to_sql(name=table_name, con=conn, if_exists='append', index=False)   # appends the data in the csv file into the dataframe
        return rows_loaded
    except Exception:   # incase of any error, return 0 rows loaded
        return 0