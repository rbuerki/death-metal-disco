from sqlalchemy import INTEGER, REAL, TEXT, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
print(type(Base))


class Record(Base):
    __tablename__ = "records"
    record_id = Column("record_id", INTEGER, primary_key=True)
    artist_id = Column("artist_id", INTEGER, ForeignKey("artists.artist_id"))
    title = Column("title", TEXT, nullable=False)
    genre_id = Column("genre_id", INTEGER, ForeignKey("genres.genre_id"))
    label_id = Column("label", INTEGER, ForeignKey("labels.label_id"))
    year = Column("year", INTEGER)
    format_id = Column("format_id", INTEGER, ForeignKey("formats.format_id"))
    vinyl_color = Column("vinyl_color", TEXT)
    lim_edition = Column("lim_edition", TEXT)
    number = Column("number", TEXT)
    remarks = Column("remarks", TEXT)
    purchase_date = Column("purchase_date", TEXT, nullable=False)
    price = Column("price", REAL, nullable=False)
    digitized = Column("digitized", INTEGER, nullable=False)
    rating = Column("rating", INTEGER)
    active = Column("active", INTEGER, nullable=False)

    # Many-to-one relationships
    artist = relationship("Artist", back_populates="records")
    genre = relationship("Genre", back_populates="records")
    record_format = relationship("RecordFormat", back_populates="records")
    # Many-to-many Relationships
    labels = relationship(
        "Label", secondary="record_label_link", back_populates="records"
    )

    def __repr__(self):
        return (
            f"<Record(record_id={self.record_id} "
            f"title={self.title} "
            f"artist_id={self.artist_id})>"
        )


class Artist(Base):
    __tablename__ = "artists"
    artist_id = Column(INTEGER, primary_key=True)
    artist_name = Column(TEXT, nullable=False)
    artist_country = Column(TEXT)

    # Many-to-one relationships
    records = relationship("Record", back_populates="artist")
    # Many-to-many Relationships
    labels = relationship(
        "Label", secondary="artist_label_link", back_populates="artists"
    )
    genres = relationship(
        "Genre", secondary="artist_genre_link", back_populates="artists"
    )

    def __repr__(self):
        return (
            f"<Artist(artist_id={self.artist_id} "
            f"artist_name={self.artist_name})>"
        )


class Genre(Base):
    __tablename__ = "genres"
    genre_id = Column(INTEGER, primary_key=True)
    genre_name = Column(TEXT, nullable=False)

    # Many-to-one Relationships
    records = relationship("Record", back_populates="genre")
    # Many-to-many Relationships
    artists = relationship(
        "Artist", secondary="artist_genre_link", back_populates="genres"
    )
    labels = relationship(
        "Label", secondary="genre_label_link", back_populates="genres"
    )

    def __repr__(self):
        return (
            f"<Genre(genre_id={self.genre_id} "
            f"genre_name={self.genre_name})>"
        )


class Label(Base):
    __tablename__ = "labels"
    label_id = Column(INTEGER, primary_key=True)
    label_name = Column(TEXT, nullable=False)

    # Many-to-many Relationships
    artists = relationship(
        "Artist", secondary="artist_label_link", back_populates="labels"
    )
    genres = relationship(
        "Genre", secondary="genre_label_link", back_populates="labels"
    )
    records = relationship(
        "Record", secondary="record_label_link", back_populates="labels"
    )

    def __repr__(self):
        return (
            f"<Label(label_id={self.label_id} "
            f"label_name={self.label_name})>"
        )


class RecordFormat(Base):
    __tablename__ = "formats"
    format_id = Column(INTEGER, primary_key=True)
    format_name = Column(TEXT, nullable=False)

    # Many-to-one Relationships
    records = relationship("Record", back_populates="record_format")

    def __repr__(self):
        return (
            f"<RecordFormat(format_id={self.format_id} "
            f"format_name={self.format_name})>"
        )


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
