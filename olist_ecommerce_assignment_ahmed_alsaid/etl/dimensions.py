from load import load
from config import DEFAULT_START_DATE

def load_static_dimensions(data):

    orders = data["orders"]
    payments = data["payments"]
    leads_closed = data["leads_closed"]

    dim_status = orders[['order_status']].drop_duplicates().dropna()
    dim_status.columns = ['status']
    load(dim_status, 'dim_order_status')

    dim_pay = payments[['payment_type']].drop_duplicates().dropna()
    load(dim_pay, 'dim_payment_type')

    dim_segment = leads_closed[['business_segment']].drop_duplicates().dropna()
    dim_segment.columns = ['segment']
    load(dim_segment, 'dim_business_segment')

    dim_lead = leads_closed[['lead_type']].drop_duplicates().dropna()
    load(dim_lead, 'dim_lead_type')

def load_dimensions(data):
    customers = data["customers"]
    sellers = data["sellers"]
    products = data["products"]

    def scd2(df, table, cols):
        df = df[cols].copy()
        df['effective_start_date'] = DEFAULT_START_DATE
        df['effective_end_date'] = None
        df['is_current'] = True
        load(df, table)

    scd2(customers, "dim_customer", [
        'customer_id','customer_unique_id','customer_city','customer_state'
    ])

    scd2(sellers, "dim_seller", [
        'seller_id','seller_city','seller_state'
    ])

    scd2(products, "dim_product", [
        'product_id','product_category_name_english'
    ])