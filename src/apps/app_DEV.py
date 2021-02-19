import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src import db_functions
from src.apps import app_utils
from src.db_declaration import (
    Artist,
    CreditTrx,
    Genre,
    Label,
    Record,
    RecordFormat,
)

# DEV BOILERPLATE ONLY

import src.db_connect as db_connect

st.set_page_config(
    page_title="DiscoBase",
    page_icon="🦇",
    layout="centered",
    initial_sidebar_state="auto",
)


@st.cache(allow_output_mutation=True)
def get_engine_and_scoped_session():
    """Note: This function is defined in this module (and not in
    db_connect) because of the caching option.
    """
    config_params = db_connect.read_yaml("config.yaml", "DB_PROD")
    engine = db_connect.create_engine(config_params)
    Session = db_connect.create_scoped_session(engine)
    return engine, Session


engine, Session = get_engine_and_scoped_session()
session = Session()

# DataFrames
rec_df_full, rec_df_small = app_utils.create_record_dataframes(session)
top_sorted = rec_df_small.sort_values(
    ["rating", "purchase_date"], ascending=False
)
top_sorted.index = range(1, len(top_sorted) + 1)


#  CODE HERE

n_top = 15
st.write("")
st.write(f"Top {n_top} Rated Records by Rating and Date:")
st.table(top_sorted[["artist", "title", "rating"]].head(n_top))
st.write("")

n_top = 15
st.write("")
st.write(f"Records by Rating:")
st.table(rec_df_small.groupby("rating", dropna=False)["title"].count())
st.write("")


st.write("")
st.write("Records by Genre:")
st.table(rec_df_small.groupby("genre")["title"].count())
st.write("")

# TODO - not correct because of the splits, have to take from db
st.write("")
st.write("Records by Label:")
st.table(rec_df_small.groupby("label")["title"].count())
st.write("")

# TODO - not correct because of the split, have to take from db
st.write("")
st.write("Records by Artist):")
st.table(rec_df_small.groupby("artist")["title"].count())
st.write("")


session.close()
