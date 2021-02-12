import datetime as dt
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import sqlalchemy

import src.db_connect as db_connect
from src.db_declaration import (
    Artist,
    Genre,
    Label,
    Record,
    RecordFormat,
    CreditTrx,
)


CONFIG_PATH = (Path.cwd().parent / "config.yaml").absolute()


def fetch_a_record_from_the_shelf(
    session: sqlalchemy.orm.session.Session, artist: str, title: str
) -> sqlalchemy.orm.query.Query:
    """Query a record by title, artist and (optional) year,
    Return the query result object. Returns None if no record is
    found, raises an error if more than one record is matched.
    """
    record = (
        session.query(Record)
        .join(Artist)
        .filter(
            (Record.title.ilike(title)),
            (Artist.artist_name.ilike(artist))
            # (Record.label_ids.any(Label.label_name == r_label)),  TODO
        )
        .one_or_none()
    )
    return record


def add_new_record(session: sqlalchemy.orm.session.Session, record_data: Dict):
    """Add a new record to the DB. The record data is passed as
    a dictionary. This function can be applied during batch
    uploads (initial data ingestion) or for adding singe new
    records later on.
    """
    assert record_data["trx_type"] == "Purchase" or "Initial Load"

    r_artist = record_data["artist"]
    r_title = record_data["title"]
    r_format = record_data["record_format"]
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
        )
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
        artist = Artist(
            artist_name=r_artist, artist_country=record_data["artist_country"]
        )
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

    # Create a purchase trx
    credit_value = record_data["credit_value"] * -1
    try:
        credit_saldo = (
            session.query(CreditTrx.credit_saldo)
            .order_by(CreditTrx.credit_trx_id)
            .all()[-1][0]
        )
    except IndexError:
        # This is for initial data_ingestion only
        credit_saldo = 0

    credit_trx = CreditTrx(
        credit_trx_date=record_data["purchase_date"],
        credit_trx_type=record_data["trx_type"],
        credit_value=credit_value,
        credit_saldo=(credit_saldo + credit_value),
    )

    # Finally: Initialize the record relationships
    record.artist = artist
    record.record_format = record_format
    record.genre = genre
    record.credit_trx.append(credit_trx)

    record.labels.append(label)
    artist.labels.append(label)
    artist.genres.append(genre)
    genre.labels.append(label)

    session.add(record)
    session.commit()


def update_record(session: sqlalchemy.orm.session.Session, record_data: Dict):
    """Update the properties of an existing record in the DB.
    The record data is passed as a dictionary and data that
    has changed will be updated to the new values.
    """
    assert record_data["trx_type"] == "Update"

    r_artist = record_data["artist"]
    r_title = record_data["title"]
    r_format = record_data["record_format"]
    r_genre = record_data["genre"]
    r_label = record_data["label"]

    # Check if record already exists
    record = fetch_a_record_from_the_shelf(session, r_artist, r_title)

    if record is None:
        print(
            f"Record '{r_title}' by {r_artist} not found in DB, cannot update."
        )
        return

    if record is not None:
        record.title = record_data["title"]
        record.year = record_data["year"]
        record.vinyl_color = record_data["vinyl_color"]
        record.lim_edition = record_data["lim_edition"]
        record.number = record_data["number"]
        record.remarks = record_data["remarks"]
        record.purchase_date = record_data["purchase_date"]
        record.price = record_data["price"]
        record.digitized = record_data["digitized"]
        record.rating = record_data["rating"]
        record.active = record_data["active"]

    # Check if the artist already exists or has to be created
    artist = (
        session.query(Artist)
        .filter(Artist.artist_name.ilike(r_artist))
        .one_or_none()
    )
    if artist is None:
        artist = Artist(
            artist_name=r_artist, artist_country=record_data["artist_country"]
        )
        session.add(artist)
    else:
        artist.artist_country = record_data["artist_country"]

    # Check if the format already exists or has to be created
    record_format = (
        session.query(RecordFormat)
        .filter(RecordFormat.format_name.ilike(r_format))
        .one_or_none()
    )
    if record_format is None:
        record_format = RecordFormat(format_name=r_format)
        session.add(record_format)
    else:
        record_format.format_name = r_format

    # Check if the genre already exists or has to be created
    genre = (
        session.query(Genre)
        .filter(Genre.genre_name.ilike(r_genre))
        .one_or_none()
    )
    if genre is None:
        genre = Genre(genre_name=r_genre)
        session.add(genre)
    else:
        genre.genre_name = r_genre

    # Check if the label already exists or has to be created
    label = (
        session.query(Label)
        .filter(Label.label_name.ilike(r_label))
        .one_or_none()
    )
    if label is None:
        label = Label(label_name=r_label)
        session.add(label)
    else:
        label.label_name = r_label

    # # Create a purchase trx  TODO For reactivations I could charge a Credit Trx
    # credit_value = record_data["credit_value"] * -1
    # try:
    #     credit_saldo = (
    #         session.query(CreditTrx.credit_saldo)
    #         .order_by(CreditTrx.credit_trx_id)
    #         .all()[-1][0]
    #     )
    # except IndexError:
    #     # This is for initial data_ingestion only
    #     credit_saldo = 0

    # credit_trx = CreditTrx(
    #     credit_trx_date=record_data["purchase_date"],
    #     credit_trx_type=record_data["trx_type"],
    #     credit_value=credit_value,
    #     credit_saldo=(credit_saldo + credit_value),
    # )

    # Finally: Initialize the record relationships
    record.artist = artist
    record.record_format = record_format
    record.genre = genre
    # record.credit_trx.append(credit_trx)

    record.labels.append(label)
    artist.labels.append(label)
    artist.genres.append(genre)
    genre.labels.append(label)

    session.add(record)
    session.commit()


def set_record_to_inactive(
    session: sqlalchemy.orm.session.Session, record_data: Dict
):
    """Set a the status of a record to inactive. This is equivalent
    to a removal, because records are never fully deleted. This
    triggers a transaction with type "Removal" and can lead to a
    credit addition depending on the credit value entered.
    """
    assert record_data["trx_type"] == "Remove"

    r_artist = record_data["artist"]
    r_title = record_data["title"]

    # Check if record already exists
    record = fetch_a_record_from_the_shelf(session, r_artist, r_title)

    if record is None:
        print(f"Record '{r_title}' by {r_artist} not found, please check.")
        return

    if record is not None:
        if record.active == 0:
            print(
                f"Status of record '{r_title}' by {r_artist} is "
                f"already 0, please check."
            )
            return

        else:
            record.active = 0
            print("Record set to inactive.")

            # Create a Removal trx
            credit_value = record_data["credit_value"]
            credit_saldo = (
                session.query(CreditTrx.credit_saldo)
                .order_by(CreditTrx.credit_trx_id)
                .all()[-1][0]
            )

            credit_trx = CreditTrx(
                credit_trx_date=record_data["removal_date"],
                credit_trx_type=record_data["trx_type"],
                credit_value=credit_value,
                credit_saldo=(credit_saldo + credit_value),
            )

            # Initialize the record relationships
            record.credit_trx.append(credit_trx)

            session.add(record)
            session.commit()


def add_regular_credits(
    session: sqlalchemy.orm.session.Session, interval_days: int = 10
):
    """Every x days a new credit is added (to be spent
    on purchasing new records). This function checks
    the delta in days since the last addition and inserts
    the necessary credit transactions depending on the
    defined interval.
    """
    last_addition_date, days_since_last = _get_days_since_last_addition(session)

    while days_since_last >= 10:
        credit_trx_date = last_addition_date + dt.timedelta(days=interval_days)
        print(f"Creating 'Addition' Trx for: {credit_trx_date}")
        addition_trx = CreditTrx(
            credit_trx_date=credit_trx_date,
            credit_trx_type="Addition",
            credit_value=1,
            credit_saldo=(
                session.query(CreditTrx.credit_saldo)
                .order_by(CreditTrx.credit_trx_id)
                .all()[-1][0]
                + 1
            ),
            # TODO i should assert that the createdate is also max, also in add_record
            record_id=np.nan,
        )
        session.add(addition_trx)
        last_addition_date, days_since_last = _get_days_since_last_addition(
            session
        )

    session.commit()


def _get_days_since_last_addition(
    session: sqlalchemy.orm.session.Session,
) -> Tuple[dt.date, int]:
    """Return the date of and the number of days since the
    last transaction with type 'Addition' stored in the
    CreditTrx table. (This is called within 'add_credit').
    """
    last_addition_date = (
        session.query(CreditTrx.credit_trx_date)
        .filter(CreditTrx.credit_trx_type == "Addition")
        .order_by(CreditTrx.credit_trx_date.desc())
        .first()
    )[0]

    days_since_last = (dt.date.today() - last_addition_date).days

    return last_addition_date, days_since_last


def create_DB_anew(
    engine: sqlalchemy.engine.Engine,
    Base,  #: sqlalchemy.ext.declarative.AbstractConcreteBase,
):
    """Drop all existing tables from the database
    and create them anew. WARNING!
    """
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine)


# EXPORT DATA


def export_db_data_to_2_parquet_files(
    session: sqlalchemy.orm.session.Session,
    engine: sqlalchemy.engine.Engine,
    config_path: Path,
):
    """Create 2 tabular parquet files, one with record-related
    data (incl. information on artists, genres, labels), and one that
    is a copy of the `credit_trx` table. With help of these files the
    database can be repopulated after a complete reset.
    """

    record_df_tuple = _save_record_related_data_to_df(session)
    credit_trx_df_tuple = _save_credit_trx_table_to_df(engine)

    for df_tuple in [record_df_tuple, credit_trx_df_tuple]:
        _save_df_to_parquet(df_tuple, config_path)


def _save_record_related_data_to_df(
    session: sqlalchemy.orm.session.Session,
) -> Tuple[str, pd.DataFrame]:
    """Save all record-related data to Pandas Dataframe and return a
    tuple with a dataframe name string and the dataframe. Called
    within `export_db_data_to_2_parquet_files`.
    """
    result_list = session.query(Record).order_by(Record.record_id).all()
    dict_list = []

    for result in result_list:
        record_data_dict = {
            "record_id": result.record_id,
            "artist": result.artist.artist_name,  # TODO: has to be adapted to many-to-many
            "artist_country": result.artist.artist_country,  # TODO: has to be adapted to many-to-many
            "title": result.title,
            "genre": result.genre.genre_name,
            "label": [label.label_name for label in result.labels],
            "year": result.year,
            "record_format": result.record_format.format_name,
            "vinyl_color": result.vinyl_color,
            "lim_edition": result.lim_edition,
            "number": result.number,
            "remarks": result.remarks,
            "price": result.price,
            "digitized": result.digitized,
            "rating": result.rating,  # TODO: has to be datapted to one-to-many
            "is_active": result.active,
            "purchase_date": result.purchase_date,
        }
        dict_list.append(record_data_dict)

    records_df = pd.DataFrame(dict_list, columns=dict_list[0].keys())
    records_df.set_index("record_id", drop=True, inplace=True)
    df_name = "record_data"

    if (
        not records_df.index.is_monotonic_increasing
        and not records_df.index.is_unique
    ):
        raise AssertionError("record_ids are messed up, please check data.")

    return df_name, records_df


def _save_credit_trx_table_to_df(
    engine: sqlalchemy.engine.Engine,
) -> Tuple[str, pd.DataFrame]:
    """Copy credit_trx_table to Pandas Dataframe and return a tuple
    with a dataframe name string and the dataframe. Called within
    `export_db_data_to_2_parquet_files`.
    """
    credit_trx_df = pd.read_sql("credit_trx", engine)
    credit_trx_df.set_index("credit_trx_id", drop=True, inplace=True)
    df_name = "trx_data"

    if (
        not credit_trx_df.index.is_monotonic_increasing
        and not credit_trx_df.index.is_unique
    ):
        raise AssertionError("record_ids are messed up, please check data.")

    return df_name, credit_trx_df


def _save_df_to_parquet(df_tuple: Tuple[str, pd.DataFrame], config_path: Path):
    """Create date and timestamped directory and file name at path
    defined in config.yaml and save dataframe as back-up to parquet.
    Called within `export_db_data_to_2_parquet_files`.
    """
    df_name, df = df_tuple
    date_stamp = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d")
    datetime_stamp = dt.datetime.strftime(
        dt.datetime.now(), "%Y-%m-%d-%H-%M-%S"
    )

    back_up_params = db_connect.read_yaml(config_path, "BACK_UP")
    rel_path = back_up_params["REL_PATH"]
    target = Path.cwd() / rel_path / f"{date_stamp}"
    Path.mkdir(target, parents=True, exist_ok=True)

    full_path = target / f"{df_name}_{datetime_stamp}.parquet"
    df.to_parquet(full_path)
