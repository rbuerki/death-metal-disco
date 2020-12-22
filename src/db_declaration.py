from sqlalchemy import INTEGER, REAL, TEXT, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship


Base = declarative_base()
print(type(Base))


class Record(Base):
    __tablename__ = "records"
    record_id = Column("record_id", INTEGER, primary_key=True)
    artist_id = Column("artist_id", INTEGER, ForeignKey("artists.artist_id"))
    title = Column("title", TEXT, nullable=False)
    genre_id = Column("genre_id", INTEGER, ForeignKey("genres.genre_id"))
    label = Column("label", INTEGER, ForeignKey("labels.label_id"))
    year = Column("year", INTEGER)
    format_id = Column("format_id", INTEGER, ForeignKey("formats.format_id"))
    vinyl_color = Column("vinyl_color", TEXT)
    lim_edition = Column("lim_edition", TEXT)
    number = Column("number", INTEGER)
    remarks = Column("remarks", TEXT)
    purchase_date = Column("purchase_date", TEXT, nullable=False)
    price = Column("price", REAL, nullable=False)
    digitized = Column("digitized", INTEGER, nullable=False)
    rating = Column("rating", INTEGER)
    active = Column("active", INTEGER, nullable=False)
    # Relationships
    labels = relationship(
        "Label", secondary="record_label_link", back_populates="records"
    )


class Artist(Base):
    __tablename__ = "artists"
    artist_id = Column(INTEGER, primary_key=True)
    artist_name = Column(TEXT, nullable=False)
    artist_country = Column(TEXT)
    # Relationships
    records = relationship("Record", backref=backref("artist"), uselist=True)
    labels = relationship(
        "Label", secondary="artist_label_link", back_populates="artists"
    )
    genres = relationship(
        "Genre", secondary="artist_genre_link", back_populates="artists"
    )


class Genre(Base):
    __tablename__ = "genres"
    genre_id = Column(INTEGER, primary_key=True)
    genre_name = Column(TEXT, nullable=False)
    # Relationships
    records = relationship("Record", backref=backref("genre"), uselist=True)
    artists = relationship(
        "Artist", secondary="artist_genre_link", back_populates="genres"
    )
    labels = relationship(
        "Label", secondary="genre_label_link", back_populates="genres"
    )


class Label(Base):
    __tablename__ = "labels"
    label_id = Column(INTEGER, primary_key=True)
    label_name = Column(TEXT, nullable=False)
    # Relationships
    artists = relationship(
        "Artist", secondary="artist_label_link", back_populates="labels"
    )
    genres = relationship(
        "Genre", secondary="genre_label_link", back_populates="labels"
    )
    records = relationship(
        "Record", secondary="record_label_link", back_populates="labels"
    )


class VinylFormat(Base):
    __tablename__ = "formats"
    format_id = Column(INTEGER, primary_key=True)
    format_name = Column(TEXT, nullable=False)
    # Relationships
    records = relationship("Record", backref=backref("format"), uselist=True)


class RecordLabelLink(Base):
    __tablename__ = "record_label_link"
    record_id = Column(
        INTEGER, ForeignKey("records.record_id"), primary_key=True
    )
    label_id = Column(INTEGER, ForeignKey("labels.label_id"), primary_key=True)


class ArtistLabelLink(Base):
    __tablename__ = "artist_label_link"
    artist_id = Column(
        INTEGER, ForeignKey("artists.artist_id"), primary_key=True
    )
    label_id = Column(INTEGER, ForeignKey("labels.label_id"), primary_key=True)


class ArtistGenreLink(Base):
    __tablename__ = "artist_genre_link"
    artist_id = Column(
        INTEGER, ForeignKey("artists.artist_id"), primary_key=True
    )
    genre_id = Column(INTEGER, ForeignKey("genres.genre_id"), primary_key=True)


class GenreLabelLink(Base):
    __tablename__ = "genre_label_link"
    genre_id = Column(INTEGER, ForeignKey("genres.genre_id"), primary_key=True)
    label_id = Column(INTEGER, ForeignKey("labels.label_id"), primary_key=True)


# songs = Table(
#     "songs",
#     metadata,
#     Column("record_id", INTEGER, primary_key=True, auto_increment="auto"),
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
