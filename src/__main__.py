from sqlalchemy.exc import ProgrammingError, OperationalError

from src import db_connect
from src import db_functions


def main():
    engine, session = db_connect.main()
    print(engine)
    print(session)

    # Always check if Addition is up
    db_functions.add_regular_credits(session)
    session.close()


if __name__ == "__main__":
    main()
