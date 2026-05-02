import sqlite3
import pandas as pd
from config import SQLITE_PATH
from utils import logger

def extract_all():
    conn = sqlite3.connect(SQLITE_PATH)

    def read(table):
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        logger.info(f"Read {table}: {df.shape}")
        return df

    data = {
        "customers": read("customers"),
        "geolocation": read("geolocation"),
        "orders": read("orders"),
        "order_items": read("order_items"),
        "payments": read("order_payments"),
        "reviews": read("order_reviews"),
        "products": read("products"),
        "sellers": read("sellers"),
        "translation": read("product_category_name_translation"),
        "leads_qual": read("leads_qualified"),
        "leads_closed": read("leads_closed")
    }

    conn.close()
    return data