import pandas as pd
from load import load

def build_facts(data, lookups):

    orders = data["orders"]
    items = data["order_items"]
    payments = data["payments"]
    reviews = data["reviews"]
    leads_qual = data["leads_qual"]
    leads_closed = data["leads_closed"]

    # ================= fact_sales =================
    fact_sales = items.merge(
        orders[['order_id','customer_id','order_purchase_timestamp','order_status']],
        on='order_id'
    )

    fact_sales['customer_key'] = fact_sales['customer_id'].map(lookups['customer'])
    fact_sales['seller_key'] = fact_sales['seller_id'].map(lookups['seller'])
    fact_sales['product_key'] = fact_sales['product_id'].map(lookups['product'])
    fact_sales['order_time_key'] = fact_sales['order_purchase_timestamp'].dt.strftime('%Y%m%d').astype(int)
    fact_sales['order_status_key'] = fact_sales['order_status'].map(lookups['status'])

    fact_sales['total_item_value'] = fact_sales['price'] + fact_sales['freight_value']
    fact_sales['quantity'] = 1

    fact_sales = fact_sales.dropna(subset=[
    'customer_key','seller_key','product_key','order_time_key'
    ])
    load(fact_sales[[
        'order_id','order_item_id','customer_key','seller_key','product_key',
        'order_time_key','order_status_key','price','freight_value','quantity','total_item_value'
    ]], "fact_sales")

    # ================= fact_order =================
    orders['delivery_days'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days

    freight = items.groupby('order_id')['freight_value'].sum().reset_index()

    reviews_sorted = reviews.sort_values('review_answer_timestamp', ascending=False)
    latest_review = reviews_sorted.drop_duplicates('order_id')[['order_id','review_score']]

    fact_order = orders.merge(freight, on='order_id', how='left').merge(latest_review, on='order_id', how='left')

    fact_order['customer_key'] = fact_order['customer_id'].map(lookups['customer'])
    fact_order['order_time_key'] = fact_order['order_purchase_timestamp'].dt.strftime('%Y%m%d').astype(int)
    fact_order['order_status_key'] = fact_order['order_status'].map(lookups['status'])

    fact_order = fact_order.dropna()

    load(fact_order[[
        'order_id','customer_key','order_time_key','order_status_key',
        'delivery_days','freight_value','review_score'
    ]], "fact_order")

    # ================= fact_payments =================
    fact_pay = payments.merge(orders[['order_id','customer_id','order_purchase_timestamp']], on='order_id')

    fact_pay['customer_key'] = fact_pay['customer_id'].map(lookups['customer'])
    fact_pay['payment_time_key'] = fact_pay['order_purchase_timestamp'].dt.strftime('%Y%m%d').astype(int)
    fact_pay['payment_type_key'] = fact_pay['payment_type'].map(lookups['payment'])

    fact_pay = fact_pay.dropna()

    load(fact_pay[[
        'order_id','payment_sequential','customer_key',
        'payment_time_key','payment_type_key','payment_value','payment_installments'
    ]], "fact_payments")

    # ================= fact_leads =================
    leads = leads_qual.merge(leads_closed, on='mql_id', how='left')

    leads['converted'] = leads['won_date'].notna()
    leads['seller_key'] = leads['seller_id'].map(lookups['seller'])
    leads['first_contact_time_key'] = leads['first_contact_date'].dt.strftime('%Y%m%d').astype(int)

    leads['won_time_key'] = pd.to_numeric(
        leads['won_date'].dt.strftime('%Y%m%d'), errors='coerce'
    ).astype('Int64')

    leads['business_segment_key'] = leads['business_segment'].map(lookups['segment'])
    leads['lead_type_key'] = leads['lead_type'].map(lookups['lead_type'])

    leads = leads.dropna(subset=['seller_key','first_contact_time_key'])

    load(leads[[
        'mql_id','seller_key','first_contact_time_key','won_time_key',
        'business_segment_key','lead_type_key','has_company','has_gtin',
        'average_stock','declared_product_catalog_size','declared_monthly_revenue','converted'
    ]], "fact_leads")