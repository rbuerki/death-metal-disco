import streamlit as st

import src.db_connect as db_connect
from src.multiapp import MultiApp
from src.apps import test_app, crud_app  # import your app modules here

st.set_page_config(
    page_title="DiscoBase",
    page_icon="🦇",
    layout="centered",
    initial_sidebar_state="auto",
)


@st.cache(allow_output_mutation=True)
def get_session():
    config_params = db_connect.read_yaml("config.yaml", "DB_PROD")
    engine = db_connect.create_engine(config_params)
    session = db_connect.create_session(engine)
    return session


session = get_session()

st.title("Death Metal Disco")
st.write(session)

multiapp = MultiApp()

# Add application pages here
multiapp.add_app("TEST", test_app.run)
multiapp.add_app("CRUD", crud_app.run)

# Run the main app # TODO add args for session ...
multiapp.run_app()
