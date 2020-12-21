import logging
import sqlite3
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd

import sqlite_utils
import sql_statements


PATH_TO_COLLECTION = Path(
    r"C:\Users\r2d4\OneDrive\_raph\sounds\Collection\collection_albums.xlsx"
)
PATH_TO_DB = Path()


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


def load_albums_into_database(
    conn: sqlite3.Connection, df: pd.DataFrame, table_name: str,
):
    """Load a dataframe into the DB. Pass the table name
    and connection. If the table already exists the contents
    will be overwritten.
    """
    df.to_sql(table_name, if_exists="replace", con=conn)
    logging.info(
        "Table with shape {df.shape} successfully loaded into tabe {table_name}!"
    )


def main(path=PATH_TO_COLLECTION):
    conn, _ = sqlite_utils.connect()
    sqlite_utils.execute_query(conn, sql_statements.create_albums)
    df = load_albums_from_xlsx(path)
    load_albums_into_database(conn, df, "albums")


if __name__ == "__main__":
    main()
