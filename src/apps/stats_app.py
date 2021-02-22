import pandas as pd
import streamlit as st
from sqlalchemy import func

from src.apps import app_utils
from src.db_declaration import (
    Artist,
    ArtistRecordLink,
    Label,
    LabelRecordLink,
    Record,
)


def run(engine, Session):

    session = Session()

    # DataFrames
    _, rec_df_small = app_utils.create_record_dataframes(session)
    top_sorted = rec_df_small.sort_values(
        ["rating", "purchase_date"], ascending=False
    )
    top_sorted.index = range(1, len(top_sorted) + 1)

    # TODO this sucks somehow
    # q = session.query(Record.rating, func.count(Record.title)).group_by(
    #     Record.rating
    # )

    # df = pd.read_sql(q.statement, q.session.bind)
    # df.columns = ["rating", "record count"]
    # df = df.replace("None", np.nan)
    # df.set_index("rating", drop=True, inplace=True)
    # st.table(df.sort_values("rating", ascending=False))

    # st.write(rec_df_full[rec_df_full["rating"].notnull()])

    n_recs = 0  # session.query(
    #     func.count((Record.is_active)).filter(Record.is_active == 1)[0][0]
    # )
    st.write("")
    st.write(f"Total Active Records in Collection: {n_recs}")
    st.write("")

    n_top = 15
    st.write("")
    st.write(f"Top {n_top} Rated Records by Rating and Date:")
    st.table(top_sorted[["artist", "title", "rating"]].head(n_top))
    st.write("")

    st.write("")
    st.write("Records by Rating:")
    st.table(rec_df_small.groupby("rating", dropna=False)["title"].count())
    st.write("")

    st.write("")
    st.write("Records by Genre:")
    st.table(rec_df_small.groupby("genre")["title"].count())
    st.write("")

    st.write("")
    st.write("Records by Format:")
    st.table(rec_df_small.groupby("record_format")["title"].count())
    st.write("")

    # # TODO - not correct because of the splits, have to take from db
    q_label = (
        session.query(Label.label_name, func.count(LabelRecordLink.record_id))
        .join(LabelRecordLink, LabelRecordLink.label_id == Label.label_id)
        .join(Record, LabelRecordLink.record_id == Record.record_id)
        .filter(Record.is_active == 1)
        .group_by(Label.label_name)
    )

    st.write("")
    st.write("Records by Label:")
    df = pd.read_sql(q_label.statement, q_label.session.bind)
    df.set_index("label_name", drop=True, inplace=True)
    st.table(df)
    st.write("")

    # # TODO - not correct because of the split, have to take from db
    q_artist = (
        session.query(
            Artist.artist_name, func.count(ArtistRecordLink.artist_id)
        )
        .join(ArtistRecordLink, ArtistRecordLink.artist_id == Artist.artist_id)
        .join(Record, ArtistRecordLink.record_id == Record.record_id)
        .filter(Record.is_active == 1)
        .group_by(Artist.artist_name)
    )

    st.write("")
    st.write("Records by Artist:")
    df = pd.read_sql(q_artist.statement, q_artist.session.bind)
    df.set_index("artist_name", drop=True, inplace=True)
    st.table(df)
    st.write("")

    session.close()
