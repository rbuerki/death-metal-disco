from typing import Any, List, Tuple

import pandas as pd
import sqlalchemy
import streamlit as st

from src import db_functions

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
    "2LP",
    "2xLP",
    '7"',
    '7" Pic',
    "LP",
    "MLP",
    "Pic-LP",
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
    `recs_app`.
    """
    _, rec_df_full = db_functions._load_record_related_data_to_df(session)
    for col in rec_df_full[["artist", "artist_country", "label"]]:
        rec_df_full[col] = (
            rec_df_full[col]
            .astype(str)
            .str.replace("[", "")
            .str.replace("]", "")
            .str.replace("'", "")
        )
    rec_df_full.sort_values("purchase_date", inplace=True)
    rec_df_active = rec_df_full[rec_df_full["is_active"] == 1]
    rec_df_small = rec_df_active[small_cols].copy()

    return rec_df_full, rec_df_small


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


def display_a_record_table(series: pd.Series):
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