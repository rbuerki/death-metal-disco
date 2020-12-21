import configparser
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple


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
