import datetime as dt
from typing import Dict

import streamlit as st

from src import db_functions
from src.apps import app_utils
from src.db_declaration import Artist, Record


trx_types = [
    "Purchase",
    "Update",
    "Remove",
]


def run(engine, Session):
    """This is the main entry point for the CRUD app.
    It contains workflows for the 3 trx_tpyes specified above.
    All CRUD-specific helper functions that are called within
    these workflows can be found below.
    """
    session = Session()

    trx_type: str = st.selectbox("Transaction Type", trx_types)
    st.write("---")

    # Purchase Workflow
    if trx_type == "Purchase":
        record_data = display_record_purchase_form_return_data(trx_type)
        insert: bool = st.checkbox("Insert Record")
        if insert:
            record_data = prepare_record_data_for_DB_insert(record_data)
            st.write(record_data)
            if record_data:
                commit = st.button("Commit Transaction")
                if commit and isinstance(record_data, dict):
                    db_functions.add_new_record(session, record_data)
                    st.write("Record inserted.")
                    # TODO Output if artist, label etc. has been created / updated

    # Update Workflow
    elif trx_type == "Update":
        artist, title = display_record_select_form(session)
        if artist != "-" and title != "-":
            record = db_functions.fetch_a_record_from_the_shelf(
                session, artist, title
            )
            if record is not None:
                st.write("---")
                record_data = display_record_update_form_and_return_data(
                    record, trx_type
                )
                update: bool = st.checkbox("Update Record")
                if update:
                    record_data = prepare_record_data_for_DB_insert(record_data)
                    st.write(record_data)
                    if record_data:
                        commit: bool = st.checkbox("Commit Transaction.")
                        if commit and isinstance(record_data, dict):
                            db_functions.update_record(session, record_data)
                            st.write("Record updated.")
                            # TODO Output if artist, label etc. has been created / updated

    # Removal (Inactivation) Workflow - no real deletion from DB!
    elif trx_type == "Remove":
        artist, title = display_record_select_form(session)
        if artist != "-" and title != "-":
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
                    (
                        removal_date,
                        credit_value,
                    ) = display_record_removal_form_and_return_data()
                    remove: bool = st.checkbox("Inactivate Record")
                    if remove:
                        record_data = create_record_data_for_removal(
                            record, trx_type, removal_date, credit_value
                        )
                        st.write(record_data)
                        if record_data:
                            commit: bool = st.checkbox("Commit Transaction.")
                            if commit and isinstance(record_data, dict):
                                db_functions.set_record_to_inactive(
                                    session, record_data
                                )
                                st.write("Record set to inactive.")

    session.close()


# ALL CRUD-HELPER FUNCTIONS HERE


def display_record_purchase_form_return_data(trx_type: str) -> Dict:
    """Display an input form for a record addition and return a dict
    with the data inserted by the user.
    """
    artist = st.text_input("Artist (separate multiple artists with ';')")
    artist_country = st.text_input(
        "(Artist) Country (one for each artist, separate with ';')"
    )
    title = st.text_input("Title")
    genre = st.selectbox("Genre", app_utils.genre_list, 3)
    label = st.text_input("Label (separate multiple labels with ';')")
    year = st.number_input("Year", value=dt.date.today().year, format="%d")
    record_format = st.selectbox("Format", app_utils.record_format_list, 4)
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
        "is digitized", value=0, min_value=0, max_value=1, step=1, format="%i",
    )
    is_active = st.number_input(
        "is active", value=1, min_value=0, max_value=1, step=1, format="%d"
    )
    credit_value = st.number_input(
        "Credits", value=1, min_value=0, max_value=1, step=1, format="%d"
    )

    record_data = {
        "trx_type": trx_type,
        "artist": artist if artist != "" else None,
        "artist_country": artist_country if artist_country != "" else None,
        "title": title if title != "" else None,
        "genre": genre,
        "label": label if label != "" else "NA",
        "year": year,
        "record_format": record_format,
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
    return record_data


def prepare_record_data_for_DB_insert(record_data: Dict) -> Dict:
    """For data fields in many-to-many relationships (artist,
    artist_country and labels) the input fields must to be parsed
    to list format. So we replace the old values with these new
    lists in the `record_data` dict and return it.
    """
    if record_data["artist"] is None or record_data["title"] is None:
        raise AssertionError("Artist and / or Title cannot be None.")

    artist_list = [art.strip() for art in record_data["artist"].split(";")]
    artist_country_list = [
        co.strip() for co in record_data["artist_country"].split(";")
    ]
    label_list = [lab.strip() for lab in record_data["label"].split(";")]

    if len(artist_list) != len(artist_country_list):
        raise AssertionError(
            "Need the same number of artists and artist countries."
        )

    record_data["artist"] = artist_list
    record_data["artist_country"] = artist_country_list
    record_data["label"] = label_list
    return record_data


def display_record_select_form(session):
    """Display selectboxes for artist and title for selection
    of a record. Return the two values. (Title options are
    dynamically adjusted to artist selection.)
    """
    artist_list = sorted(
        [artist.artist_name for artist in session.query(Artist).all()]
    )
    artist_list.insert(0, "-")
    artist = st.selectbox(
        "Artist (Note: in case of split records only first artist is checked)",
        options=artist_list,
    )
    if artist == "-":
        title = st.text_input("Title", value="-")
    else:
        title_list = [
            record.title
            for record in session.query(Record)
            .filter(Record.artists.any(Artist.artist_name == artist))
            .all()
        ]
        title = st.selectbox("Title", options=title_list)
    return artist, title


def display_record_update_form_and_return_data(record, trx_type: str) -> Dict:
    """Display an input form for a record update. It displays the
    actual values stored in the DB, which can be overwritten. Return a
    dictionary with the data updated by the user.
    """
    artist = st.text_input(
        "Artist",
        value="; ".join([artist.artist_name for artist in record.artists]),
    )
    artist_country = st.text_input(
        "(Artist) Country",
        value="; ".join([artist.artist_country for artist in record.artists]),
    )
    title = st.text_input("Title", value=record.title)
    genre = st.text_input("Genre", value=record.genre.genre_name)
    label = st.text_input(
        "Label", value="; ".join([label.label_name for label in record.labels]),
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
    is_digitized = st.number_input("is digitized", value=record.is_digitized)
    rating = st.text_input("Rating", value=record.rating)
    is_active = st.number_input("is active", value=record.is_active)
    purchase_date = st.date_input("Purchase Date", value=record.purchase_date)

    record_data = {
        "trx_type": trx_type,
        "artist": artist if artist != "" else None,
        "artist_country": artist_country if artist_country != "" else None,
        "title": title if title != "" else None,
        "genre": genre,
        "label": label if label != "" else "NA",
        "year": year,
        "record_format": record_format,
        "vinyl_color": vinyl_color if vinyl_color != "" else None,
        "lim_edition": lim_edition if lim_edition != "" else None,
        "number": number if number != "" else None,
        "remarks": remarks if remarks != "" else None,
        "purchase_date": purchase_date,
        "price": price,
        "rating": rating if rating != "" else None,
        "is_digitized": is_digitized,
        "is_active": is_active,
        # "credit_value": credit_value,  # we dont return a cretid value yet
    }
    return record_data


def display_record_removal_form_and_return_data():
    """Give the user the possibility to set values for
    the removal date (defaults to actual date) and for
    if credits are returned for the removal.
    """
    removal_date = st.date_input("Removal Date", value=dt.date.today())
    credit_value: int = st.number_input(
        "Credits", value=0, min_value=0, max_value=1, step=1, format="%d",
    )
    return removal_date, credit_value


def create_record_data_for_removal(
    record, trx_type: str, removal_date: dt.datetime, credit_value: float
) -> Dict:
    """Create a dictionary of data for the record selected for
    removal. Most values are for display only. We actualy only need
    artist and title for the record identification and the last
    three values in the dict for the transaction.
    """
    record_data = {
        "trx_type": trx_type,
        "artist": "; ".join([artist.artist_name for artist in record.artists]),
        "title": record.title,
        "genre": record.genre.genre_name,
        "label": "; ".join([label.label_name for label in record.labels]),
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
    return record_data
