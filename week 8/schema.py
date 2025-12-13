def create_users_table(conn):       # create the user authentication table
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
    """)
    conn.commit()


def create_cyber_incidents_table(conn):   # creates the cyber incidents table
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id TEXT NOT NULL UNIQUE, 
        timestamp TEXT, 
        severity TEXT, 
        category TEXT, 
        status TEXT, 
        description TEXT
    )
    """)
    conn.commit()


def create_datasets_metadata_table(conn):    # create the datasets metadata table
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id TEXT NOT NULL UNIQUE,
        name TEXT,
        rows INTEGER,
        columns INTEGER,
        uploaded_by TEXT,
        upload_date TEXT
    )
    """)
    conn.commit()


def create_it_tickets_table(conn):    # create the IT tickets table
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL, 
        priority TEXT, 
        description TEXT, 
        status TEXT, 
        assigned_to TEXT, 
        created_at TEXT, 
        resolution_time_hours REAL
    )
    """)
    conn.commit()


def create_all_tables(conn):      # Runs all table creation functions
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)