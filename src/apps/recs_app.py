import streamlit as st

# from src import db_functions  # TODO Update problems, see below
from src.apps import app_utils  # , crud_app  # TODO Update problems, see below


def run(engine, Session):

    session = Session()

    st.sidebar.write("---")
    st.sidebar.write("Filter Records:")
    artist = st.sidebar.text_input("Artist")
    title = st.sidebar.text_input("Title")
    label = st.sidebar.text_input("Label")
    record_format = st.sidebar.text_input("Format")
    genre = st.sidebar.text_input("Genre")
    year = st.sidebar.number_input("Release Year", 0)
    rating = st.sidebar.slider("Rating", 0, 10, (0, 0), step=1)

    rec_df_full, rec_df_small = app_utils.create_record_dataframes(session)

    # Display the collection table
    st.write("")
    st.write("Record table (open fullscreen view):")
    app_utils.display_collection_table(rec_df_full, width=None, height=100)
    st.write("")

    # Filter the records according to sidetable
    if artist:
        rec_df_small = rec_df_small[
            rec_df_small["artist"].str.lower().str.contains(artist.lower())
        ]
    if title:
        rec_df_small = rec_df_small[
            rec_df_small["title"].str.lower() == title.lower()
        ]
    if label:
        rec_df_small = rec_df_small[
            rec_df_small["label"].str.lower().str.contains(label.lower())
        ]
    if record_format:
        rec_df_small = rec_df_small[
            rec_df_small["record_format"].str.lower() == record_format.lower()
        ]
    if genre:
        rec_df_small = rec_df_small[
            rec_df_small["genre"].str.lower() == genre.lower()
        ]
    if year != 0:
        rec_df_small = rec_df_small[rec_df_small["year"] == year]
    if rating[1] != 0:
        rec_df_small = rec_df_small[
            (rec_df_small["rating"] >= rating[0])
            & (rec_df_small["rating"] <= rating[1])
        ]

    # Display either filtered records or record-of-the-day
    if (
        artist != ""
        or title != ""
        or label != ""
        or record_format != ""
        or genre != ""
        or year != 0
        or rating[1] != 0
    ):
        n_recs = len(rec_df_small)
        st.write(f"{n_recs} Filtered Records:")
        for _, row in rec_df_small.iterrows():
            app_utils.display_a_pretty_record_table(row.squeeze())

    else:
        st.write("Record Of The Day:")
        record_of_the_day = rec_df_small.sample(1).squeeze()
        app_utils.display_a_pretty_record_table(record_of_the_day)

        # # TODO Goal: allow update of rotd, Problem: reloads new record at every input
        # update_record = st.checkbox("Update")
        # if update_record:
        #     artist = record_of_the_day["artist"]
        #     title = record_of_the_day["title"]
        #     trx_type = "Update"
        #     record = db_functions.fetch_a_record_from_the_shelf(
        #         session, artist, title
        #     )
        #     # NOTE: The next block is copied from CRUD App's Update workflow
        #     record_data = crud_app.display_record_update_form_and_return_data(
        #         record, trx_type
        #     )
        #     update: bool = st.checkbox("Update Record")
        #     if update:
        #         record_data = crud_app.prepare_record_data_for_DB_insert(
        #             record_data
        #         )
        #         st.write(record_data)
        #         if record_data:
        #             commit: bool = st.checkbox("Commit Transaction.")
        #             if commit and isinstance(record_data, dict):
        #                 db_functions.update_record(session, record_data)
        #                 st.write("Record updated.")

        session.close()
