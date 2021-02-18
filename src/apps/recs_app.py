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


def run(engine, Session):

    session = Session()

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

    # TODO styling, e.g. gray if not active
    st.dataframe(rec_df.sort_values("purchase_date"), width=None, height=None)

    st.write("Record Of The Day:")
    st.table(rec_df_small.sample(1).squeeze())

    session.close()
    # Session.remove()

    # result = (
    #     session.query(CreditTrx.credit_saldo)
    #     .order_by(CreditTrx.credit_trx_id.desc())
    #     .first()[0]
    # )
    # st.write(f"Actual Credit Saldo: {result}")

    # _, trx_df = db_functions._load_credit_trx_table_to_df(engine)
    # st.dataframe(trx_df.tail(6), width=None, height=None)
