import collections
from pathlib import Path
from typing import Dict

import numpy as np
from src.db_declaration import (
    Artist,
    Genre,
    Label,
    Record,
    RecordFormat,
    CreditTrx,
)

CONFIG_PATH = (Path(__file__).parent.parent / "config.cfg").absolute()

RecordData = collections.namedtuple(
    "RecordData",
    [
        "artist",
        "title",
        "genre",
        "label",
        "year",
        "format",
        "vinyl_color",
        "lim_edition",
        "number",
        "remarks",
        "purchase_date",
        "price",
        "digitized",
        "rating",
        "active",
    ],
)

TEST_DATA = RecordData(
    artist="Year Of The Knife",
    title="Ultimate Aggression",
    genre="Hardcore",
    label="Southern Lord",
    year=2020,
    format="LP",
    vinyl_color="red",
    lim_edition=200,
    number=None,
    purchase_date=5,
    remarks="blah blah",
    price=20,
    digitized=True,
    rating=9,
    active=True,
)


def add_new_record(session, record_data: Dict):
    """Add a new record to the DB. The record data is passed as
    a dictionary. This function can be applied during batch
    uploads (initial data ingestion) or for adding singe new
    records later on.
    """

    r_artist = record_data["artist"]
    r_title = record_data["title"]
    r_format = record_data["format"]
    r_genre = record_data["genre"]
    r_label = record_data["label"]

    # Check if record already exists
    record = (
        session.query(Record)
        .join(Artist)
        .filter(
            (Record.title.ilike(r_title)),
            (Artist.artist_name.ilike(r_artist))
            # (Record.label_ids.any(Label.label_name == r_label)),  TODO
        )
        .one_or_none()
    )

    if record is not None:
        print(
            f"Record '{r_title}' by {r_artist} already exists, insert skipped."
        )  # TODO Update might be better
        return

    if record is None:
        record = Record(
            title=record_data["title"],
            year=record_data["year"],
            vinyl_color=record_data["vinyl_color"],
            lim_edition=record_data["lim_edition"],
            number=record_data["number"],
            remarks=record_data["remarks"],
            purchase_date=record_data["purchase_date"],
            price=record_data["price"],
            digitized=record_data["digitized"],
            rating=record_data["rating"],
            active=record_data["active"],
        )

    # Check if the artist already exists or has to be created
    artist = (
        session.query(Artist)
        .filter(Artist.artist_name.ilike(r_artist))
        .one_or_none()
    )
    if artist is None:
        artist = Artist(artist_name=r_artist, artist_country=None)
        session.add(artist)

    # Check if the format already exists or has to be created
    record_format = (
        session.query(RecordFormat)
        .filter(RecordFormat.format_name.ilike(r_format))
        .one_or_none()
    )
    if record_format is None:
        record_format = RecordFormat(format_name=r_format)
        session.add(record_format)

    # Check if the genre already exists or has to be created
    genre = (
        session.query(Genre)
        .filter(Genre.genre_name.ilike(r_genre))
        .one_or_none()
    )
    if genre is None:
        genre = Genre(genre_name=r_genre)
        session.add(genre)

    # Check if the label already exists or has to be created
    label = (
        session.query(Label)
        .filter(Label.label_name.ilike(r_label))
        .one_or_none()
    )
    if label is None:
        label = Label(label_name=r_label)
        session.add(label)

    # Create a trx
    credit_trx = CreditTrx(
        credit_trx_date=record_data["purchase_date"],
        credit_trx_type="Purchase",
        credit_value=-1,  # TODO: credit_value or -1,
        credit_saldo=(
            np.array(session.query(CreditTrx.credit_value).all()).sum()
            + -1  # TODO: credit_value
        ),
    )

    # Finally: Initialize the record relationships
    record.artist = artist
    record.genre = genre
    record.format = record_format
    record.genre = genre
    record.credit_trx.append(credit_trx)
    record.labels.append(label)  # many to many  TODO this does not work yet

    session.add(record)
    session.commit()
