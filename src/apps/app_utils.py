from typing import Any, List, Tuple

import datetime as dt
import pandas as pd
import sqlalchemy
import streamlit as st

from src import db_functions
from src.db_declaration import CreditTrx


genre_list = [
    "Black Metal",
    "Crossover",
    "Crust",
    "Death Metal",
    "Grindcore",
    "Hardcore",
    "Punk",
    "Speed Metal",
    "Thrash Metal",
]

record_format_list = [
    '10"',
    '12"',
    "2xLP",
    '7"',
    "LP",
    "MLP",
    'Pic-7"',
    "Pic-LP",
    "Tape",
]

essential_columns_list = [
    "artist",
    "title",
    "genre",
    "label",
    "year",
    "record_format",
    "vinyl_color",
    "lim_edition",
    "remarks",
    "purchase_date",
    "price",
    "rating",
    "is_digitized",
]


# @st.cache() - NOTE Caching this function hangs up Streamlit
def create_record_dataframes(
    session: sqlalchemy.orm.session.Session,
    small_cols: List[str] = essential_columns_list,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return two dataframes with all the record related data. The
    second is a subset of the first, with active records and selected
    columns only. These dataframes are used for display in the
    `recs_app`. The data loading uses the `_load_record_related_data`
    function that was originally designed for data export.
    """
    _, rec_df_full = db_functions._load_record_related_data_to_df(
        session, include_id_column=True
    )
    for col in rec_df_full[["artist", "artist_country", "label"]]:
        rec_df_full[col] = (
            rec_df_full[col]
            .astype(str)
            .str.replace("[", "")
            .str.replace("]", "")
            .str.replace("'", "")
        )
    rec_df_full["purchase_date"] = rec_df_full["purchase_date"].dt.date
    rec_df_full.sort_values("purchase_date", inplace=True)
    rec_df_active = rec_df_full[rec_df_full["is_active"] == 1]
    rec_df_small = rec_df_active.set_index("record_id", drop=True)
    rec_df_small = rec_df_small[small_cols].copy()

    return rec_df_full, rec_df_small


def create_trx_dataframe(
    session: sqlalchemy.orm.session.Session,
) -> pd.DataFrame:
    """Return a dataframe containing a customized view of the
    credit_trx table, including the record titles for better
    orientation. Used in the trx_app.
    """
    result_list = (
        session.query(CreditTrx).order_by(CreditTrx.credit_trx_id).all()
    )
    dict_list = []

    for result in result_list:
        try:
            title = result.record.title
        except AttributeError:
            title = ""

        record_data_dict = {
            "credit_trx_id": result.credit_trx_id,
            "credit_trx_date": dt.datetime.strftime(
                result.credit_trx_date, "%Y-%m-%d"
            ),
            "credit_trx_type": result.credit_trx_type,
            "credit_value": result.credit_value,
            "credit_saldo": result.credit_saldo,
            "record_id": result.record_id,
            "record_title": title,
            "created_at": result.created_at,
        }
        dict_list.append(record_data_dict)

    trx_df = pd.DataFrame(dict_list, columns=dict_list[0].keys())

    return trx_df


def display_collection_table(df: pd.DataFrame, **kwargs):
    """Apply some styling and display an interactive table
    for dataframe containing a collection of records. Additional
    kwargs can be passed to st.dataframe().
    """
    st.dataframe(
        df.style.format(
            {"price": "{:,.2f}", "rating": "{:.0f}"}, na_rep="-"
        ).applymap(
            _set_color_grey,
            subset=pd.IndexSlice[df.index[df["is_active"] == 0], :],
        ),
        **kwargs
    )


def display_a_pretty_record_table(series: pd.Series):
    """Apply some styling and display a static table
    for a single record.
    """
    df = series.to_frame()
    st.table(
        df.style.format({}, na_rep="-")
        .set_precision(2)
        .set_properties(**{"max-width": "400px", "min-width": "400px"})
        .applymap(
            _set_color_purple,
            subset=pd.IndexSlice[
                df.index[df.index.isin(["artist", "title"])], :
            ],
        )
        .applymap(
            _set_bold_font,
            subset=pd.IndexSlice[
                df.index[df.index.isin(["artist", "title"])], :
            ],
        )
    )


def _set_color_grey(val: Any) -> str:
    """Take a scalar and return a string with css property.
    (Called within `display_collection_table`.)
    """
    return "color: darkgrey"


def _set_color_purple(val: Any) -> str:
    """Take a scalar and return a string with css property.
    (Called within `display_a record_table`.)
    """
    return "color: purple"  # streamlit's primary color: #f63366


def _set_bold_font(val: Any) -> str:
    """Take a scalar and return a string with css property.
    (Called within `display_a record_table`.)
    """
    return "font-weight: bold"
