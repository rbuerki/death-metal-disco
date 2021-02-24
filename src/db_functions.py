import datetime as dt
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
import sqlalchemy

from src import db_connect
from src.db_declaration import (
    Artist,
    Genre,
    Label,
    Record,
    RecordFormat,
    CreditTrx,
)


def fetch_a_record_from_the_shelf(
    session: sqlalchemy.orm.session.Session,
    artist: Union[str, Sequence[str]],
    title: str,
) -> Optional[Record]:
    """Query a record by title, artist and (optional) year,
    Return the query result object. Returns None if no record is
    found, raises an error if more than one record is matched.

    NOTE / TODO: Checks for first artist only in case of splits.
    """
    if isinstance(artist, str):
        artist = [a.strip() for a in artist.split(";")]

    record = (
        session.query(Record)
        .filter(
            (Record.title.ilike(title)),
            (Record.artists.any(Artist.artist_name.ilike(artist[0]))),
        )
        .one_or_none()
    )
    return record


def create_record_from_record_data(
    session: sqlalchemy.orm.session.Session, record_data: Dict[str, Any]
) -> Record:
    """Use the information in the passed record_data dict
    to instantiate and return a new Record object.
    """
    record = Record(
        title=record_data["title"],
        year=record_data["year"],
        vinyl_color=record_data["vinyl_color"],
        lim_edition=record_data["lim_edition"],
        number=record_data["number"],
        remarks=record_data["remarks"],
        purchase_date=record_data["purchase_date"],
        price=record_data["price"],
        rating=record_data["rating"],
        is_digitized=record_data["is_digitized"],
        is_active=record_data["is_active"],
    )
    return record


def check_if_artist_exists_or_create(
    session: sqlalchemy.orm.session.Session,
    r_artist: Sequence[str],
    r_artist_country: Sequence[str],
) -> List[Artist]:
    """For every artist name in the passed list, check if an
    Artist object of same name already exists, if not instantiate
    it. In any case append the Artist instance to the returned
    list `artist_list` (will be used to update the relationships).
    """
    artist_list = []
    for n, a in enumerate(r_artist):
        artist = (
            session.query(Artist)
            .filter(Artist.artist_name.ilike(a))
            .one_or_none()
        )
        if artist is None:
            artist = Artist(artist_name=a, artist_country=r_artist_country[n],)
            session.add(artist)

        artist_list.append(artist)
    return artist_list


def check_if_label_exists_or_create(
    session: sqlalchemy.orm.session.Session, r_label: Sequence[str],
) -> List[Label]:
    """For every label name in the passed list, check if a
    Label object of same name already exists, if not instantiate
    it. In any case append the Label instance to the returned
    list `label_list` (will be used to update the relationships).
    """
    label_list = []
    for lab in r_label:
        label = (
            session.query(Label)
            .filter(Label.label_name.ilike(lab))
            .one_or_none()
        )
        if label is None:
            label = Label(label_name=lab)
            session.add(label)

        label_list.append(label)
    return label_list


def check_if_format_exists_or_create(
    session: sqlalchemy.orm.session.Session, r_format: str,
) -> RecordFormat:
    """Check if a RecordFormat format object of same name already
    exists, if not instantiate it. In any case return the
    RecordFormat instance (will be used to update the
    relationships).
    """
    record_format = (
        session.query(RecordFormat)
        .filter(RecordFormat.format_name.ilike(r_format))
        .one_or_none()
    )
    if record_format is None:
        record_format = RecordFormat(format_name=r_format)
        session.add(record_format)
    return record_format


def check_if_genre_exists_or_create(
    session: sqlalchemy.orm.session.Session, r_genre: str,
) -> Genre:
    """Check if a RecordFormat format object of same name already
    exists, if not instantiate it. In any case return the
    RecordFormat instance (will be used to update the
    relationships).
    """
    genre = (
        session.query(Genre)
        .filter(Genre.genre_name.ilike(r_genre))
        .one_or_none()
    )
    if genre is None:
        genre = Genre(genre_name=r_genre)
        session.add(genre)
    return genre


def create_a_purchase_trx(
    session: sqlalchemy.orm.session.Session, record_data: Dict[str, Any]
) -> CreditTrx:
    """Create and return a CreditTrx instance of type "Purchase" in
    the DB based on the information in `record_data`.
    """
    credit_value = record_data["credit_value"] * -1
    try:
        credit_saldo = (
            session.query(CreditTrx.credit_saldo)
            .order_by(CreditTrx.credit_trx_id)
            .all()[-1][0]
        )
    except IndexError:
        # This is in case of initial data_ingestion only
        credit_saldo = 0

    credit_trx = CreditTrx(
        credit_trx_date=record_data["purchase_date"],
        credit_trx_type=record_data["trx_type"],
        credit_value=credit_value,
        credit_saldo=(credit_saldo + credit_value),
    )
    return credit_trx


def create_a_removal_trx(
    session: sqlalchemy.orm.session.Session, record_data: Dict[str, Any]
) -> CreditTrx:
    """Create and return a CreditTrx instance of type "Removal" in
    the DB based on the information in `record_data`.
    """
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
    return credit_trx


def initialize_record_relationships(
    session: sqlalchemy.orm.session.Session,
    record: Record,
    artist_list: List[Artist],
    label_list: List[Label],
    record_format: RecordFormat,
    genre: Genre,
    credit_trx: Union[CreditTrx, None],
):
    """Initialize the record relationships. This is straightforward
    for the one-to-many and many-to-one relationships. For the
    many-to-many we make sure not only to append to but to
    overwrite all existing relationships. (Because we pass a full
    list and not a diff list and want faulty relationships to
    be removed.)
    """
    record.record_format = record_format
    record.genre = genre
    if credit_trx is not None:
        record.credit_trx.append(credit_trx)

    record.artists = []
    for artist in artist_list:
        record.artists.append(artist)
        artist.genres.append(genre)
        for label in label_list:
            artist.labels.append(label)

    record.labels = []
    for label in label_list:
        record.labels.append(label)
        genre.labels.append(label)


def add_new_record(
    session: sqlalchemy.orm.session.Session, record_data: Dict[str, Any]
):
    """Add a new record to the DB. The record data is passed as
    a dictionary. This function can be applied during batch
    uploads (initial data ingestion) or for adding singe new
    records later on.
    """
    assert record_data["trx_type"] == "Purchase" or "Initial Load"

    r_artist: Sequence[str] = record_data["artist"]
    r_artist_country: Sequence[str] = record_data["artist_country"]
    r_label: Sequence[str] = record_data["label"]
    r_format: str = record_data["record_format"]
    r_genre: str = record_data["genre"]
    r_title: str = record_data["title"]

    # Check if record already exists
    record = fetch_a_record_from_the_shelf(session, r_artist, r_title)
    if record is not None:
        print(
            f"Record '{r_title}' by {r_artist} already exists, insert skipped."
        )
        return None

    if record is None:
        record = create_record_from_record_data(session, record_data)
        artist_list = check_if_artist_exists_or_create(
            session, r_artist, r_artist_country
        )
        label_list = check_if_label_exists_or_create(session, r_label)
        record_format = check_if_format_exists_or_create(session, r_format)
        genre = check_if_genre_exists_or_create(session, r_genre)
        credit_trx = create_a_purchase_trx(session, record_data)
        initialize_record_relationships(
            session,
            record,
            artist_list,
            label_list,
            record_format,
            genre,
            credit_trx,
        )

    session.add(record)
    session.commit()


def update_record(
    session: sqlalchemy.orm.session.Session, record_data: Dict[str, Any]
):
    """Update the properties of an existing record in the DB.
    The record data is passed as a dictionary and data that
    has changed will be updated to the new values. Except of that
    most of the steps in the process are shared with `add_new_record`.
    """
    assert record_data["trx_type"] == "Update"

    r_artist: Sequence[str] = record_data["artist"]
    r_artist_country: Sequence[str] = record_data["artist_country"]
    r_label: Sequence[str] = record_data["label"]
    r_format: str = record_data["record_format"]
    r_genre: str = record_data["genre"]
    r_title: str = record_data["title"]

    # Check if record already exists
    record = fetch_a_record_from_the_shelf(session, r_artist, r_title)

    if record is None:
        print(
            f"Record '{r_title}' by {r_artist} not found in DB, cannot update."
        )
        return None

    if record is not None:
        record.title = record_data["title"]
        record.year = record_data["year"]
        record.vinyl_color = record_data["vinyl_color"]
        record.lim_edition = record_data["lim_edition"]
        record.number = record_data["number"]
        record.remarks = record_data["remarks"]
        record.purchase_date = record_data["purchase_date"]
        record.price = record_data["price"]
        record.is_digitized = record_data["is_digitized"]
        record.rating = record_data["rating"]
        record.is_active = record_data["is_active"]

        artist_list = check_if_artist_exists_or_create(
            session, r_artist, r_artist_country
        )
        label_list = check_if_label_exists_or_create(session, r_label)
        record_format = check_if_format_exists_or_create(session, r_format)
        genre = check_if_genre_exists_or_create(session, r_genre)
        # TODO For reactivations I could charge a Credit Trx
        credit_trx = None
        initialize_record_relationships(
            session,
            record,
            artist_list,
            label_list,
            record_format,
            genre,
            credit_trx,
        )

    session.add(record)
    session.commit()


def set_record_to_inactive(
    session: sqlalchemy.orm.session.Session, record_data: Dict
):
    """Set a the status of a record to inactive. This is equivalent
    to a removal, because records are never fully deleted. This also
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
        return None

    if record is not None:
        if record.is_active == False:
            print(
                f"Status of record '{r_title}' by {r_artist} is "
                f"already 0, please check."
            )
            return None

        else:
            record.is_active = False
            print("Record set to inactive.")
            credit_trx = create_a_removal_trx(session, record_data)
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

    record_df_tuple = _load_record_related_data_to_df(session)
    credit_trx_df_tuple = _load_credit_trx_table_to_df(engine)

    for df_tuple in [record_df_tuple, credit_trx_df_tuple]:
        _save_df_to_parquet(df_tuple, config_path)


def _load_record_related_data_to_df(
    session: sqlalchemy.orm.session.Session, include_id_column: bool = True
) -> Tuple[str, pd.DataFrame]:
    """Save all record-related data to Pandas Dataframe and return a
    tuple with a dataframe name string and the dataframe. Called
    within `export_db_data_to_2_parquet_files`, but also used for
    displaying a full collection dataframe in the the frontend's
    `recs_app`. Note: If `include_id_column` is actively set to
    False the id will be (re-)defined during the reset of the DB.
    (ATTENTION - dangerous, might break relations to trx data.)
    """
    result_list = session.query(Record).order_by(Record.record_id).all()
    dict_list = []

    for result in result_list:
        record_data_dict = {
            "record_id": result.record_id,
            "artist": [artist.artist_name for artist in result.artists],
            "artist_country": [
                artist.artist_country for artist in result.artists
            ],
            "title": result.title,
            "genre": result.genre.genre_name,
            "label": [label.label_name for label in result.labels],
            "year": result.year,
            "record_format": result.record_format.format_name,
            "vinyl_color": result.vinyl_color,
            "lim_edition": result.lim_edition,
            "number": result.number,
            "remarks": result.remarks,
            "purchase_date": result.purchase_date,
            "price": result.price,
            "rating": result.rating,  # TODO: has to be atapted to one-to-many
            "is_digitized": result.is_digitized,
            "is_active": result.is_active,
        }
        dict_list.append(record_data_dict)

    records_df = pd.DataFrame(dict_list, columns=dict_list[0].keys())
    if include_id_column is False:
        records_df.set_index("record_id", drop=True, inplace=True)
    df_name = "record_data"

    records_df = records_df.replace("None", np.nan)
    for col in ["is_digitized", "is_active"]:
        records_df[col] = records_df[col].astype(bool)
    for col in ["rating", "price"]:
        records_df[col] = records_df[col].astype(float)
    records_df["purchase_date"] = records_df["purchase_date"].astype(
        "datetime64"
    )

    if (
        not records_df.index.is_monotonic_increasing
        and not records_df.index.is_unique
    ):
        raise AssertionError("record_ids are messed up, please check data.")

    return df_name, records_df


def _load_credit_trx_table_to_df(
    engine: sqlalchemy.engine.Engine, include_id_column: bool = True
) -> Tuple[str, pd.DataFrame]:
    """Copy credit_trx_table to Pandas Dataframe and return a tuple
    with a dataframe name string and the dataframe. Called within
    `export_db_data_to_2_parquet_files`. Note: If `include_id_column`
    is actively set to False the id will be (re-)defined during the
    reset of the DB. (ATTENTION - dangerous, might break relations to
    record data.)
    """
    credit_trx_df = pd.read_sql("credit_trx", engine)
    if include_id_column is False:
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
    datetime_stamp = dt.datetime.strftime(
        dt.datetime.now(), "%Y-%m-%d-%H-%M-%S"
    )

    back_up_params = db_connect.read_yaml(config_path, "BACK_UP")
    rel_path = back_up_params["REL_PATH"]
    target_folder = Path.cwd() / rel_path
    Path.mkdir(target_folder, parents=True, exist_ok=True)
    full_path = target_folder / f"{df_name}_{datetime_stamp}.parquet"
    print(f"Saving data to: {full_path}")

    df.to_parquet(full_path)


# RESET AND IMPORT DATA


def reset_db_with_backup_data(
    engine: sqlalchemy.engine.Engine,
    session: sqlalchemy.orm.session.Session,
    Base,  #: sqlalchemy.ext.declarative.AbstractConcreteBase,
    config_path: Union[Path, str],
    record_data_file: Union[Path, str],
    trx_data_file: Union[Path, str],
):
    """Drop and re-create the DB (losing all existing data in it)
    and repopulate it with backup-data from two parquet files.
    """
    record_data, trx_data = _load_backup_data_from_parquet(
        config_path, record_data_file, trx_data_file
    )
    _drop_and_reset_DB(engine, Base)
    _insert_record_data_with_sqlalchemy_orm(session, record_data)
    _truncate_credit_trx_table(engine, CreditTrx)
    _insert_trx_data_with_sqlalchemy_core(engine, trx_data, CreditTrx)
    print("Reset successful!")


def _load_backup_data_from_parquet(
    config_path: Union[Path, str],
    record_data_file: Union[Path, str],
    trx_data_file: Union[Path, str],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load the two back-up files with the record-related and
    the credit_trx data into Pandas DataFrames. Pass the file
    names only, the full path to the back-up folder defined
    with help of the config file "BACK_UP" parameters.
    (Called within `reset_db_with_backup_data`.)
    """

    back_up_params = db_connect.read_yaml(config_path, "BACK_UP")
    rel_path = back_up_params["REL_PATH"]
    target_folder = Path.cwd() / rel_path

    df_list = []
    for file in [record_data_file, trx_data_file]:
        full_path = target_folder / file

        df = pd.read_parquet(full_path)
        df_list.append(df)

    return df_list[0], df_list[1]


def _drop_and_reset_DB(
    engine: sqlalchemy.engine.Engine,
    Base,  #: sqlalchemy.ext.declarative.AbstractConcreteBase,
):
    """Drop all existing tables from the database
    and create them anew. WARNING - ALL DATA LOST!
    (Called within `reset_db_with_backup_data`.)
    """
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine)


def _insert_record_data_with_sqlalchemy_orm(
    session: sqlalchemy.orm.session.Session, record_data: pd.DataFrame
):
    """Import the record related data using the regular `add_record`
    function. (This populates the recrods, artists, genres, record_formats,
    and labels tables.) - That's why we first have to add trx values,
    even if we will then delete these again in the next step.
    (Called within `reset_db_with_backup_data`.)
    """
    # Add bogus trx values
    record_data["credit_value"] = 0
    record_data["trx_type"] = "Initial Load"

    for x in record_data.to_dict("records"):
        add_new_record(session, x)


def _truncate_credit_trx_table(
    engine: sqlalchemy.engine.Engine,
    Base,  #: sqlalchemy.ext.declarative.AbstractConcreteBase,
    table_class: sqlalchemy.ext.declarative.api.DeclarativeMeta = CreditTrx,
):
    """Workaround for truncating the credit_trx table to get rid of
    the entries that where created during the data import.
    (Called within `reset_db_with_backup_data`.)

    Note: Just deleting the table content with table.delete() will
    not reset the autoincrement of the primary key, that's why we
    have to drop and re-create the table.
    """
    Base.metadata.drop_all(engine, tables=[table_class.__table__])
    Base.metadata.create_all(engine, tables=[table_class.__table__])


def _insert_trx_data_with_sqlalchemy_core(
    engine: sqlalchemy.engine.Engine,
    trx_data: pd.DataFrame,
    table_class: sqlalchemy.ext.declarative.api.DeclarativeMeta = CreditTrx,
):
    """Copy the original trx_data into the empty credit_trx table
    using the speedy 'bulk' insert function from sqlalchemy's core
    functionality. (Called within `reset_db_with_backup_data`.)
    """
    trx_data.drop(["created_at", "updated_at"], axis=1, inplace=True)
    engine.execute(
        table_class.__table__.insert(), [x for x in trx_data.to_dict("records")]
    )
