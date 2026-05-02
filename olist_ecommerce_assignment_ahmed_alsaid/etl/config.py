from datetime import date

from sqlalchemy import URL

SQLITE_PATH = "olist.sqlite"

PG_DB_URL = URL.create(
    drivername="postgresql",
    username="postgres",
    password="nader@#$123",
    host="localhost",
    database="olist_ecommerce_dw"
 )

DEFAULT_START_DATE = date(2016, 1, 1)