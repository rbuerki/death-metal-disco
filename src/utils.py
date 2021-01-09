import configparser
from pathlib import Path
from typing import Dict, Union

import sqlalchemy
from sqlalchemy.orm import sessionmaker


def read_config_return_dict(filepath: Path, section: str) -> Dict:
    """Read a config file section and return a dict of
    key value pairs for all the parameters in it.
    """
    config = configparser.ConfigParser()
    if not Path(filepath).is_file():
        raise FileNotFoundError(
            f"Config file not found. Please check the path "
            f"to the config file: {filepath}"
        )
    else:
        config.read(filepath)
        db_params = {}
        if config.has_section(section):
            params = config.items(section)
            for param in params:
                db_params[param[0]] = param[1]
        else:
            raise ValueError(f"Section {section} not found in {filepath}.")

        return db_params


def read_config_return_str(filepath: Path, section: str) -> str:
    """Read a config file section with one parameter and
    return a string. Will raise an exception if more than
    one parameter is found in the section.
    """
    config = configparser.ConfigParser()
    if not Path(filepath).is_file():
        raise FileNotFoundError(
            f"Config file not found. Please check the path "
            f"to the config file: {filepath}"
        )
    else:
        config.read(filepath)
        if config.has_section(section):
            params = config.items(section)
            if len(params) > 1:
                raise ValueError(
                    f"Section {section} has more than one parameter."
                )
            db_param = params[0][1]
        else:
            raise ValueError(f"Section {section} not found in {filepath}.")

        return db_param


def create_engine(rel_path: Union[Path, str]) -> sqlalchemy.engine.Engine:
    """Create an engine as factory and pool forthe DB connections."""
    full_path = Path.cwd() / rel_path
    print(full_path)
    conn_str = f"sqlite:///{full_path}"
    engine = sqlalchemy.create_engine(conn_str)
    return engine


def create_session(
    engine: sqlalchemy.engine.Engine,
) -> sqlalchemy.orm.session.Session:
    """Define a Session class bound to the engine and
    instantiate a session object as workspace for
    all ORM operations.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_DB_anew(
    engine: sqlalchemy.engine.Engine,
    Base,  #: sqlalchemy.ext.declarative.api.DeclarativeMeta],
):
    """Drop all existing tables from the database
    and create them anew.
    """
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine)
