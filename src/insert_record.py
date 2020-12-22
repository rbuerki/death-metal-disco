import collections
from pathlib import Path
from typing import Union

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from src.db_declaration import (
    Artist,
    Genre,
    Label,
    Record,
    VinylFormat,
)
from src import utils


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


def add_new_record(session, record_data: RecordData):  # TODO
    """Add a new record to the DB."""

    r_artist = record_data.artist  # TODO Id or name in table???
    r_title = record_data.title
    r_format = record_data.format  # TODO
    r_genre = record_data.genre  # TODO
    r_label = record_data.label
    # Check if record already exists
    record = (
        session.query(Record)
        .join(Artist)
        .filter(
            (Record.title == r_title),  # TODO lower ... cannot call directly
            # (Record.labels.any(Label.label_name == r_label)),
            # (Artist.artist_name == r_artist),
        )
        .one_or_none()
    )
    # Does the book by the author and publisher already exist?
    if record is not None:
        print("Record is already existing.")
        return

    # # Get the record by the artist
    # record = (
    #     session.query(Record)
    #     .join(Artist)
    #     .filter(
    #         (Record.title.lower() == r_title.lower()),
    #         (Record.labels.any(Label.label_name == r_label)),
    #         (Artist.artist_name == r_artist),
    #     )
    #     .one_or_none()
    # )

    # Create the new record if needed
    if record is None:
        record = Record(
            title=record_data.title,
            year=record_data.year,
            vinyl_color=record_data.vinyl_color,
            lim_edition=record_data.lim_edition,
            number=record_data.number,
            remarks=record_data.remarks,
            purchase_date=record_data.purchase_date,
            price=record_data.price,
            digitized=record_data.digitized,
            rating=record_data.rating,
            active=record_data.active,
        )

    # Get the artist
    artist = (
        session.query(Artist)
        .filter(Artist.artist_name == r_artist)
        .one_or_none()
    )
    # Do we need to create the artist?
    if artist is None:
        artist = Artist(artist_name=r_artist, artist_country=None)
        session.add(artist)

    # Get the format
    vinyl_format = (
        session.query(VinylFormat)
        .filter(VinylFormat.format_name == r_format)
        .one_or_none()
    )
    # Do we need to create the format?
    if vinyl_format is None:
        vinyl_format = VinylFormat(format_name=r_format)
        session.add(vinyl_format)

    # Get the genre
    genre = (
        session.query(Genre).filter(Genre.genre_name == r_genre).one_or_none()
    )
    # Do we need to create the genre?
    if genre is None:
        genre = Genre(genre_name=r_genre)
        session.add(genre)

    # Get the label
    label = (
        session.query(Label).filter(Label.label_name == r_label).one_or_none()
    )
    # Do we need to create the label?
    if label is None:
        label = Label(label_name=r_label)
        session.add(label)

    # Initialize the book relationships
    record.artist = artist
    record.genre = genre
    record.format = vinyl_format
    record.genre = genre
    record.labels.append(label)

    session.add(record)

    # Commit to the database
    session.commit()


def connect_to_db(rel_path: Union[Path, str]) -> sqlalchemy.engine.Engine:
    """Connect to SQLite DB using a relative path from root."""
    full_path = Path.cwd() / rel_path
    print(full_path)
    conn_str = f"sqlite:///{full_path}"
    engine = sqlalchemy.create_engine(conn_str)
    return engine


def main():
    rel_path = utils.read_config_return_str(CONFIG_PATH, "SQLITE")
    engine = connect_to_db(rel_path)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # session = sessionmaker().configure(bind=engine)
    add_new_record(
        session, TEST_DATA
    )  # TODO I can add.all(), see tutorial sqlalchemy
    session.close()


if __name__ == main():
    main()
