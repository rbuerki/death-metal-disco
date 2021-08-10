import streamlit as st
from datetime import date
from src.db_declaration import Record
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
        "Kind of record list:", ["all of them", "no rating", "not digitized",]
    )

    st.sidebar.write("\n\nDate Range:")
    max_date = st.sidebar.date_input("Max Date", value=max_date_default)
    min_date = st.sidebar.date_input("Min Date", value=min_date_default)

    large_format_only = st.sidebar.checkbox('Exklude 7" records and tapes')

    if large_format_only:
        sevens_and_tapes = ['7"', 'Pic-7"', "Tape"]
        large_format_list = [
            fmt for fmt in record_format_list if fmt not in sevens_and_tapes
        ]
        # TODO inlcude in statements if param is set

    if choice == "all of them":
        record_list = (
            session.query(Record)
            .filter(
                Record.is_active == 1,
                Record.purchase_date <= max_date,
                Record.purchase_date >= min_date,
            )
            .order_by(Record.purchase_date.desc())
            .all()
        )
        st.write(f"\nFull Record List, {str(max_date)} to {str(min_date)}\n")
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
            )
            .order_by(Record.purchase_date.desc())
            .all()
        )
        st.write(
            f"\nRecords not rated yet, {str(max_date)} to {str(min_date)}\n"
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
            )
            .order_by(Record.purchase_date.desc())
            .all()
        )
        st._transparent_write(
            f"\nRecords not digitized yet, {str(max_date)} to {str(min_date)}\n"
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
