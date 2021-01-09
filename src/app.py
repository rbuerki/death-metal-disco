import datetime as dt
from pathlib import Path

import streamlit as st

import src.db_functions as db_functions
import src.utils as utils

st.set_page_config(
    page_title="DiscoBase",
    page_icon="🦇",
    layout="centered",
    initial_sidebar_state="auto",
)

CONFIG_PATH = Path.cwd() / "config.cfg"
path_to_db = utils.read_config_return_str(CONFIG_PATH, "SQLITE")
engine = utils.create_engine(path_to_db)
session = utils.create_session(engine)
# utils.create_DB_anew(engine, Base)

# TODO Depending on this I can show more or less of the others
trx_types = [
    "Purchase",
    "Deletion",
]

st.title("Death Metal Disco")

trx_type = st.selectbox("Transaction Type", trx_types)
st.write("---")
artist = st.text_input("Artist")
artist_country = st.text_input("(Artist) Country")
title = st.text_input("Title")
genre = st.text_input("Genre")
label = st.text_input("Label")
year = st.number_input("Year", value=dt.date.today().year, format="%d")
record_format = st.text_input("Format")
vinyl_color = st.text_input("Vinyl Color")
lim_edition = st.text_input("Lim Edition")
number = st.text_input("Number")
remarks = st.text_input("Remarks")
price = st.number_input(
    "Price", value=20.00, min_value=0.00, step=5.00, format="%f"
)
digitized = st.number_input(
    "Digitized", value=0, min_value=0, max_value=1, step=1, format="%i"
)
rating = st.text_input("Rating")
active = st.number_input(
    "Active", value=1, min_value=0, max_value=1, step=1, format="%d"
)
purchase_date = st.date_input("Purchase Date", value=dt.date.today())
credit_value = st.number_input(
    "Credits", value=1, min_value=0, max_value=1, step=1, format="%d"
)

# record_data_dict = None

save = st.checkbox("Save Record")
if save:

    record_data_dict = {
        "trx_type": trx_type,
        "artist": artist if artist != "" else None,
        "artist_country": artist_country if artist_country != "" else None,
        "title": title if title != "" else None,
        "genre": genre if genre != "" else None,
        "label": label if label != "" else None,
        "year": year,
        "record_format": record_format if record_format != "" else None,
        "vinyl_color": vinyl_color if vinyl_color != "" else None,
        "lim_edition": lim_edition if lim_edition != "" else None,
        "number": number if number != "" else None,
        "remarks": remarks if remarks != "" else None,
        "price": price,
        "digitized": digitized,
        "rating": rating if rating != "" else None,
        "active": active,
        "purchase_date": purchase_date,
        "credit_value": credit_value,
    }
    st.write(record_data_dict)

    # TODO Install validations

    if record_data_dict:

        insert = st.button("Insert Record")
        if insert and isinstance(record_data_dict, dict):
            db_functions.add_new_record(session, record_data_dict)
            st.write("Record inserted.")
            # TODO write actual credit score

# data_loaded = helpers.load_preprocessed_data("./data/preprocessed_results.csv")

# date_list = helpers.get_filter_options_for_due_date(data_loaded, 24)
# max_date = helpers.return_max_date_string(data_loaded)

# filter_due_date = st.sidebar.selectbox("Auswahl Stichdatum:", options=date_list)
# actual_date = helpers.return_actual_date_string(filter_due_date, max_date)

# data_truncated_head = helpers.truncate_data_to_actual_date(
#     data_loaded, actual_date
# )

# n_years = helpers.calculate_max_n_years_available(data_truncated_head)

# filter_result_dim = st.sidebar.selectbox(
#     "Auswahl Resultatsdimension:",
#     options=helpers.get_filter_options_for_result_dim(n_years),
# )

# data_truncated = helpers.truncate_data_n_years_back(
#     data_truncated_head, actual_date, n_years
# )

# data_prepared = helpers.prepare_values_according_to_result_dim(
#     data_truncated, filter_result_dim, actual_date
# )

# data_with_diff = helpers.calculate_diff_column(data_prepared)
# data_actual = helpers.create_df_with_actual_period_only(
#     data_with_diff, actual_date
# )


# # SIDEBAR FILTER OPTIONS

# mandant_options = helpers.get_filter_options_for_mandant_groups(data_actual)


# # SIDEBAR

# filter_mandant = st.sidebar.selectbox(
#     "Auswahl Mandanten-Gruppe:", options=mandant_options
# )
# filter_display_mode = st.sidebar.radio(
#     "Auswahl Gruppierung für Anzeige:", options=["nach KPI", "nach Entität"]
# )
# filter_product_dim = st.sidebar.radio(
#     "Auswahl Produktsicht:", options=["Produkt", "Kartenprofil"]
# )
# st.sidebar.markdown("---")
# st.sidebar.text("")
# st.sidebar.text(f"Datenstand:\n {max_date}")


# # UPPER FILTER OPTIONS MAIN PAGE

# # data = helpers.select_monthly_vs_ytd(data_actual, filter_result_dim)
# data = helpers.filter_for_sidebar_selections(
#     data_actual,
#     filter_display_mode=filter_display_mode,
#     filter_product_dim=filter_product_dim,
#     filter_mandant=filter_mandant,
# )


# # GENERATING OPTION FOR MAIN PAGE FILTERS

# entity_options = helpers.get_filter_options_for_entities(data, filter_mandant)
# kpi_options = helpers.get_filter_options_for_kpi(data)


# # MAIN PAGE FILTERS

# filter_entity = st.multiselect(
#     "Select entities:", options=entity_options, default=["[alle]"]
# )
# filter_kpi = st.multiselect(
#     "Select KPIs:", options=kpi_options, default=["[alle]"]
# )

# st.write("")


# # FILTERING DATA ACCORDING TO CHOICES

# data = helpers.filter_for_entity_and_kpi(
#     data,
#     filter_entity=filter_entity,
#     filter_kpi=filter_kpi,
#     filter_mandant=filter_mandant,
# )

# # DISPLAY AND STYLING OF DATAFRAMES

# if filter_display_mode.endswith("KPI"):
#     display_dict = helpers.create_dict_of_df_for_each_kpi(data)
#     for k, v in display_dict.items():
#         st.write(f"**{k}**")
#         v = helpers.arrange_for_display_per_kpi(
#             v, filter_product_dim, filter_mandant
#         )
#         # v.set_index("Entität", inplace=True)  # hack to get rid of the index TODO
#         st.table(
#             v.style.format({"Wert": "{:,.0f}", "Abw VJ": "{:0.1%}"}).applymap(
#                 helpers.set_bold_font,
#                 subset=pd.IndexSlice[v.index[v.index == 0], :],
#             )
#         )
# else:
#     display_dict = helpers.create_dict_of_df_for_each_entity(data)
#     for k, v in display_dict.items():
#         st.write(f"**{k}**")
#         v = helpers.arrange_for_display_per_entity(v)
#         # v.set_index("KPI", inplace=True)  # hack to get rid of the index TODO
#         st.table(v.style.format({"Wert": "{:,.0f}", "Abw VJ": "{:0.1%}"}))


# # DISPLAY STANDARD PLOT IF CONDITIONS ARE MET

# fig, df_plot = plots.main(data, data_truncated)
# if fig is not None:
#     st.plotly_chart(fig)


# # EXCEL EXPORT

# excel = st.button("Download Excel")

# if excel:
#     if fig is not None:
#         download_data = df_plot
#     else:
#         download_data = downloads.style_for_export_if_no_plot(
#             data, filter_display_mode
#         )

#     download_path = downloads.get_download_path()
#     b64, href = downloads.export_excel(download_data, download_path)
#     st.markdown(href, unsafe_allow_html=True)
