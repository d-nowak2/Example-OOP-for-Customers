"""
    GoldCustomer.py
    Subclass that overrides discount_rate() and adds a Gold-only behavior.
"""

from __future__ import annotations
from Customer import Customer

class GoldCustomer(Customer):
    def discount_rate(self, on_date=None) -> float:
        return 0.15  # 15% always

    def points_earned(self, subtotal: float) -> int:
        subtotal = float(subtotal)
        if subtotal < 0:
            raise ValueError("subtotal cannot be negative")
        return int(subtotal) * 2  # 2 points per $1, rounded down
