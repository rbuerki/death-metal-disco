from pathlib import Path

from sqlalchemy.exc import ProgrammingError, OperationalError

from src import db_connect
from src import db_functions
from src.db_declaration import Base

CONFIG_PATH = (Path.cwd() / "config.yaml").absolute()


def main():
    """This is for manual manipulation only!"""
    engine, session = db_connect.get_engine_and_session()
    print(engine)
    print(session)

    # Always check if Addition is up
    db_functions.add_regular_credits(session)

    # # Export data back-up
    # db_functions.export_db_data_to_2_parquet_files(
    #     session, engine, CONFIG_PATH,
    # )

    # # Reset DB and Import data back-up
    # db_functions.reset_db_with_backup_data(
    #     engine,
    #     session,
    #     Base,
    #     CONFIG_PATH,
    #     "record_data_2021-02-24-15-22-40.parquet",
    #     "trx_data_2021-02-24-15-22-41.parquet",
    # )

    session.close()


if __name__ == "__main__":
    main()
