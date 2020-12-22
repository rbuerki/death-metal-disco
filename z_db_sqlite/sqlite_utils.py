import configparser
import logging
import sqlite3
from pathlib import Path
from sqlite3 import Error
from typing import Dict, Optional, Tuple

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


def connect() -> Tuple[Optional[sqlite3.Connection], Optional[sqlite3.Cursor]]:
    """Connect to the SQLite database (file) and return the
    connection. Note: By setting `isolation_level` = None in the
    connec() call, the auto commit mode is activated.
    """
    conn = None
    cur = None
    try:
        db_params = _config()
        path = db_params["path"]
        conn = sqlite3.connect(path, isolation_level=None)
        cur = conn.cursor()
        logging.info("Connecting to SQLite DB successful!")
    except Error as e:
        logging.error(f"Connecting to SQLite DB failed: {e}")

    return conn, cur


def close(conn, cur):
    """Close the connection to the Sqlite DB."""
    try:
        cur.close()
    except (Exception, Error) as e:
        logging.error(e)
    finally:
        if conn is not None:
            conn.close()
            logging.info("DB connection closed.")


def query_execute(query: str, cur: sqlite3.Cursor):
    """Execute the passed query. Note: Be cause we connected
    in auto commit mode, we do not have to commit the query
    explicetly.
    """
    try:
        cur.execute(query)
        # conn.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"Query failed with error: {e}")


def query_read(query: str, cur: sqlite3.Cursor):
    """Return the results of a read query."""
    result = None
    try:
        cur.execute(query)
        result = cur.fetchall()
        return result
    except Error as e:
        print(f"Query failed with error: {e}")
