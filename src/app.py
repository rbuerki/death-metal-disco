import streamlit as st

import src.db_connect as db_connect
from src.MultiApp import MultiApp
from src.apps import crud_app, recs_app, trx_app


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


st.title("Death Metal Disco")
st.write(Session)

multiapp = MultiApp()

# Add application pages here
multiapp.add_app("Records", recs_app.run)
multiapp.add_app("Credit Trx", trx_app.run)
multiapp.add_app("CRUD Operations", crud_app.run)


# Run the main app # TODO add args for session ...
multiapp.run_app(engine, Session)
