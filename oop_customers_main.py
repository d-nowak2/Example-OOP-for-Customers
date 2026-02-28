"""
    oop_customers_main.py
    Main program: reads a CSV file into class objects (Customer / SeasonalCustomer / GoldCustomer),
    stores them in a list, and demonstrates overriding + encapsulation.

    Run:
        python oop_customers_main.py
"""

from __future__ import annotations

import csv
import datetime as dt
import sys
from pathlib import Path
from typing import List

from Customer import Customer
from SeasonalCustomer import SeasonalCustomer
from GoldCustomer import GoldCustomer


def customer_from_row(row: dict) -> Customer:
    """
    Factory function: returns the correct object type based on the CSV row.
    Keeping this logic here avoids stuffing 'type switches' inside your classes.
    """
    ctype = (row.get("customer_type") or "").strip().lower()

    customer_id = row["customer_id"]
    name = row["name"]
    email = row["email"]
    total_spent = float(row.get("total_spent") or 0)
    visits = int(row.get("visits") or 0)

    if ctype == "seasonal":
        season = row.get("season") or "Winter"
        return SeasonalCustomer(customer_id, name, email, season=season, total_spent=total_spent, visits=visits)

    if ctype in {"gold", "gold-member", "gold_member"}:
        return GoldCustomer(customer_id, name, email, total_spent=total_spent, visits=visits)

    # default: regular
    return Customer(customer_id, name, email, total_spent=total_spent, visits=visits)


def load_customers(csv_file: Path) -> List[Customer]:
    customers: List[Customer] = []
    with csv_file.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers.append(customer_from_row(row))
    return customers


def demo(customers: List[Customer]) -> None:
    print("\nLoaded customers:")
    for c in customers:
        print(" ", c.summary())

    print("\nOverriding / Polymorphism demo: same call, different results (final_price on a $100 subtotal):")
    today = dt.date.today()
    for c in customers[:6]:
        print(
            f"  {c.name:18} {c.__class__.__name__:14} "
            f"discount={c.discount_rate(today):.0%} final=${c.final_price(100, today):.2f}"
        )

    print("\nEncapsulation demo: record_purchase($35.50) updates state through validated properties:")
    for c in customers[:3]:
        before = c.total_spent
        c.record_purchase(35.50)
        print(f"  {c.name:18} total_spent: ${before:.2f} -> ${c.total_spent:.2f} | visits={c.visits}")

    print("\nSubclass-only behavior demo: Gold customers earn bonus points:")
    for c in customers:
        if isinstance(c, GoldCustomer):
            print(f"  {c.name:18} points on $42 = {c.points_earned(42)}")


if __name__ == "__main__":
    current_path = (Path(__file__).parent / 'customers_demo.csv').resolve()
    customers = load_customers(current_path)
    demo(customers)