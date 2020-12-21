import sys
from pathlib import Path

# import numpy as np
# import pandas as pd
import pytest


sys.path.append(str(Path.cwd().parent / "src"))
# sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")


@pytest.fixture(scope="module")
def path_to_config():
    return Path.cwd() / "tests/data/config_test.cfg"


# @pytest.fixture(scope="module")
# def mock_dataframe_1():
#     mock_df = pd.read_csv(
#         "mock_data.csv",
#         sep=";",
#         engine="python",
#         parse_dates=["calculation_date"],
#     )
#     return mock_df.head()


# @pytest.fixture(scope='function')
# def example_fixture():
#     LOGGER.info("Setting Up Example Fixture...")
#     yield
#     LOGGER.info("Tearing Down Example Fixture...")
