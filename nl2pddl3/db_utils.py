
# This file contains various utility functions for interacting with the pipeline database.

import os
import sqlite3
import logging
from typing import List, Tuple, Dict, Any

def wipe_db(db_file: str) -> None:
    """Wipe the database by deleting the file if it exists."""
    if os.path.exists(db_file):
        os.remove(db_file)
    logging.warn(f"Database wiped (or did not exist).")

def reset_db(db_file: str) -> sqlite3.Connection:
    """Reset the database by deleting the file if it exists and creating a new one,
    then populating the tables from the up.sql file."""
    wipe_db(db_file)
    conn = create_connection(db_file)
    if conn:
        with open("up.sql", "r") as f:
            sql_script = f.read()
        try:
            cursor = conn.cursor()
            cursor.executescript(sql_script)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return create_connection(db_file)

def create_connection(db_file: str) -> sqlite3.Connection:
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

