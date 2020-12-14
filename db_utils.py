import logging
import psycopg2
from configparser import ConfigParser


def _config(filename="cofig.cfg", section="POSTGRES"):
    """Return necessary parameters for connecting to the database.
    (This function is called within `connect`.)
    """
    parser = ConfigParser()
    parser.read(filename)

    db_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in {filename}.")

    return db_params


def connect():
    """Connect to the PostgreSQL database server. 
    Return cursor and connection.
    """
    conn = None
    try:
        db_params = _config()
        logging.info("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**db_params)
        # Set auto commit so that each action is commited without calling conn.commit()
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        logging.info("Success!")

        return cur, conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def close(cur, conn):
    """Close the communication with the PostgreSQL database."""
    try:
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            logging.info("Database connection closed.")
