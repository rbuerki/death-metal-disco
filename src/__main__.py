from pathlib import Path

from sqlalchemy.exc import ProgrammingError, OperationalError

from src import db_connect
from src import db_functions

CONFIG_PATH = (Path.cwd() / "config.yaml").absolute()


def main():
    engine, session = db_connect.get_engine_and_session()
    print(engine)
    print(session)

    # Always check if Addition is up
    db_functions.add_regular_credits(session)

    # # Export data back-up
    # db_functions.export_db_data_to_2_parquet_files(
    #     session, engine, config_path=CONFIG_PATH
    # )

    session.close()


if __name__ == "__main__":
    main()
