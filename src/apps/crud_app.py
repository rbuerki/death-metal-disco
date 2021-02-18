import datetime as dt

import streamlit as st

from src import db_functions
from src.apps import app_utils

# TODO: does not work because session is created in different thread
# _, session = db_connect.main()


trx_types = [
    "Purchase",
    "Update",
    "Remove",
]


def run(engine, Session):

    session = Session()

    trx_type: str = st.selectbox("Transaction Type", trx_types)
    st.write("---")

    if trx_type == "Purchase":
        artist: str = st.text_input(
            "Artist (separate multiple artists with ';')"
        )
        artist_country = st.text_input(
            "(Artist) Country (one for each artist, separate with ';')"
        )
        title = st.text_input("Title")
        genre = st.selectbox("Genre", app_utils.genre_list, 3)
        label = st.text_input("Label (separate multiple labels with ';')")
        year = st.number_input("Year", value=dt.date.today().year, format="%d")
        record_format = st.selectbox("Format", app_utils.record_format_list, 6)
        vinyl_color = st.text_input("Vinyl Color")
        lim_edition = st.text_input("Lim Edition")
        number = st.text_input("Number")
        remarks = st.text_input("Remarks")
        purchase_date = st.date_input("Purchase Date", value=dt.date.today())
        price = st.number_input(
            "Price", value=20.00, min_value=0.00, step=5.00, format="%f"
        )
        rating = st.text_input("Rating")
        is_digitized = st.number_input(
            "is digitized",
            value=0,
            min_value=0,
            max_value=1,
            step=1,
            format="%i",
        )
        is_active = st.number_input(
            "is active", value=1, min_value=0, max_value=1, step=1, format="%d"
        )
        credit_value = st.number_input(
            "Credits", value=1, min_value=0, max_value=1, step=1, format="%d"
        )

        insert: bool = st.checkbox("Insert Record")
        if insert:

            artist_list = [a.strip() for a in artist.split(";")]
            artist_country_list = [c.strip() for c in artist_country.split(";")]
            label_list = [l.strip() for l in label.split(";")]
            if len(artist_list) != len(artist_country_list):
                raise AssertionError(
                    "Need same number of artists and artist countries."
                )

            record_data_dict = {
                "trx_type": trx_type,
                "artist": artist_list if artist_list != "" else None,
                "artist_country": artist_country_list
                if artist_country_list != ""
                else None,
                "title": title if title != "" else None,
                "genre": genre if genre != "" else None,
                "label": label_list if label_list != "" else None,
                "year": year,
                "record_format": record_format if record_format != "" else None,
                "vinyl_color": vinyl_color if vinyl_color != "" else None,
                "lim_edition": lim_edition if lim_edition != "" else None,
                "number": number if number != "" else None,
                "remarks": remarks if remarks != "" else None,
                "purchase_date": purchase_date,
                "price": price,
                "rating": rating if rating != "" else None,
                "is_digitized": is_digitized,
                "is_active": is_active,
                "credit_value": credit_value,
            }
            st.write(record_data_dict)

            # TODO Install validations

            if record_data_dict:

                commit = st.button("Commit Transaction")
                if commit and isinstance(record_data_dict, dict):
                    db_functions.add_new_record(session, record_data_dict)
                    st.write("Record inserted.")
                    # TODO write actual credit score
                    # TODO OUtput if artist, label, genre etc. has been created or updated

    elif trx_type == "Update":
        artist = st.text_input(
            "Artist (Note: in case of split records only first artist is checked)",
            value="",
        )
        title = st.text_input("Title", value="")

        if artist != "" and title != "":
            record = db_functions.fetch_a_record_from_the_shelf(
                session, artist, title
            )
            if record is not None:
                st.write("---")
                artist = st.text_input(
                    "Artist",
                    value="; ".join(
                        [artist.artist_name for artist in record.artists]
                    ),
                )
                artist_country = st.text_input(
                    "(Artist) Country",
                    value="; ".join(
                        [artist.artist_country for artist in record.artists]
                    ),
                )
                title = st.text_input("Title", value=record.title)
                genre = st.text_input("Genre", value=record.genre.genre_name)
                label = st.text_input(
                    "Label",
                    value="; ".join(
                        [label.label_name for label in record.labels]
                    ),
                )
                year = st.number_input("Year", value=record.year)
                record_format = st.text_input(
                    "Format", value=record.record_format.format_name
                )
                vinyl_color = st.text_input(
                    "Vinyl Color", value=record.vinyl_color
                )
                lim_edition = st.text_input(
                    "Lim Edition", value=record.lim_edition
                )
                number = st.text_input("Number", value=record.number)
                remarks = st.text_input("Remarks", value=record.remarks)
                price = st.number_input(
                    "Price",
                    value=float(record.price),
                    min_value=0.00,
                    step=5.00,
                    format="%f",
                )
                is_digitized = st.number_input(
                    "is digitized", value=record.is_digitized
                )
                rating = st.text_input("Rating", value=record.rating)
                is_active = st.number_input("is active", value=record.is_active)
                purchase_date = st.date_input(
                    "Purchase Date", value=record.purchase_date
                )

                # NOTE I could create a reaktivation trx, if I set to 1
                # credit_value = st.number_input(
                #     "Credits", value=0, min_value=0, max_value=1, step=1, format="%d"
                # )

                update: bool = st.checkbox("Update Record")
                if update:

                    artist_list = [a.strip() for a in artist.split(";")]
                    artist_country_list = [
                        c.strip() for c in artist_country.split(";")
                    ]
                    label_list = [l.strip() for l in label.split(";")]
                    if len(artist_list) != len(artist_country_list):
                        raise AssertionError(
                            "Need same number of artists and artist countries."
                        )

                    record_data_dict = {
                        "trx_type": trx_type,
                        "artist": artist_list if artist_list != "" else None,
                        "artist_country": artist_country_list
                        if artist_country_list != ""
                        else None,
                        "title": title if title != "" else None,
                        "genre": genre if genre != "" else None,
                        "label": label_list if label_list != "" else None,
                        "year": year,
                        "record_format": record_format
                        if record_format != ""
                        else None,
                        "vinyl_color": vinyl_color
                        if vinyl_color != ""
                        else None,
                        "lim_edition": lim_edition
                        if lim_edition != ""
                        else None,
                        "number": number if number != "" else None,
                        "remarks": remarks if remarks != "" else None,
                        "purchase_date": purchase_date,
                        "price": price,
                        "rating": rating if rating != "" else None,
                        "is_digitized": is_digitized,
                        "is_active": is_active,
                        # "credit_value": credit_value,
                    }
                    st.write(record_data_dict)
                    # TODO Install validations

                    if record_data_dict:
                        commit: bool = st.checkbox("Commit Transaction.")
                        if commit and isinstance(record_data_dict, dict):
                            db_functions.update_record(
                                session, record_data_dict
                            )
                            st.write("Record updated.")
                            # TODO Output if artist, label, genre etc. has been created or updated

    elif trx_type == "Remove":
        artist = st.text_input(
            "Artist (Note: for splits enter first artist only)", value=""
        )
        title = st.text_input("Title", value="")

        if artist != "" and title != "":
            record = db_functions.fetch_a_record_from_the_shelf(
                session, artist, title
            )
            if record is not None:
                if record.is_active == 0:
                    st.write(
                        "Record is already inactive. You cannot remove it twice."
                    )
                elif record.is_active == 1:
                    st.write("---")
                    removal_date = st.date_input(
                        "Removal Date", value=dt.date.today()
                    )
                    credit_value: int = st.number_input(
                        "Credits",
                        value=0,
                        min_value=0,
                        max_value=1,
                        step=1,
                        format="%d",
                    )

                    remove: bool = st.checkbox("Inactivate Record")
                    if remove:

                        record_data_dict = {
                            "trx_type": trx_type,
                            "artist": " / ".join(
                                [
                                    artist.artist_name
                                    for artist in record.artists
                                ]
                            ),
                            "title": record.title,
                            "genre": record.genre.genre_name,
                            "label": " / ".join(
                                [label.label_name for label in record.labels]
                            ),
                            "year": record.year,
                            "record_format": record.record_format.format_name,
                            "vinyl_color": record.vinyl_color,
                            "lim_edition": record.lim_edition,
                            "number": record.number,
                            "remarks": record.remarks,
                            "purchase_date": record.purchase_date,
                            "price": record.price,
                            "rating": record.rating,
                            "is_digitized": record.is_digitized,
                            "is_active": 0,
                            "removal_date": removal_date,
                            "credit_value": credit_value,
                        }
                        st.write(record_data_dict)

                        if record_data_dict:

                            commit: bool = st.checkbox("Commit Transaction.")
                            if commit and isinstance(record_data_dict, dict):
                                db_functions.set_record_to_inactive(
                                    session, record_data_dict
                                )
                                st.write("Record set to inactive.")
                                # TODO Output if artist, label, genre etc. has been created or updated

    # TODO, problably not ...
    session.close()
