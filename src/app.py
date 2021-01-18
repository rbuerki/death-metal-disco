import datetime as dt
from pathlib import Path

import streamlit as st

import src.db_functions as db_functions
import src.utils as utils

st.set_page_config(
    page_title="DiscoBase",
    page_icon="🦇",
    layout="centered",
    initial_sidebar_state="auto",
)

path_to_db = (
    r"C:\Users\r2d4\OneDrive\code\projects\20-02_disco\dev\DeafDiscoBase.db"
)
engine = utils.create_engine(path_to_db)
session = utils.create_session(engine)

trx_types = [
    "Purchase",
    "Update",
    "Remove",
]

st.title("Death Metal Disco")

trx_type: str = st.selectbox("Transaction Type", trx_types)
st.write("---")

if trx_type == "Purchase":
    artist = st.text_input("Artist")
    artist_country = st.text_input("(Artist) Country")
    title = st.text_input("Title")
    genre = st.text_input("Genre")
    label = st.text_input("Label")
    year = st.number_input("Year", value=dt.date.today().year, format="%d")
    record_format = st.text_input("Format")
    vinyl_color = st.text_input("Vinyl Color")
    lim_edition = st.text_input("Lim Edition")
    number = st.text_input("Number")
    remarks = st.text_input("Remarks")
    price = st.number_input(
        "Price", value=20.00, min_value=0.00, step=5.00, format="%f"
    )
    digitized = st.number_input(
        "Digitized", value=0, min_value=0, max_value=1, step=1, format="%i"
    )
    rating = st.text_input("Rating")
    active = st.number_input(
        "Active", value=1, min_value=0, max_value=1, step=1, format="%d"
    )
    purchase_date = st.date_input("Purchase Date", value=dt.date.today())
    credit_value = st.number_input(
        "Credits", value=1, min_value=0, max_value=1, step=1, format="%d"
    )

    insert: bool = st.checkbox("Insert Record")
    if insert:

        record_data_dict = {
            "trx_type": trx_type,
            "artist": artist if artist != "" else None,
            "artist_country": artist_country if artist_country != "" else None,
            "title": title if title != "" else None,
            "genre": genre if genre != "" else None,
            "label": label if label != "" else None,
            "year": year,
            "record_format": record_format if record_format != "" else None,
            "vinyl_color": vinyl_color if vinyl_color != "" else None,
            "lim_edition": lim_edition if lim_edition != "" else None,
            "number": number if number != "" else None,
            "remarks": remarks if remarks != "" else None,
            "price": price,
            "digitized": digitized,
            "rating": rating if rating != "" else None,
            "active": active,
            "purchase_date": purchase_date,
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
    artist = st.text_input("Artist", value="")
    title = st.text_input("Title", value="")

    if artist != "" and title != "":
        record = db_functions.fetch_a_record_from_the_shelf(
            session, artist, title
        )
        if record is not None:
            st.write("---")
            artist = st.text_input("Artist", value=record.artist.artist_name)
            artist_country = st.text_input(
                "(Artist) Country", value=record.artist.artist_country
            )
            title = st.text_input("Title", value=record.title)
            genre = st.text_input("Genre", value=record.genre.genre_name)
            label = st.text_input(
                "Label",
                value=" / ".join([label.label_name for label in record.labels]),
            )
            year = st.number_input("Year", value=record.year)
            record_format = st.text_input(
                "Format", value=record.record_format.format_name
            )
            vinyl_color = st.text_input("Vinyl Color", value=record.vinyl_color)
            lim_edition = st.text_input("Lim Edition", value=record.lim_edition)
            number = st.text_input("Number", value=record.number)
            remarks = st.text_input("Remarks", value=record.remarks)
            price = st.number_input(
                "Price",
                value=float(record.price),
                min_value=0.00,
                step=5.00,
                format="%f",
            )
            digitized = st.number_input("Digitized", value=record.digitized)
            rating = st.text_input("Rating", value=record.rating)
            active = st.number_input("Active", value=record.active)
            purchase_date = st.date_input(
                "Purchase Date", value=record.purchase_date
            )

            # NOTE I could create a reaktivation trx, if I set to 1
            # credit_value = st.number_input(
            #     "Credits", value=0, min_value=0, max_value=1, step=1, format="%d"
            # )

            update: bool = st.checkbox("Update Record")
            if update:

                record_data_dict = {
                    "trx_type": trx_type,
                    "artist": artist if artist != "" else None,
                    "artist_country": artist_country
                    if artist_country != ""
                    else None,
                    "title": title if title != "" else None,
                    "genre": genre if genre != "" else None,
                    "label": label if label != "" else None,
                    "year": year,
                    "record_format": record_format
                    if record_format != ""
                    else None,
                    "vinyl_color": vinyl_color if vinyl_color != "" else None,
                    "lim_edition": lim_edition if lim_edition != "" else None,
                    "number": number if number != "" else None,
                    "remarks": remarks if remarks != "" else None,
                    "price": price,
                    "digitized": digitized,
                    "rating": rating if rating != "" else None,
                    "active": active,
                    "purchase_date": purchase_date
                    # "credit_value": credit_value,
                }
                st.write(record_data_dict)
                # TODO Install validations

                if record_data_dict:
                    commit: bool = st.checkbox("Commit Transaction.")
                    if commit and isinstance(record_data_dict, dict):
                        db_functions.update_record(session, record_data_dict)
                        st.write("Record updated.")
                        # TODO Output if artist, label, genre etc. has been created or updated


elif trx_type == "Remove":
    # TODO The next 9 rows are shared with Update
    artist = st.text_input("Artist", value="")
    title = st.text_input("Title", value="")

    if artist != "" and title != "":
        record = db_functions.fetch_a_record_from_the_shelf(
            session, artist, title
        )
        if record is not None:
            if record.active == 0:
                st.write(
                    "Record is already inactive. You cannot remove it twice."
                )
            elif record.active == 1:
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
                        "artist": record.artist.artist_name,
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
                        "price": record.price,
                        "digitized": record.digitized,
                        "rating": record.rating,
                        "active": 0,
                        "purchase_date": record.purchase_date,
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
