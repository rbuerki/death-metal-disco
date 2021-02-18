import plotly.graph_objects as go
import streamlit as st

from src import db_functions
from src.db_declaration import (
    Artist,
    CreditTrx,
    Genre,
    Label,
    Record,
    RecordFormat,
)


def run(engine, Session):

    session = Session()

    result = (
        session.query(CreditTrx.credit_saldo)
        .order_by(CreditTrx.credit_trx_id.desc())
        .first()[0]
    )

    fig = go.Figure(
        go.Indicator(
            title={"text": "Actual Credit Saldo"},
            mode="delta",
            value=result,
            delta={"reference": 0},
        )
    )
    st.plotly_chart(fig)

    _, trx_df = db_functions._load_credit_trx_table_to_df(engine)
    st.dataframe(trx_df.tail(6), width=None, height=None)

    session.close()
