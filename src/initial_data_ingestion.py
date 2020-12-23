from pathlib import Path

from src.db_declaration import Base
from src import insert_record
from src import utils

CONFIG_PATH = Path.cwd().parent / "config.cfg"


def load_albums_from_xlsx(
    filepath: Union[Path, str], genres: Optional[List] = None
) -> pd.DataFrame:
    """Load the original album collection file into a dataframe.
    You can specify a list of genres you want to include
    (defaults to None).
    """
    df = pd.read_excel(filepath, engine="openpyxl")
    if genres:
        df = df[df["Genre"].isin(genres)]
    print(df.columns)
    return df


def main():
    path_to_db = utils.read_config_return_str(CONFIG_PATH, "SQLITE")
    engine = utils.create_engine(path_to_db)
    session = utils.create_session(engine)
    utils.create_DB_anew(session, Base)

