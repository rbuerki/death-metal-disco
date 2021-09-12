import streamlit as st
from datetime import date
from src.db_declaration import Record, RecordFormat
from src.apps.app_utils import record_format_list


def run(engine, Session):

    session = Session()

    max_date_default = date.today()
    min_date_default = (
        session.query(Record.purchase_date)
        .order_by(Record.purchase_date)
        .first()[0]
    )

    st.sidebar.write("---")
    choice = st.sidebar.radio(
        "Kind of records list:", ["all of them", "no rating", "not digitized",]
    )

    st.sidebar.write("\n\nDate Range:")
    max_date = st.sidebar.date_input("Max Date", value=max_date_default)
    min_date = st.sidebar.date_input("Min Date", value=min_date_default)

    large_format_only = st.sidebar.checkbox('Exklude 7" records and tapes')

    relevant_formats = record_format_list
    if large_format_only:
        sevens_and_tapes = ['7"', 'Pic-7"', "Tape"]
        relevant_formats = [
            fmt for fmt in record_format_list if fmt not in sevens_and_tapes
        ]

    if choice == "all of them":
        record_list = (
            session.query(Record)
            .filter(
                Record.is_active == 1,
                Record.purchase_date <= max_date,
                Record.purchase_date >= min_date,
                Record.record_format.has(
                    RecordFormat.format_name.in_(relevant_formats)
                ),
            )
            .order_by(Record.purchase_date.desc())
            .all()
        )
        st.write(
            f"\nFull List of {len(record_list)} Records, {str(max_date)} to {str(min_date)}\n"
        )
        for record in record_list:
            st.text(
                ", ".join(
                    [
                        str(record.purchase_date),
                        "/".join([x.artist_name for x in record.artists]),
                        record.title,
                        record.record_format.format_name,
                        f"Rating: {str(record.rating)}",
                        f"Digi: {str(record.is_digitized)}",
                    ]
                )
            )
    elif choice == "no rating":
        record_list = (
            session.query(Record)
            .filter(
                Record.is_active == 1,
                Record.purchase_date <= max_date,
                Record.purchase_date >= min_date,
                Record.rating == None,
                Record.record_format.has(
                    RecordFormat.format_name.in_(relevant_formats)
                ),
            )
            .order_by(Record.purchase_date.desc())
            .all()
        )
        st.write(
            f"\n{len(record_list)} Records not rated yet, {str(max_date)} to {str(min_date)}\n"
        )
        for record in record_list:
            st.text(
                ", ".join(
                    [
                        str(record.purchase_date),
                        "/".join([x.artist_name for x in record.artists]),
                        record.title,
                        record.record_format.format_name,
                    ]
                )
            )
    elif choice == "not digitized":
        record_list = (
            session.query(Record)
            .filter(
                Record.is_active == 1,
                Record.purchase_date <= max_date,
                Record.purchase_date >= min_date,
                Record.is_digitized == False,
                Record.record_format.has(
                    RecordFormat.format_name.in_(relevant_formats)
                ),
            )
            .order_by(Record.purchase_date.desc())
            .all()
        )
        st._transparent_write(
            f"\n{len(record_list)} Records not digitized yet, {str(max_date)} to {str(min_date)}\n"
        )
        for record in record_list:
            st.text(
                ", ".join(
                    [
                        str(record.purchase_date),
                        "/".join([x.artist_name for x in record.artists]),
                        record.title,
                        record.record_format.format_name,
                    ]
                )
            )

    session.close()
