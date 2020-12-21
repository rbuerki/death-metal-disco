from pathlib import Path
from typing import Union

import sqlalchemy
from sqlalchemy import FLOAT, INTEGER, REAL, TEXT, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.orm import backref, relationship

from src import utils

CONFIG_PATH = (Path(__file__).parent.parent / "config.cfg").absolute()


# DEFINE TABLES

Base = declarative_base()


class Album(Base):
    __tablename__ = "albums"
    album_id = Column("album_id", INTEGER, primary_key=True)
    artist_id = Column("artist_id", INTEGER, ForeignKey("artists.artist_id"))
    title = Column("title", TEXT, nullable=False)
    format_id = Column("format_id", INTEGER, ForeignKey("formats.format_id"))
    year = Column("year", INTEGER)
    genre_id = Column("genre_id", INTEGER, ForeignKey("genres.genre_id"))
    vinyl_color = Column("vinyl_color", TEXT)
    lim_edition = Column("lim_edition", TEXT)
    number = Column("number", INTEGER)
    label = Column("label", INTEGER, ForeignKey("labels.label_id"))
    remarks = Column("remarks", TEXT)
    purchase_date = Column("purchase_date", TEXT, nullable=False)
    price = Column("price", REAL, nullable=False)
    digitized = Column("digitized", INTEGER, nullable=False)
    rating = Column("rating", INTEGER)
    active = Column("active", INTEGER, nullable=False)
    credit = Column("credits", FLOAT, default=1)


class Artist(Base):
    __tablename__ = "artists"
    artist_id = Column(INTEGER, primary_key=True)
    artist_name = Column(TEXT, nullable=False)
    artist_country = Column(TEXT)
    # albums = relationship("Book", backref=backref("author"))
    # publishers = relationship(
    #     "Publisher", secondary=author_publisher, back_populates="authors"
    # )


class VinylFormat(Base):
    __tablename__ = "formats"
    format_id = Column(INTEGER, primary_key=True)
    format_name = Column(TEXT, nullable=False)


class Genre(Base):
    __tablename__ = "genres"
    genre_id = Column(INTEGER, primary_key=True)
    genre_name = Column(TEXT, nullable=False)


class Label(Base):
    __tablename__ = "labels"
    label_id = Column(INTEGER, primary_key=True)
    label_name = Column(TEXT, nullable=False)


# songs = Table(
#     "songs",
#     metadata,
#     Column("album_id", INTEGER, primary_key=True, auto_increment="auto"),
#     Column("song_title", TEXT, nullable=False),
#     Column("danceability", FLOAT),
#     Column("energy", FLOAT),
#     Column("key", INTEGER),
#     Column("mode", INTEGER),
#     Column("instrumentalness", FLOAT),
#     Column("valence", FLOAT),
#     Column("tempo", FLOAT),
#     Column("loudness", FLOAT),
#     Column("duration_ms", FLOAT),
# )


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
    Base.metadata.drop_all(engine, checkfirst=False)
    Base.metadata.create_all(engine)


if __name__ == main():
    main()
