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

#  CODE HERE

