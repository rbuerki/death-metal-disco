import yaml
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker


def read_yaml(config_path: Union[str, Path], section: Optional[str]) -> Dict:
    """Return the key-value-pairs from a YAML file, or, if the
    optional `section` parameter is passed, only from a specific
    section of that file.
    """
    with open(config_path, "r") as f:
        yaml_content = yaml.safe_load(f)
    if not section:
        return yaml_content
    else:
        try:
            return yaml_content[section]
        except KeyError:
            print(f"Section {section} not found in config file. Please check.")
            raise


def create_engine(db_params: Dict) -> sqlalchemy.engine.Engine:
    """Create an engine as factory and pool for the DB connections."""
    rel_path = db_params["REL_PATH"]
    full_path = Path.cwd() / rel_path
    conn_str = f"sqlite:///{full_path}"
    engine = sqlalchemy.create_engine(conn_str)
    return engine


def create_session(
    engine: sqlalchemy.engine.Engine,
) -> sqlalchemy.orm.session.Session:
    """Define a Session class bound to the engine and instantiate
    a session object as workspace for all ORM operations.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_scoped_session(
    engine: sqlalchemy.engine.Engine,
) -> sqlalchemy.orm.scoping.scoped_session:
    """Define a tread-save Session class bound to the
    engine. Use it to create a session object as workspace
    for all ORM operations per thread.

    For more infos see here:
    - https://stackoverflow.com/a/18265238/13797028
    - https://stackoverflow.com/a/9621251/13797028

    (I have combined this with Streamlit's advanced caching.
    This is probably a somewhat hacky solution. And I should
    also call Session.remove() when done.)
    """
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    return Session


def get_engine_and_session(
    config_path: Optional[Union[str, Path]] = None,
    section: Optional[str] = None,
) -> Tuple[sqlalchemy.engine.Engine, sqlalchemy.orm.session.Session]:
    """Connect to the DB and return the sqlalchemy engine and
    ORM-session object (not thread save). If no specific config_path or
    section params are passed, the app connects to the PROD DB by default.
    """
    # Set default to standard config file and PROD DB
    config_path = config_path or Path.cwd() / "config.yaml"
    section = section or "DB_PROD"
    # TODO logging where you connect to
    db_params = read_yaml(config_path, section)
    engine = create_engine(db_params)
    session = create_session(engine)
    return engine, session
