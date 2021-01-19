import yaml
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

import sqlalchemy
from sqlalchemy.orm import sessionmaker


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
    """Define a Session class bound to the engine and
    instantiate a session object as workspace for
    all ORM operations.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def main(
    config_path: Optional[Union[str, Path]] = None,
    section: Optional[str] = None,
) -> Tuple[sqlalchemy.engine.Engine, sqlalchemy.orm.session.Session]:
    """Connect to the DB and return the sqlalchemy engine and
    ORM-session objects. If no specific config_path or section
    params are passed, the app connects to the PROD DB by default.
    """
    # Set default to standard config file an PROD DB
    config_path = config_path or Path.cwd() / "config.yaml"
    section = section or "DB_DEV"

    db_params = read_yaml(config_path, section)
    engine = create_engine(db_params)
    session = create_session(engine)
    return engine, session
