import configparser
import logging
import sqlite3
from pathlib import Path
from sqlite3 import Error
from typing import Dict, Optional

CONFIG_PATH = (Path(__file__).parent.parent / "config.cfg").absolute()
SECTION = "SQLITE"


def _config(filepath: Path = CONFIG_PATH, section: str = SECTION) -> Dict:
    """Read a config file and return the parameters of
    the selected section. (This is called within `connect`.)
    """
    config = configparser.ConfigParser()
    try:
        config.read(filepath)
    except FileNotFoundError as e:
        print(f"Please check the path to the config file: {e}")
        raise

    db_params = {}
    if config.has_section(section):
        params = config.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in {filepath}.")

    return db_params


def connect() -> Optional[sqlite3.Connection]:
    """Connect to the SQLite database (file) and return
    the connection.
    """
    conn = None
    try:
        db_params = _config()
        path = db_params["path"]
        conn = sqlite3.connect(path)
        logging.info("Connecting to SQLite DB successful!")
    except Error as e:
        logging.error(f"Connecting to SQLite DB failed: {e}")

    return conn


def close(conn):
    """Close the connection to the Sqlite DB."""
    try:
        conn.close()
    except (Exception, Error) as e:
        logging.error(e)
    finally:
        if conn is not None:
            conn.close()
            logging.info("DB connection closed.")


def execute_query(connection: sqlite3.Connection, query: str):
    """Execute the passed query, after creating a cursor
    from the passed connection.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"Query failed with error: {e}")
