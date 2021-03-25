import pandas as pd
import streamlit as st
from sqlalchemy import func

from src.apps import app_utils
from src.db_declaration import (
    Artist,
    ArtistRecordLink,
    Genre,
    Label,
    LabelRecordLink,
    Record,
    RecordFormat,
)


def run(engine, Session):

    session = Session()

    # DataFrames - TODO check if I really need them ... only for n_top ...
    _, rec_df_small = app_utils.create_record_dataframes(session)
    top_sorted = rec_df_small.sort_values(
        ["rating", "purchase_date"], ascending=False
    )
    top_sorted.index = range(1, len(top_sorted) + 1)

    n_active = session.query(Record).filter(Record.is_active == 1).count()
    st.write("")
    st.write(f"Total Active Records in Collection: {n_active}")
    st.write("")

    # Top X by Rating & Date - TODO fix the artist name(s) display
    # "; ".join([artist.artist_name for artist in record.artists]
    n_top = 20
    q_top_x = session.query(Record.title, Record.rating).order_by(
        Record.rating.desc(), Record.purchase_date.desc()
    )

    st.write("")
    st.write(f"Top {n_top} Records by Rating and Date:")
    df = pd.read_sql(q_top_x.statement, q_top_x.session.bind)
    st.table(df.head(n_top))
    st.write("")

    # Record count by rating
    q_rating = (
        session.query(Record.rating, func.count(Record.format_id))
        .filter(Record.is_active == 1)
        .group_by(Record.rating)
        .order_by(Record.rating.desc())
    )

    st.write("")
    st.write("Records by Rating:")
    df = pd.read_sql(q_rating.statement, q_rating.session.bind)
    df.set_index("rating", drop=True, inplace=True)
    df["pct"] = df["count_1"] / sum(
        (list(df["count_1"])[:-1])
    )  # TODO make better
    st.table(df)
    st.write("")

    # Record count by genre
    q_genre = (
        session.query(Genre.genre_name, func.count(Record.format_id))
        .join(Record, Genre.genre_id == Record.genre_id)
        .filter(Record.is_active == 1)
        .group_by(Genre.genre_name)
        .order_by(func.count(Record.format_id).desc())
    )

    st.write("")
    st.write("Records by Genre:")
    df = pd.read_sql(q_genre.statement, q_genre.session.bind)
    df.set_index("genre_name", drop=True, inplace=True)
    st.table(df)
    st.write("")

    # Record count by format
    q_format = (
        session.query(RecordFormat.format_name, func.count(Record.format_id))
        .join(Record, RecordFormat.format_id == Record.format_id)
        .filter(Record.is_active == 1)
        .group_by(RecordFormat.format_name)
        .order_by(func.count(Record.format_id).desc())
    )

    st.write("")
    st.write("Records by Format:")
    df = pd.read_sql(q_format.statement, q_format.session.bind)
    df.set_index("format_name", drop=True, inplace=True)
    st.table(df)
    st.write("")

    # st.table(
    #     rec_df_small.groupby("record_format")["title"]
    #     .count()
    #     .sort_values(ascending=False)
    # )
    # st.write("")

    # Record count by label
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

    # Record count by artist
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
