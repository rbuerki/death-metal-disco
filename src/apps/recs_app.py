import streamlit as st

from src.apps import app_utils


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

        session.close()
