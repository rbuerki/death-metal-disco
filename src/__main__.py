from sqlalchemy.exc import ProgrammingError, OperationalError

from src import db_connect


def main():
    engine, session = db_connect.main()
    print(engine)
    print(session)
    pass
    session.close()


if __name__ == "__main__":
    main()
