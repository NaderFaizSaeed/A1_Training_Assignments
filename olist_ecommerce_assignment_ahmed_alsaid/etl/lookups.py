import pandas as pd
from load import engine

def build_lookups():

    def get_dict(query, key, val):
        df = pd.read_sql(query, engine)
        return dict(zip(df[key], df[val]))

    return {
        "customer": get_dict("SELECT customer_id, customer_key FROM dim_customer WHERE is_current=TRUE","customer_id","customer_key"),
        "seller": get_dict("SELECT seller_id, seller_key FROM dim_seller WHERE is_current=TRUE","seller_id","seller_key"),
        "product": get_dict("SELECT product_id, product_key FROM dim_product WHERE is_current=TRUE","product_id","product_key"),
        "status": get_dict("SELECT status, status_key FROM dim_order_status","status","status_key"),
        "payment": get_dict("SELECT payment_type, payment_type_key FROM dim_payment_type","payment_type","payment_type_key"),
        "segment": get_dict("SELECT segment, segment_key FROM dim_business_segment","segment","segment_key"),
        "lead_type": get_dict("SELECT lead_type, lead_type_key FROM dim_lead_type","lead_type","lead_type_key")
    }