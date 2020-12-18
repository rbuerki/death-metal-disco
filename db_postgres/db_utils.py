import logging
import psycopg2
import configparser


def _config(filepath="cofig.cfg", section="POSTGRES"):
    """Read a config file and return the parameters 
    of the selected section. (This function is called 
    within `connect`.)
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
