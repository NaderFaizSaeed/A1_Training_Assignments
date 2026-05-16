import csv
import os
import random
import time
from datetime import datetime
from faker import Faker

fake = Faker()

OUTPUT_DIR = "./lab_data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

payment_methods = [
    "CreditCard",
    "Cash",
    "PayPal",
    "ApplePay"
]

order_statuses = [
    "Delivered",
    "Pending",
    "Cancelled",
    "Returned"
]


def generate_timestamp():

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%m-%d-%Y %I:%M %p"
    ]

    selected_format = random.choice(formats)

    return datetime.now().strftime(selected_format)


def generate_valid_record(order_id):

    return [
        order_id,
        f"CUST{random.randint(100,999)}",
        f"PRD{random.randint(10,99)}",
        round(random.uniform(10, 1000), 2),
        random.choice(payment_methods),
        random.choice(order_statuses),
        generate_timestamp()
    ]


def generate_invalid_record(order_id):

    invalid_type = random.choice([
        "missing",
        "corrupted_customer",
        "corrupted_payment",
        "invalid_amount",
        "duplicate",
        "bad_timestamp"
    ])

    if invalid_type == "missing":
        return [
            order_id,
            "",
            f"PRD{random.randint(10,99)}",
            round(random.uniform(10, 1000), 2),
            "Cash",
            "Delivered",
            generate_timestamp()
        ]

    elif invalid_type == "corrupted_customer":
        return [
            order_id,
            "%%%%CORRUPTED%%%%",
            f"PRD{random.randint(10,99)}",
            round(random.uniform(10, 1000), 2),
            "Cash",
            "Delivered",
            generate_timestamp()
        ]

    elif invalid_type == "corrupted_payment":
        return [
            order_id,
            f"CUST{random.randint(100,999)}",
            f"PRD{random.randint(10,99)}",
            round(random.uniform(10, 1000), 2),
            "%%%%CORRUPTED%%%%",
            "Delivered",
            generate_timestamp()
        ]

    elif invalid_type == "invalid_amount":
        return [
            order_id,
            f"CUST{random.randint(100,999)}",
            f"PRD{random.randint(10,99)}",
            "INVALID",
            "CreditCard",
            "Delivered",
            generate_timestamp()
        ]

    elif invalid_type == "duplicate":
        return [
            1001,
            "CUST101",
            "PRD10",
            250,
            "Cash",
            "Delivered",
            generate_timestamp()
        ]

    elif invalid_type == "bad_timestamp":
        return [
            order_id,
            f"CUST{random.randint(100,999)}",
            f"PRD{random.randint(10,99)}",
            round(random.uniform(10, 1000), 2),
            "PayPal",
            "Pending",
            "99-99-9999"
        ]


while True:

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"orders_{current_time}.csv"

    file_path = os.path.join(OUTPUT_DIR, file_name)

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "order_id",
            "customer_id",
            "product_id",
            "amount",
            "payment_method",
            "order_status",
            "timestamp"
        ])

        for i in range(20):

            order_id = random.randint(1000, 9999)

            if random.random() < 0.2:
                row = generate_invalid_record(order_id)
            else:
                row = generate_valid_record(order_id)

            writer.writerow(row)

    print(f"Generated: {file_name}")

    time.sleep(5)