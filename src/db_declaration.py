from sqlalchemy import Column, Date, ForeignKey, Float, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
print(type(Base))


class Record(Base):
    __tablename__ = "records"
    record_id = Column("record_id", Integer, primary_key=True)
    artist_id = Column("artist_id", Integer, ForeignKey("artists.artist_id"))
    title = Column("title", String, nullable=False)
    genre_id = Column("genre_id", Integer, ForeignKey("genres.genre_id"))
    label_id = Column("label", Integer, ForeignKey("labels.label_id"))
    year = Column("year", Integer)
    format_id = Column("format_id", Integer, ForeignKey("formats.format_id"))
    vinyl_color = Column("vinyl_color", String)
    lim_edition = Column("lim_edition", String)
    number = Column("number", String)
    remarks = Column("remarks", String)
    purchase_date = Column("purchase_date", Date, nullable=False)
    price = Column("price", Numeric, nullable=False)
    digitized = Column("digitized", Integer, nullable=False)
    rating = Column("rating", Integer)
    active = Column("active", Integer, nullable=False)

    # Many-to-one relationships
    artist = relationship("Artist", back_populates="records")
    genre = relationship("Genre", back_populates="records")
    record_format = relationship("RecordFormat", back_populates="records")
    # One-to-many relationships
    credit_trx = relationship("CreditTrx", back_populates="record")
    # Many-to-many relationships
    labels = relationship(
        "Label", secondary="record_label_link", back_populates="records"
    )

    def __repr__(self):
        return (
            f"<Record(record_id={self.record_id}, "
            f"title={self.title}, "
            f"artist_id={self.artist_id})>"
        )


class Artist(Base):
    __tablename__ = "artists"
    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String, nullable=False)
    artist_country = Column(String)

    # One-to-many relationships
    records = relationship("Record", back_populates="artist")
    # Many-to-many relationships
    labels = relationship(
        "Label", secondary="artist_label_link", back_populates="artists"
    )
    genres = relationship(
        "Genre", secondary="artist_genre_link", back_populates="artists"
    )

    def __repr__(self):
        return (
            f"<Artist(artist_id={self.artist_id}, "
            f"artist_name={self.artist_name})>"
        )


class Genre(Base):
    __tablename__ = "genres"
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String, nullable=False)

    # One-to-many relationships
    records = relationship("Record", back_populates="genre")
    # Many-to-many relationships
    artists = relationship(
        "Artist", secondary="artist_genre_link", back_populates="genres"
    )
    labels = relationship(
        "Label", secondary="genre_label_link", back_populates="genres"
    )

    def __repr__(self):
        return (
            f"<Genre(genre_id={self.genre_id}, "
            f"genre_name={self.genre_name})>"
        )


class Label(Base):
    __tablename__ = "labels"
    label_id = Column(Integer, primary_key=True)
    label_name = Column(String, nullable=False)

    # Many-to-many relationships
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
            f"<Label(label_id={self.label_id}, "
            f"label_name={self.label_name})>"
        )


class RecordFormat(Base):
    __tablename__ = "formats"
    format_id = Column(Integer, primary_key=True)
    format_name = Column(String, nullable=False)

    # One-to-many relationships
    records = relationship("Record", back_populates="record_format")

    def __repr__(self):
        return (
            f"<RecordFormat(format_id={self.format_id}, "
            f"format_name={self.format_name})>"
        )


class CreditTrx(Base):
    __tablename__ = "credit_trx"
    credit_trx_id = Column(Integer, primary_key=True)
    credit_trx_date = Column(Date, nullable=False)
    credit_trx_type = Column(String, nullable=False)
    credit_value = Column(Float, nullable=False)
    credit_saldo = Column(Float, nullable=False)  # TODO: Check calc on DB
    record_id = Column("record_id", Integer, ForeignKey("records.record_id"))

    # One-to-many relationships
    record = relationship("Record", back_populates="credit_trx")

    def __repr__(self):
        return (
            f"<CreditTrx(credit_trx_id={self.credit_trx_id}, "
            f"credit_trx_date={self.credit_trx_date}, "
            f"credit_trx_type={self.credit_trx_type}, "
            f"credit_value={self.credit_value}, "
            f"credit_saldo={self.credit_saldo}, "
            f"record_id={self.record_id})>"
        )


class RecordLabelLink(Base):
    __tablename__ = "record_label_link"
    record_id = Column(
        Integer, ForeignKey("records.record_id"), primary_key=True
    )
    label_id = Column(Integer, ForeignKey("labels.label_id"), primary_key=True)


class ArtistLabelLink(Base):
    __tablename__ = "artist_label_link"
    artist_id = Column(
        Integer, ForeignKey("artists.artist_id"), primary_key=True
    )
    label_id = Column(Integer, ForeignKey("labels.label_id"), primary_key=True)


class ArtistGenreLink(Base):
    __tablename__ = "artist_genre_link"
    artist_id = Column(
        Integer, ForeignKey("artists.artist_id"), primary_key=True
    )
    genre_id = Column(Integer, ForeignKey("genres.genre_id"), primary_key=True)


class GenreLabelLink(Base):
    __tablename__ = "genre_label_link"
    genre_id = Column(Integer, ForeignKey("genres.genre_id"), primary_key=True)
    label_id = Column(Integer, ForeignKey("labels.label_id"), primary_key=True)


# songs = Table(
#     "songs",
#     metadata,
#     Column("record_id", Integer, primary_key=True, auto_increment="auto"),
#     Column("song_title", String, nullable=False),
#     Column("danceability", Float),
#     Column("energy", Float),
#     Column("key", Integer),
#     Column("mode", Integer),
#     Column("instrumentalness", Float),
#     Column("valence", Float),
#     Column("tempo", Float),
#     Column("loudness", Float),
#     Column("duration_ms", Float),
# )
