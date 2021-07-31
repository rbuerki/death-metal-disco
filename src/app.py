import streamlit as st

from src import db_functions, db_connect
from src.MultiApp import MultiApp
from src.apps import crud_app, lists_app, recs_app, stats_app, trx_app


st.set_page_config(
    page_title="DiscoBase",
    page_icon="🦇",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("Death Metal Disco")
# st.write("---")


@st.cache(allow_output_mutation=True)
def get_engine_and_scoped_session():
    """Note: This function is defined in this module (and not in
    db_connect) because of the caching option.
    """
    config_params = db_connect.read_yaml(
        "config.yaml", "DB_PROD"
    )  # NOTE: you can switch between "DB_PROD", "DB_DEV"
    engine = db_connect.create_engine(config_params)
    Session = db_connect.create_scoped_session(engine)
    return engine, Session


engine, Session = get_engine_and_scoped_session()

multiapp = MultiApp()

# Add application pages here
multiapp.add_app("Records", recs_app.run)
multiapp.add_app("Credit Trx", trx_app.run)
multiapp.add_app("Stats", stats_app.run)
multiapp.add_app("CRUD Operations", crud_app.run)
multiapp.add_app("Lists", lists_app.run)

# Check for regular credit additions
session = Session()
db_functions.add_regular_credits(session)

# Run the main app
multiapp.run_app(engine, Session)
