import streamlit as st

from src.db_declaration import CreditTrx


# DEV SECTION
import src.db_connect as db_connect


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

result = (
    session.query(CreditTrx.credit_saldo)
    .order_by(CreditTrx.credit_trx_id.desc())
    .first()[0]
)
st.write(f"Actual Credit Saldo: {result}")


# PROD SECTION


def run(engine, Session):

    # session = Session()

    # st.write(
    #     session.query(CreditTrx).order_by(CreditTrx.credit_trx_id.desc)[0][0]
    # )

    st.write("test again")

    Session.remove()
