import pandas as pd

def transform(data):
    customers = data["customers"]
    geolocation = data["geolocation"]
    orders = data["orders"]
    order_items = data["order_items"]
    payments = data["payments"]
    reviews = data["reviews"]
    products = data["products"]
    sellers = data["sellers"]
    translation = data["translation"]
    leads_qual = data["leads_qual"]
    leads_closed = data["leads_closed"]

    # تحويل التواريخ
    date_cols = ['order_purchase_timestamp','order_approved_at',
                 'order_delivered_carrier_date','order_delivered_customer_date',
                 'order_estimated_delivery_date']

    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors='coerce')

    reviews['review_creation_date'] = pd.to_datetime(reviews['review_creation_date'], errors='coerce')
    reviews['review_answer_timestamp'] = pd.to_datetime(reviews['review_answer_timestamp'], errors='coerce')
    leads_qual['first_contact_date'] = pd.to_datetime(leads_qual['first_contact_date'], errors='coerce')
    leads_closed['won_date'] = pd.to_datetime(leads_closed['won_date'], errors='coerce')

    # تنظيف
    customers['customer_city'] = customers['customer_city'].str.strip().str.title()
    customers['customer_state'] = customers['customer_state'].str.strip().str.upper()
    customers['customer_zip_code_prefix'] = customers['customer_zip_code_prefix'].astype(str).str.zfill(5)

    sellers['seller_city'] = sellers['seller_city'].str.strip().str.title()
    sellers['seller_state'] = sellers['seller_state'].str.strip().str.upper()
    sellers['seller_zip_code_prefix'] = sellers['seller_zip_code_prefix'].astype(str).str.zfill(5)

    orders['order_status'] = orders['order_status'].str.strip().str.lower()
    payments['payment_type'] = payments['payment_type'].str.strip().str.lower()

    # المنتجات
    for col in ['product_weight_g','product_length_cm','product_height_cm','product_width_cm']:
        products[col] = products[col].fillna(products[col].median())

    products['product_category_name'] = products['product_category_name'].fillna('unknown').str.lower()
    products = products.merge(translation, on='product_category_name', how='left')
    products['product_category_name_english'] = products['product_category_name_english'].fillna('unknown')

    # geo
    geo_agg = geolocation.groupby('geolocation_zip_code_prefix').agg(
        geolocation_lat=('geolocation_lat','mean'),
        geolocation_lng=('geolocation_lng','mean')
    ).reset_index()

    geo_agg['geolocation_zip_code_prefix'] = geo_agg['geolocation_zip_code_prefix'].astype(str).str.zfill(5)

    customers = customers.merge(geo_agg, left_on='customer_zip_code_prefix',
                                right_on='geolocation_zip_code_prefix', how='left')

    sellers = sellers.merge(geo_agg, left_on='seller_zip_code_prefix',
                            right_on='geolocation_zip_code_prefix', how='left')

    return {
        "customers": customers,
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
        "reviews": reviews,
        "products": products,
        "sellers": sellers,
        "leads_qual": leads_qual,
        "leads_closed": leads_closed
    }