import plotly.graph_objects as go
import streamlit as st

from src.apps import app_utils
from src.db_declaration import CreditTrx


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
    fig.update_layout(
        autosize=False,
        width=300,
        height=300,
        margin=dict(l=10, r=10, b=10, t=10, pad=4),
    )

    st.plotly_chart(fig)

    trx_df = app_utils.create_trx_dataframe(session)
    st.dataframe(trx_df.tail(10), width=None, height=None)

    session.close()
