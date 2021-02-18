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

_, rec_df = db_functions._load_record_related_data_to_df(session)
for col in rec_df[["artist", "artist_country", "label"]]:
    rec_df[col] = (
        rec_df[col]
        .astype(str)
        .str.replace("[", "")
        .str.replace("]", "")
        .str.replace("'", "")
    )
rec_df_active = rec_df[rec_df["is_active"] == 1]
rec_df_small = rec_df_active[app_utils.essential_columns_list].copy()


#  CODE HERE

st.sidebar.write("Filter Records:")
artist = st.sidebar.text_input("Artist")
title = st.sidebar.text_input("Title")
label = st.sidebar.text_input("Label")
genre = st.sidebar.text_input("Genre")
year = st.sidebar.number_input("Release Year", 0)
rating = st.sidebar.slider("Rating", 0, 10, (0, 0), step=1)

if artist:
    rec_df_small = rec_df_small[
        rec_df_small["artist"].str.lower().str.contains(artist.lower())
    ]
if title:
    rec_df_small = rec_df_small[
        rec_df_small["title"].str.lower() == title.lower()
    ]
if label:
    rec_df_small = rec_df_small[
        rec_df_small["label"].str.lower().str.contains(label.lower())
    ]
if genre:
    rec_df_small = rec_df_small[
        rec_df_small["genre"].str.lower() == genre.lower()
    ]
if year != 0:
    pass
    rec_df_small = rec_df_small[rec_df_small["year"] == year]
if rating[1] != 0:
    rec_df_small = rec_df_small[
        (rec_df_small["rating"] >= rating[0])
        & (rec_df_small["rating"] <= rating[1])
    ]

if (
    artist != ""
    or title != ""
    or label != ""
    or genre != ""
    or year != 0
    or rating[1] != 0
):
    rec_df_small = rec_df_small.reset_index(drop=True)
    for _, row in rec_df_small.iterrows():
        st.table(row.squeeze())
