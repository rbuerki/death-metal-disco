# CREATE TABLE STATEMENTS

create_albums = """
    CREATE TABLE IF NOT EXISTS albums(
        album_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Artist TEXT NOT NULL,
        Album TEXT NOT NULL,
        Format TEXT NOT NULL,
        Year INTEGER,
        Genre TEXT NOT NULL,
        Vinyl_Color TEXT,
        Lim_Edition TEXT,
        Number INTEGER,
        Label TEXT,
        Remarks TEXT,
        Purchase_Date TEXT NOT NULL,
        Price NUMERIC (5, 2) NOT NULL,  -- could use MONEY too
        Digitized INTEGER NOT NULL,
        Rating INTEGER,
        Active INTEGER NOT NULL,
        Credits FLOAT
    );
    """


# DROP TABLE STATMENTS

drop_staging_album = "DROP TABLE IF EXISTS albums;"


# INSERT STATMENTS

insert_album = """
    INSERT INTO albums (
        Artist,
        Album,
        Format,
        Year,
        Genre,
        Vinyl_Color,
        Lim_Edition,
        Number,
        Label,
        Remarks,
        Purchase_Date,
        Price,
        Digitized,
        Rating,
        Alive,
        Credits,
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    );
    """


# CREATE TABLES

# Postgres' SERIAL command is not supported in Redshift. The equivalent is IDENTITY(0,1)
# Read more here: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_TABLE_NEW.html

# # Staging Tables

# create_staging_NonMotCount = (
#     """
#     CREATE TABLE IF NOT EXISTS staging_NonMotCount(
#         fk_zaehler VARCHAR(20),
#         fk_standort SMALLINT,
#         datum TIMESTAMP SORTKEY DISTKEY,
#         velo_in SMALLINT,
#         velo_out SMALLINT,
#         fuss_in SMALLINT,
#         fuss_out SMALLINT,
#         ost INT,
#         nord INT
#     )
#     DISTSTYLE KEY
#     """
# )

# create_staging_NonMotLocation = (
#     """
#     CREATE TABLE IF NOT EXISTS staging_NonMotLocation(
#         abkuerzung CHAR(8),
#         bezeichnung VARCHAR(50),
#         bis TIMESTAMP,
#         fk_zaehler VARCHAR(20),
#         id1 SMALLINT,
#         richtung_in VARCHAR(50),
#         richtung_out VARCHAR(50),
#         von TIMESTAMP,
#         objectid SMALLINT,
#         korrekturfaktor FLOAT,
#         long FLOAT,
#         lat FLOAT
#     )
#     DISTSTYLE ALL
#     """
# )

# create_staging_weather = (
#     """
#     CREATE TABLE IF NOT EXISTS staging_weather(
#         datetime_cet TIMESTAMP SORTKEY,
#         air_temperature FLOAT,
#         humidity SMALLINT,
#         wind_gust_max_10min FLOAT,
#         wind_speed_avg_10min FLOAT,
#         wind_force_avg_10min SMALLINT,
#         wind_direction SMALLINT,
#         windchill FLOAT,
#         barometric_pressure_qfe FLOAT,
#         dew_point FLOAT
#     )
#     DISTSTYLE AUTO
#     """
# )

# # Dim Tables

# create_dim_location = (
#     """
#     CREATE TABLE IF NOT EXISTS dim_location(
#         location_key INT IDENTITY(0,1) PRIMARY KEY, -- counts_id SERIAL PRIMARY KEY,
#         location_id SMALLINT NOT NULL,
#         location_name VARCHAR(50) NOT NULL,
#         location_code VARCHAR(8) NOT NULL,
#         count_type CHAR(3) NOT NULL,
#         lat FLOAT NOT NULL,
#         long FLOAT NOT NULL,
#         active_from DATE NOT NULL,
#         active_to DATE
#         -- still_active BOOLEAN NOT NULL
#     )
#     DISTSTYLE ALL
#     """
# )

# create_dim_date = (
#     """
#     CREATE TABLE IF NOT EXISTS dim_date(
#         date_key INT PRIMARY KEY SORTKEY,
#         date DATE NOT NULL,
#         year SMALLINT NOT NULL,
#         quarter SMALLINT NOT NULL,
#         month SMALLINT NOT NULL,
#         month_name  VARCHAR(9) NOT NULL,
#         week_of_year SMALLINT NOT NULL,
#         day_of_year SMALLINT NOT NULL,
#         day_of_quarter SMALLINT NOT NULL,
#         day_of_month SMALLINT NOT NULL,
#         day_of_week SMALLINT NOT NULL,
#         day_name VARCHAR(9) NOT NULL,
#         is_weekend BOOLEAN NOT NULL,
#         is_holiday BOOLEAN NOT NULL,
#         first_day_of_week DATE NOT NULL,
#         last_day_of_week DATE NOT NULL,
#         first_day_of_month DATE NOT NULL,
#         last_day_of_month DATE NOT NULL,
#         first_day_of_quarter DATE NOT NULL,
#         last_day_of_quarter DATE NOT NULL,
#         first_day_of_year DATE NOT NULL,
#         last_day_of_year DATE NOT NULL
#     )
#     DISTSTYLE AUTO
#     """
# )

# create_dim_time = (
#     """
#     CREATE TABLE IF NOT EXISTS dim_time(
#         time_key INT PRIMARY KEY SORTKEY,
#         time_of_day CHAR(5) NOT NULL,
#         hour SMALLINT NOT NULL,
#         half_hour CHAR(13) NOT NULL,
#         quarter_hour CHAR(13) NOT NULL,
#         minute SMALLINT NOT NULL
#     )
#     DISTSTYLE ALL
#     """
# )

# # Fact Tables

# create_fact_count = (
#     """
#     CREATE TABLE IF NOT EXISTS fact_count(
#         counts_id INT IDENTITY(0,1) PRIMARY KEY, -- counts_id SERIAL PRIMARY KEY,
#         date_key INT REFERENCES dim_date (date_key) SORTKEY DISTKEY,
#         time_key INT REFERENCES dim_time (time_key),
#         location_key SMALLINT REFERENCES dim_location (location_key),
#         count_type CHAR(1),
#         count_total SMALLINT,
#         count_in SMALLINT,
#         count_out SMALLINT
#     )
#     DISTSTYLE KEY
#     """
# )

# create_fact_weather = (
#     """
#     CREATE TABLE IF NOT EXISTS fact_weather(
#         weather_id INT IDENTITY(0,1) PRIMARY KEY,
#         date_key INT REFERENCES dim_date (date_key) SORTKEY,
#         time_key INT REFERENCES dim_time (time_key),
#         air_temperature FLOAT,
#         humidity SMALLINT,
#         wind_gust_max FLOAT,
#         wind_speed_avg FLOAT,
#         wind_force_avg SMALLINT,
#         wind_direction SMALLINT,
#         windchill FLOAT,
#         barometric_pressure_qfe FLOAT,
#         dew_point FLOAT
#     )
#     DISTSTYLE AUTO
#     """
# )

# COPY INTO STAGING TABLES

# copy_staging_NonMotLocation = (
#     f"""
#     COPY staging_NonMotLocation
#     FROM {NON_MOT_LOC_DATA}
#     CREDENTIALS 'aws_access_key_id={KEY};aws_secret_access_key={SECRET}'
#     DELIMITER ','
#     TIMEFORMAT 'YYYY-MM-DD HH:MI:SS'
#     TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
#     REGION 'eu-west-1';
#     """
# )

# INSERT INTO FINAL TABLES
# Note: I use DISTINCT statement to handle possible duplicates

# insert_fact_count = (
#     """
#     INSERT INTO fact_count(
#         date_key,
#         time_key,
#         location_key,
#         count_type,
#         count_total,
#         count_in,
#         count_out
#     )
#     SELECT
#         TO_CHAR(sc.datum,'yyyymmdd')::INT AS date_key,
#         EXTRACT(HOUR FROM sc.datum)*100 + EXTRACT(MINUTE FROM sc.datum) AS time_key,
#         sc.fk_standort AS location_key,
#         dl.count_type AS count_type,
#         sc.velo_in + sc.velo_out + sc.fuss_in + sc.fuss_out AS count_total,
#         sc.velo_in + sc.fuss_in AS count_in,
#         sc.velo_out + sc.fuss_out AS count_out
#     FROM staging_NonMotCount AS sc
#     JOIN dim_location AS dl
#         ON dl.location_id = sc.fk_standort
#     """
# )


# QUERY LISTS

create_table_queries = [
    create_albums,
]

drop_table_queries = [
    drop_staging_album,
]

# copy_table_queries = [
#     copy_staging_NonMotCount,
# ]

# insert_table_queries = [
#     insert_dim_location,
# ]
