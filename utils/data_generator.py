"""
Utility script to generate realistic synthetic sales data.

This script can be run independently to regenerate the dataset:

    python utils/data_generator.py
"""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List


@dataclass
class Product:
    category: str
    name: str
    base_price: float
    margin_pct: float


REGIONS = ["North", "South", "East", "West"]

COUNTRIES_BY_REGION = {
    "North": ["USA", "Canada"],
    "South": ["Brazil", "Argentina"],
    "East": ["China", "Japan", "India"],
    "West": ["UK", "Germany", "France"],
}

CUSTOMER_SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SALES_CHANNELS = ["Online", "Retail"]

PRODUCTS: List[Product] = [
    Product("Electronics", "Smartphone X", 800, 0.25),
    Product("Electronics", "Laptop Pro", 1200, 0.22),
    Product("Electronics", "Wireless Headphones", 150, 0.35),
    Product("Electronics", "4K Monitor", 400, 0.28),
    Product("Furniture", "Ergonomic Chair", 250, 0.3),
    Product("Furniture", "Standing Desk", 500, 0.32),
    Product("Furniture", "Bookshelf", 120, 0.27),
    Product("Clothing", "Men's Jacket", 90, 0.4),
    Product("Clothing", "Women's Dress", 80, 0.42),
    Product("Clothing", "Running Shoes", 110, 0.38),
    Product("Grocery", "Organic Coffee Beans", 12, 0.3),
    Product("Grocery", "Olive Oil Premium", 18, 0.28),
    Product("Grocery", "Breakfast Cereal", 6, 0.25),
]


def random_date(start: datetime, end: datetime) -> datetime:
    """Return a random datetime between `start` and `end`."""
    delta = end - start
    random_days = random.randrange(delta.days + 1)
    # Bias slightly toward more recent dates
    bias_factor = random.random() ** 2
    random_days = int(random_days * bias_factor)
    return start + timedelta(days=random_days)


def generate_sales_data(num_rows: int = 1500) -> List[dict]:
    """Generate a list of synthetic sales records."""
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)

    data: List[dict] = []
    for order_id in range(1, num_rows + 1):
        order_date = random_date(start_date, end_date)

        region = random.choice(REGIONS)
        country = random.choice(COUNTRIES_BY_REGION[region])
        product = random.choice(PRODUCTS)
        sales_channel = random.choices(SALES_CHANNELS, weights=[0.6, 0.4])[0]
        customer_segment = random.choice(CUSTOMER_SEGMENTS)

        # Quantities depend a bit on channel and category
        if sales_channel == "Online":
            base_qty = random.randint(1, 5)
        else:
            base_qty = random.randint(1, 10)

        # Grocery tends to have higher quantity per order
        if product.category == "Grocery":
            base_qty += random.randint(1, 10)

        quantity = max(1, base_qty)

        # Unit price with small random variation around base price
        price_variation = random.uniform(0.9, 1.1)
        unit_price = round(product.base_price * price_variation, 2)

        total_sales = round(quantity * unit_price, 2)

        # Profit margin variation per order
        margin_variation = random.uniform(0.8, 1.2)
        profit_margin = product.margin_pct * margin_variation
        profit = round(total_sales * profit_margin, 2)

        record = {
            "order_id": f"ORD-{order_id:06d}",
            "order_date": order_date.strftime("%Y-%m-%d"),
            "region": region,
            "country": country,
            "product_category": product.category,
            "product_name": product.name,
            "sales_channel": sales_channel,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_sales": total_sales,
            "profit": profit,
            "customer_segment": customer_segment,
        }
        data.append(record)

    return data


def save_to_csv(records: List[dict], output_path: Path) -> None:
    """Persist generated records to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "order_id",
        "order_date",
        "region",
        "country",
        "product_category",
        "product_name",
        "sales_channel",
        "quantity",
        "unit_price",
        "total_sales",
        "profit",
        "customer_segment",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    """Generate and save the synthetic sales dataset."""
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "data" / "sales_data.csv"

    num_rows = 2000  # >= 1000 as requested
    records = generate_sales_data(num_rows=num_rows)
    save_to_csv(records, output_path)
    print(f"Generated {len(records)} rows at {output_path}")


if __name__ == "__main__":
    main()


